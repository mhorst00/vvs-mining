import sys
import vvspy
import concurrent.futures
import requests
import utils
import db
import discord_logging

from datetime import datetime
from retry import retry


@retry(TypeError, delay=2, tries=3)
def get_trips_with_retries(
    start: str, destination: str, time: datetime, session: requests.Session
):
    try:
        trips = vvspy.get_trips(
            start,
            destination,
            time,
            session=session,
            limit=5,
            timeout=(3.05, 6.1),
        )

    except Exception as err:
        discord_logging.warning(err)
    if trips is None:
        discord_logging.info("trips was null in retry function")
        raise TypeError("trips was null")
    return trips


def get_all_trips_from_station(start: str, stations: list[str], time: datetime):
    results = []
    session = requests.Session()
    for destination in stations:
        if start is not destination:
            try:
                trips = get_trips_with_retries(
                    start, destination, time, session=session
                )
                if trips is not None:
                    for i in trips:
                        if isinstance(i, vvspy.obj.Trip):
                            trip = i.raw
                            del trip["fare"]
                            del trip["isAdditional"]
                            del trip["daysOfService"]
                            for leg in range(len(trip["legs"])):
                                if "coords" in trip["legs"][leg]:
                                    del trip["legs"][leg]["coords"]
                            results.append(trip)
                else:
                    discord_logging.info(
                        "trips is None for:"
                        + utils.station_id_to_name(start)
                        + " "
                        + utils.station_id_to_name(destination)
                    )
            except Exception as err:
                discord_logging.warning(err)
    return results


def get_station_departures(station: str, time: datetime):
    return vvspy.get_departures(station, time)


def get_all_trips(stations: list[str], curr_time: datetime):
    trips = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(stations)) as executor:
        future_to_trip = {
            executor.submit(
                get_all_trips_from_station, start, stations, curr_time
            ): start
            for start in stations
        }
        for future in concurrent.futures.as_completed(future_to_trip):
            try:
                trips.extend(future.result())
            except Exception as err:
                discord_logging.error(err)
        return trips


def get_all_station_departures(stations: list[str], curr_time: datetime):
    station_delays = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(stations)) as executor:
        future_to_trip = {
            executor.submit(get_station_departures, start, curr_time): start
            for start in stations
        }
        for future in concurrent.futures.as_completed(future_to_trip):
            try:
                station_delays.extend(future.result())
            except Exception as err:
                discord_logging.error(err)
    return station_delays


if __name__ == "__main__":
    discord_logging.initialise()
    discord_logging.info("Starting import")
    curr_time = datetime.now()
    stations = utils.read_station_ids_csv("vvs_sbahn_haltestellen_2022.csv")
    try:
        trips = get_all_trips(stations, curr_time)
        tripCount = len(trips)
        x = db.new_entries(trips)
        if x:
            discord_logging.error("Could not save trips")
        trips = get_all_station_departures(stations, curr_time)
        time_for_execute = datetime.now() - curr_time
        discord_logging.finishLogging(tripCount, sys.getsizeof(trips))
        del trips
    except Exception as err:
        discord_logging.error(err)
        discord_logging.finishLogging(0, 0)

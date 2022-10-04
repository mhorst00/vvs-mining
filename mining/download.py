import sys
import vvspy
import concurrent.futures
import requests
import utils
import discord_logging

from datetime import datetime
from retry import retry


@retry(Exception, delay=1, tries=5)
def get_trips_with_retries(
    start: str, destination: str, time: datetime, session: requests.Session
):
    try:
        trips = vvspy.get_trips(
            start, destination, time, session=session, limit=5, timeout=(3.05, 6.1)
        )
        if trips is None:
            raise Exception("trips is none")
    except Exception as err:
        discord_logging.warning(str(err))
        raise Exception("Request timeout")
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
                for i in trips:
                    if isinstance(i, vvspy.obj.Trip):
                        trip = i.raw
                        results.append(trip)
            except Exception as err:
                discord_logging.warning(
                    str(err) + utils.station_id_to_name(start),
                    utils.station_id_to_name(destination) + str(type(trip)),
                )
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
                discord_logging.error(str(err))
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
                discord_logging.error(str(err))
    return station_delays


curr_time = datetime.now()
stations = utils.read_station_ids_csv("vvs_sbahn_haltestellen_2022.csv")

print(utils.station_id_to_name(stations[14]))
trips = get_all_trips(stations, curr_time)
# trips = get_all_station_departures(stations, curr_time)
print("Number of trips: ", len(trips))
print("Size in bytes: ", sys.getsizeof(trips))
discord_logging.finishLogging(len(trips), sys.getsizeof(trips))

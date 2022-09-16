import vvspy
import csv
import concurrent.futures
from datetime import datetime


def get_all_trips_from_station(start: str, stations: list[str], time: datetime):
    trips = []
    for destination in stations:
        if start is not destination:
            trips.append(vvspy.get_trip(start, destination, time).raw)
    return trips


def get_station_delay(station: str, time: datetime):
    return vvspy.get_departures(station, time)


def get_all_trips(stations: list[str], curr_time: datetime):
    trips = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        future_to_trip = {
            executor.submit(get_all_trips, start, stations, curr_time): start
            for start in stations
        }
        for future in concurrent.futures.as_completed(future_to_trip):
            trip = future_to_trip[future]
            try:
                trips.extend(future.result())
            except Exception as err:
                print(err)
        return trips


def get_all_station_delays(stations: list[str], curr_time: datetime):
    station_delays = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        future_to_trip = {
            executor.submit(get_station_delay, start, curr_time): start
            for start in stations
        }
        for future in concurrent.futures.as_completed(future_to_trip):
            delay = future_to_trip[future]
            try:
                station_delays.extend(future.result())
            except Exception as err:
                print(err)
    return station_delays


curr_time = datetime.now()

stations: list[str] = []
with open("vvs_sbahn_haltestellen_2022.csv", "r") as f:
    reader = csv.reader(f, delimiter=";")
    for line in reader:
        stations.append(line[3])

trip = vvspy.get_trip(stations[26], stations[14], curr_time).raw

trip["legs"][0].pop("coords")
trip.pop("fare")

print(trip)

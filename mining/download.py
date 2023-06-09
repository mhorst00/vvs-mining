import sys
from datetime import datetime

import db
import discord_logging
import utils
import vvspy


def get_all_departures(stations: list[str], time: datetime, limit: int):
    departures = []
    try:
        for station in stations:
            station_deps = vvspy.get_departures(station, time, limit=limit)
            if isinstance(station_deps, list):
                departures.extend(station_deps)
    except Exception as err:
        discord_logging.error(err)
    return departures


if __name__ == "__main__":
    discord_logging.initialise()
    discord_logging.info("Starting import")
    curr_time = datetime.now()
    hf_stations = utils.read_station_ids_csv("vvs_hf_stations.csv")
    lf_stations = utils.read_station_ids_csv("vvs_lf_stations.csv")
    try:
        deps = get_all_departures(lf_stations, curr_time, 10)
        deps.extend(get_all_departures(hf_stations, curr_time, 20))
        dep_count = len(deps)
        print(dep_count)
        x = db.new_entries(deps)
        if x:
            discord_logging.error(f"Could not save departures. Reason: {x}")
        time_for_execute = datetime.now() - curr_time
        discord_logging.finishLogging(dep_count, sys.getsizeof(deps))
        del deps
    except Exception as err:
        discord_logging.error(err)
        discord_logging.finishLogging(0, 0)

import csv
import random
import urllib
import json

full_station_file = []
proxy_list = []


def read_station_ids_csv(file: str) -> list[str]:
    """Read csv file with VVS stations line-by-line"""
    stations: list[str] = []
    with open(file, "r") as f:
        reader = csv.reader(f, delimiter=";")
        for line in reader:
            full_station_file.append(line)
            stations.append(line[3])
    return stations


def station_id_to_name(station_id: str) -> str:
    for line in full_station_file:
        if line[3] == station_id:
            return line[0]


def get_proxy_list() -> list[str]:
    for line in urllib.request.urlopen(
        "https://raw.githubusercontent.com/shiftytr/proxy-list/master/https.txt"
    ):
        proxy_list.append(line)
    return proxy_list


def get_random_proxy() -> dict:
    raw = random.choice(proxy_list)
    return {"https": raw}


if __name__ == "__main__":
    tmp = read_station_ids_csv("vvs_sbahn_haltestellen_2022.csv")
    file = open("haltestellen.json", "w")
    file.write(json.dumps(tmp))

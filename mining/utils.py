import csv

full_station_file = []


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

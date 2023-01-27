import argparse
import zstandard
import pathlib
import polars as pl
from enum import Enum


class Mode(Enum):
    STATION_DELAY = 1


parser = argparse.ArgumentParser(
    prog="DB_Extraction_tool",
    description="Construct single Database from one or more sources",
)
parser.add_argument(
    "-o", dest="filename", type=str, help="Name of the output file", required=True
)
parser.add_argument(
    "-m",
    dest="mode",
    type=str,
    default="STATION_DELAY",
    choices={"STATION_DELAY"},
    help="In which mode the program should run",
)
parser.add_argument(
    "dblist",
    type=str,
    nargs="+",
    help="Name of the DB which should be used. Can be passed multiple times",
)


def zstd_to_temp(input_file):
    input_file = pathlib.Path(input_file)
    with open(input_file, "rb") as compressed:
        decomp = zstandard.ZstdDecompressor()
        output_path = pathlib.Path("temp.db")
        with open(output_path, "wb") as destination:
            decomp.copy_stream(compressed, destination)


def read_db_to_df(mode: Mode) -> pl.DataFrame:
    conn = f"sqlite://{pathlib.Path('temp.db')}"
    if mode is Mode.STATION_DELAY:
        query = """
        SELECT DISTINCT
        stops.name, legs.transportation_name,
        legs.transportation_properties_trainNumber, stops.arrivalTimePlanned,
        stops.arrivalTimeEstimated, stops.departureTimePlanned,
        stops.departureTimeEstimated
        FROM trips
        INNER JOIN legs
        ON trips.data_id=legs.data_trip_id
        INNER JOIN stops
        on legs.data_id=stops.data_leg_id
        where transportation_name='S-Bahn S5'
        GROUP BY transportation_properties_trainNumber, name
        """
    else:
        query = ""

    df = pl.read_sql(query, conn)
    return df


def calculate_delays(mode: Mode, df: pl.DataFrame):
    # TODO drop stops only if both arrival and departure are null
    if mode is Mode.STATION_DELAY:
        pass
    pass


if __name__ == "__main__":
    args = parser.parse_args()
    run_mode = Mode[args.mode]
    for elem in args.dblist:
        print(f"Extracting {elem}...")
        zstd_to_temp(elem)
        print("Reading source db...")
        df = read_db_to_df(run_mode)
        print(df)
        print(df.drop_nulls())
        pathlib.Path("temp.db").unlink()

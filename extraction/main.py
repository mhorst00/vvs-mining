import argparse
import zstandard
import pathlib
from psycopg2 import sql
import psycopg2.extras
import polars as pl
from enum import Enum


class Mode(Enum):
    STATION_DELAY = 1
    TRAIN_INCIDENT = 2
    STATION_INFO = 3


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
    choices={"STATION_DELAY", "TRAIN_INCIDENT", "STATION_INFO"},
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
        GROUP BY transportation_properties_trainNumber, name
        """
    elif mode is Mode.TRAIN_INCIDENT:
        query = """
        SELECT
        stops.name, legs.transportation_name,
        legs.transportation_properties_trainNumber,
                hints.content
        FROM trips
        INNER JOIN legs
        ON trips.data_id=legs.data_trip_id
        INNER JOIN stops
        on legs.data_id=stops.data_leg_id
                INNER JOIN hints
                on legs.data_id=hints.data_leg_id
                WHERE hints.type like("%incident%")
                GROUP BY legs.transportation_properties_trainNumber, stops.name
        """
    elif mode is Mode.STATION_INFO:
        query = """
        SELECT tmp.data_leg_id, tmp.id, stops.name, tmp.type, tmp.urlText, tmp.content
        FROM (SELECT data_leg_id,id, type, urlText, content FROM infos GROUP BY id) as tmp
        INNER JOIN stops ON tmp.data_leg_id = stops.data_leg_id
        WHERE tmp.content LIKE ("%" || stops.name || "%")
        """
    else:
        query = ""

    df = pl.read_sql(query, conn)
    return df


def write_df_to_db(mode: Mode, df: pl.DataFrame):
    columns = sql.SQL(",").join(sql.Identifier(name.lower()) for name in df.columns)
    values = sql.SQL(",").join([sql.Placeholder() for _ in df.columns])
    table_name = mode.name.lower()
    insert_stmt = sql.SQL("INSERT INTO {} ({}) VALUES({});").format(
        sql.Identifier(table_name), columns, values
    )
    conn = psycopg2.connect(
        database="data", user="admin", password="admin", host="127.0.0.1", port="5432"
    )
    create_psql_table(mode, conn)
    cur = conn.cursor()
    psycopg2.extras.execute_batch(cur, insert_stmt, df.rows())
    conn.commit()


def create_psql_table(mode: Mode, c: psycopg2.connection):
    if mode is Mode.STATION_DELAY:
        cur = c.cursor()
        cur.execute(
            f"""CREATE TABLE IF NOT EXISTS {mode.name} (
                        name text,
                        transportation_name text,
                        transportation_properties_trainNumber integer,
                        arrivalTimePlanned timestamp,
                        arrivalTimeEstimated timestamp,
                        departureTimePlanned timestamp,
                        departureTimeEstimated timestamp,
                        arrivalDelay interval,
                        departureDelay interval
                        )"""
        )
        c.commit()


def calculate_delays(mode: Mode, df: pl.DataFrame) -> pl.DataFrame:
    df = df.filter(~pl.all(pl.col("transportation_name").str.contains("Stadtbahn")))
    if mode is Mode.STATION_DELAY:
        df = df.filter(~pl.all(pl.col("^.*Time.*$").is_null()))
        df = df.with_columns(
            pl.col("^.*Time.*$").str.strptime(pl.Datetime, fmt="%+").cast(pl.Datetime)
        )
        df = df.with_columns(
            [
                (pl.col("arrivalTimeEstimated") - pl.col("arrivalTimePlanned")).alias(
                    "arrivalDelay"
                ),
                (
                    pl.col("departureTimeEstimated") - pl.col("departureTimePlanned")
                ).alias("departureDelay"),
            ]
        )
        return df
    else:
        pass


if __name__ == "__main__":
    args = parser.parse_args()
    run_mode = Mode[args.mode]
    for elem in args.dblist:
        print(f"Extracting {elem}...")
        zstd_to_temp(elem)
        print("Reading source db...")
        df = read_db_to_df(run_mode)
        pathlib.Path("temp.db").unlink()
        print(df)
        df = calculate_delays(run_mode, df)
        print(df)
        write_df_to_db(run_mode, df)

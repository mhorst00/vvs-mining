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
    "-o", dest="psql_host", type=str, help="PostgreSQL hostname", required=True
)
parser.add_argument(
    "-u", dest="psql_user", type=str, help="PostgreSQL username", required=True
)
parser.add_argument(
    "-p", dest="psql_pass", type=str, help="PostgreSQL password", required=True
)
parser.add_argument(
    "--port",
    dest="psql_port",
    type=str,
    help="PostgreSQL port",
    required=False,
    default=5432,
)
parser.add_argument(
    "--db",
    dest="psql_db",
    type=str,
    help="PostgreSQL database name",
    required=False,
    default="data",
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
        hints.content, stops.arrivalTimePlanned, stops.departureTimePlanned
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
        SELECT tmp.data_leg_id, tmp.id, stops.name, tmp.type, tmp.urlText, tmp.content,
        stops.arrivalTimePlanned, stops.departureTimePlanned
        FROM (SELECT data_leg_id,id, type, urlText, content FROM infos GROUP BY id)
        as tmp
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
        database=args.psql_db,
        user=args.psql_user,
        password=args.psql_pass,
        host=args.psql_host,
        port=args.psql_port,
    )
    create_psql_table(mode, conn)
    cur = conn.cursor()
    psycopg2.extras.execute_batch(cur, insert_stmt, df.rows())
    conn.commit()


def create_psql_table(mode: Mode, c):
    cur = c.cursor()
    if mode is Mode.STATION_DELAY:
        cur.execute(
            f"""CREATE TABLE IF NOT EXISTS {mode.name} (
                        name text,
                        transportation_name text,
                        transportation_properties_trainNumber integer,
                        arrivalTimePlanned timestamp,
                        arrivalTimeEstimated timestamp,
                        departureTimePlanned timestamp,
                        departureTimeEstimated timestamp,
                        arrivalDelay integer,
                        departureDelay integer,
                        delay integer
                        )"""
        )
        c.commit()
    elif mode is Mode.TRAIN_INCIDENT:
        cur.execute(
            f"""CREATE TABLE IF NOT EXISTS {mode.name} (
                        name text,
                        transportation_name text,
                        transportation_properties_trainNumber integer,
                        content text,
                        date timestamp
                        )"""
        )
        c.commit()
    elif mode is Mode.STATION_INFO:
        cur.execute(
            f"""CREATE TABLE IF NOT EXISTS {mode.name} (
                        data_leg_id integer,
                        id text,
                        name text,
                        type text,
                        urlText text,
                        content text,
                        date timestamp
                        )"""
        )
        c.commit()


def calculate_delays(df: pl.DataFrame) -> pl.DataFrame:
    df = df.filter(~pl.all(pl.col("^.*Time.*$").is_null()))
    df = df.with_columns(
        pl.col("^.*Time.*$").str.strptime(pl.Datetime, fmt="%+").cast(pl.Datetime)
    )
    df = df.with_columns(
        [
            (pl.col("arrivalTimeEstimated") - pl.col("arrivalTimePlanned"))
            .dt.seconds()
            .alias("arrivalDelay"),
            (pl.col("departureTimeEstimated") - pl.col("departureTimePlanned"))
            .dt.seconds()
            .alias("departureDelay"),
        ]
    )
    df = df.with_columns(
        [
            pl.col("arrivalDelay").fill_null(strategy="zero"),
            pl.col("departureDelay").fill_null(strategy="zero"),
        ]
    )
    df = df.with_columns(
        [
            pl.when(pl.col("departureDelay") > pl.col("arrivalDelay"))
            .then(pl.col("departureDelay"))
            .otherwise(pl.col("arrivalDelay"))
            .alias("delay"),
        ]
    )
    return df


def calulate_date(df: pl.DataFrame, file_name: str) -> pl.DataFrame:
    date = file_name.removesuffix(".db.zst")
    df = df.with_columns(
        [
            pl.when(pl.col("departureTimePlanned") > pl.col("arrivalTimePlanned"))
            .then(pl.col("departureTimePlanned"))
            .otherwise(pl.col("arrivalTimePlanned"))
            .alias("date"),
        ]
    )
    df = df.with_columns(pl.col("date").fill_null(pl.lit(date)))
    df = df.drop("departureTimePlanned")
    df = df.drop("arrivalTimePlanned")
    return df


if __name__ == "__main__":
    args = parser.parse_args()
    run_mode = Mode[args.mode]
    for elem in args.dblist:
        print(f"Extracting {elem}...")
        zstd_to_temp(elem)
        print("Reading source db...")
        df = read_db_to_df(run_mode)
        pathlib.Path("temp.db").unlink()
        if run_mode is not Mode.STATION_INFO:
            df = df.filter(
                ~pl.all(pl.col("transportation_name").str.contains("Stadtbahn"))
            )
        print("Calculating and filtering...")
        if run_mode is Mode.STATION_DELAY:
            df = calculate_delays(df)
        if run_mode is not Mode.STATION_DELAY:
            df = calulate_date(df, elem)
        write_df_to_db(run_mode, df)

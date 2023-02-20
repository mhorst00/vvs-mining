import argparse
import pathlib
from psycopg2 import sql
import psycopg2.extras
import polars as pl
from enum import Enum


class Mode(Enum):
    STATION_DELAY = 1
    STATION_INFO = 2


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
    choices={"STATION_DELAY", "STATION_INFO"},
    help="In which mode the program should run",
)
parser.add_argument(
    "dblist",
    type=str,
    nargs="+",
    help="Name of the DB which should be used. Can be passed multiple times.",
)


def read_db_to_df(mode: Mode, filename: pathlib.Path) -> pl.DataFrame:
    conn = f"sqlite://{filename}"
    if mode is Mode.STATION_DELAY:
        query = """
        SELECT DISTINCT
        stop_name, servingline_number as line_number,
        datetime as departure_planned, real_datetime as departure_estimated, 
        delay
        FROM departures 
        WHERE servingline_number LIKE '%S%'
        GROUP BY servingline_train_num, stop_name 
        """
    elif mode is Mode.STATION_INFO:
        query = """
        SELECT DISTINCT 
        stop_name, servingline_number as line_number, 
        subject, subtitle, content, date(datetime) as date
        FROM stop_infos 
        INNER JOIN departures
        ON stop_infos.data_dep_id=departures.data_id
        WHERE servingline_number LIKE '%S%'
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
                        stop_name text,
                        line_number text,
                        departure_planned timestamp,
                        departure_estimated timestamp,
                        delay integer
                        )"""
        )
        c.commit()
    elif mode is Mode.STATION_INFO:
        cur.execute(
            f"""CREATE TABLE IF NOT EXISTS {mode.name} (
                        stop_name text,
                        line_number text,
                        subject text,
                        subtitle text,
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
    full_path = pathlib.PurePath(file_name).stem
    date = full_path.removesuffix(".db")
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
        print("Reading source db...")
        df = read_db_to_df(run_mode, pathlib.Path(elem))
        write_df_to_db(run_mode, df)

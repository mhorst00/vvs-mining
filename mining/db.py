import sqlite3


TRIP_TABLE_NAME = "trip_table"
STATION_TABLE_NAME = "station_table"

con = sqlite3.connect("trip_delays.db")
cur = con.cursor()


def trips_to_db(trips: list, cursor: sqlite3.Cursor):
    table_list = cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND"
        f" name='{TRIP_TABLE_NAME}';"
    ).fetchall()
    if len(table_list) == 0:
        cursor.execute(f"CREATE TABLE {TRIP_TABLE_NAME} (id integer, data json)")
    for trip in trips:
        cursor.execute(f"insert into {TRIP_TABLE_NAME} values ?", trip)


def station_delays_to_db(station_delays: list, cursor: sqlite3.Cursor):
    table_list = cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND"
        f" name='{STATION_TABLE_NAME}';"
    ).fetchall()
    if len(table_list) == 0:
        cursor.execute(
            f"CREATE TABLE {STATION_TABLE_NAME} (id integer, data varchar(100))"
        )
    for station_delay in station_delays:
        print(station_delay)
        cursor.execute(
            f"insert into {STATION_TABLE_NAME} values(?,?)", (1, station_delay)
        )

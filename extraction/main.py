import argparse

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
    action="append",
    help="Name of the DB which should be used. Can be passed multiple times",
)

if __name__ == "__main__":
    args = parser.parse_args()

import os
from dotenv import load_dotenv
load_dotenv()

MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DB = os.getenv("MYSQL_DB")

PG_HOST = os.getenv("PG_HOST")
PG_USER = os.getenv("PG_USER")
PG_PASSWORD = os.getenv("PG_PASSWORD")
PG_DB = os.getenv("PG_DB")
SHOULD_DELETE_OLD_DATA = os.getenv("SHOULD_DELETE_OLD_DATA") == "true"
LOGGING_LEVEL = os.getenv("LOGGING_LEVEL") or "info"

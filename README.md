# Translation script

Script that queries the current schedule database and inserts the corresponding data in a new database.
## Prerequisites:
Make sure you have ```python3``` and ```python3-venv``` installed on your machine.
## Instructions:
1. Add a .env file with the following fields:
```
MYSQL_HOST=****
MYSQL_USER=****
MYSQL_PASSWORD=****
MYSQL_DB=****

PG_HOST=****
PG_USER=****
PG_PASSWORD=****
PG_DB=****

# either true or false
SHOULD_DELETE_OLD_DATA=true
# either info or debug
LOGGING_LEVEL=debug
```
2. Run ```./setup.sh```

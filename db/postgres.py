import psycopg2
import config

def get_postgres_connection():
    return psycopg2.connect(
        host=config.PG_HOST,
        user=config.PG_USER,
        password=config.PG_PASSWORD,
        database=config.PG_DB,
        port=config.PG_PORT,
    )

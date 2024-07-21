import psycopg2
from psycopg2.extras import RealDictCursor

POSTGRESQL_DATABASE_URL = "postgres://<UserName>:<Password>@<Host>:<Port>/<DatabaseName>?sslmode=require"

def get_postgresql_connection():
    conn = psycopg2.connect(POSTGRESQL_DATABASE_URL, cursor_factory=RealDictCursor)
    return conn
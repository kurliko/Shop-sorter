import psycopg2
from psycopg2.extras import RealDictCursor

# Dane do Twojej bazy Postgres
DATABASE_URL = "postgresql://filip:filip123@localhost:5432/shop_sorter"

def get_db_connection():
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
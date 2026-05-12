import sqlite3
from pathlib import Path

DB_PATH = Path("database/used_cars.db")

def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH) # opens a connection to the db file


def create_table(name):
    conn = get_connection()
    cursor = conn.cursor() # cursor is what exectues sql commands on the db file

    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            brand TEXT NOT NULL,
            model TEXT NOT NULL,
            year INTEGER NOT NULL,
            mileage INTEGER NOT NULL,
            fuel_type TEXT,
            engine TEXT,
            transmission TEXT,
            ext_col TEXT,
            int_col TEXT,
            accident TEXT,
            clean_title TEXT,
            price REAL NOT NULL
        )
    """)

    conn.commit() # saves create table operation
    conn.close() # closes db connection


def drop_table(name):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"""DROP TABLE IF EXISTS {name}""")

    conn.commit()
    conn.close()




def main():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*) FROM used_cars
    """)
    print(cursor.fetchone())

    conn.close()

if __name__ == "__main__" :
    main()

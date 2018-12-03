import sqlite3

conn = sqlite3.connect(":memory:")

cursor = conn.cursor()

cursor.execute(
    """CREATE TABLE contacts (
        first_name text,
        last_name text,
        email text,
        phone integer,
        address text
    )"""
)

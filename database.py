import sqlite3
from werkzeug.security import generate_password_hash


DATABASE = "secureapi.db"


def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    existing_users = connection.execute(
        "SELECT COUNT(*) FROM users"
    ).fetchone()[0]

    if existing_users == 0:
        connection.execute(
            """
            INSERT INTO users (name, email, password)
            VALUES (?, ?, ?)
            """,
            (
                "Pranay",
                "pranay@example.com",
                generate_password_hash("LOCAL_TEST_PASSWORD")
            )
        )

        connection.execute(
            """
            INSERT INTO users (name, email, password)
            VALUES (?, ?, ?)
            """,
            (
                "Rahul",
                "rahul@example.com",
                generate_password_hash("LOCAL_TEST_PASSWORD")
            )
        )

    connection.commit()
    connection.close()
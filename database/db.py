
from pathlib import Path
import sqlite3

# Find the database folder
BASE_DIR = Path(__file__).resolve().parent

# Database and schema locations
DB_PATH = BASE_DIR / "enterprise360.db"
SCHEMA_PATH = BASE_DIR / "schema.sql"


def get_connection():
    """Connect Python to the SQLite database."""

    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row

    # Enable foreign key validation
    connection.execute("PRAGMA foreign_keys = ON")

    return connection


def initialize_database():
    """Create database tables using schema.sql."""

    if not SCHEMA_PATH.exists():
        raise FileNotFoundError(
            f"SQL schema not found: {SCHEMA_PATH}"
        )

    connection = get_connection()

    try:
        schema = SCHEMA_PATH.read_text(encoding="utf-8")
        connection.executescript(schema)
        connection.commit()

        print("Enterprise360 database initialized successfully!")

    finally:
        connection.close()


if __name__ == "__main__":
    initialize_database()
    print(f"Database location: {DB_PATH}")

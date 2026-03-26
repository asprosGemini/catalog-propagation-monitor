import sqlite3

DB_PATH = "catalog.db"


def create_connection():
    try:
        conn = sqlite3.connect(DB_PATH)
        print(f"✅ Connected to SQLite database: {DB_PATH}")
        return conn
    except sqlite3.Error as e:
        print("❌ SQLite connection error:", e)
        return None


def create_catalog_objects_table(conn):
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS catalog_objects (
        id TEXT,
        type TEXT,
        version INTEGER,
        name TEXT,
        snapshot_type TEXT,
        snapshot_time TEXT
    );
    """

    cursor = conn.cursor()
    cursor.execute(create_table_sql)
    conn.commit()
    print("✅ catalog_objects table is ready")


if __name__ == "__main__":
    conn = create_connection()

    if conn:
        create_catalog_objects_table(conn)
        conn.close()
        print("✅ Connection closed")
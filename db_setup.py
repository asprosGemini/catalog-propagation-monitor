import json
import sqlite3

DB_PATH = "catalog.db"
SOURCE_SNAPSHOT_PATH = "snapshots/source_snapshot.json"


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


def load_source_snapshot_into_sqlite(conn):
    with open(SOURCE_SNAPSHOT_PATH, "r", encoding="utf-8") as f:
        snapshot_objects = json.load(f)

    insert_sql = """
    INSERT INTO catalog_objects (id, type, version, name, snapshot_type, snapshot_time)
    VALUES (?, ?, ?, ?, ?, ?)
    """

    rows_to_insert = []
    for obj in snapshot_objects:
        rows_to_insert.append(
            (
                obj.get("id"),
                obj.get("type"),
                obj.get("version"),
                obj.get("name"),
                "SOURCE",
                None,
            )
        )

    cursor = conn.cursor()
    cursor.executemany(insert_sql, rows_to_insert)
    conn.commit()

    print(f"✅ Inserted {len(rows_to_insert)} SOURCE rows into catalog_objects")


if __name__ == "__main__":
    conn = create_connection()

    if conn:
        create_catalog_objects_table(conn)
        load_source_snapshot_into_sqlite(conn)
        conn.close()
        print("✅ Connection closed")
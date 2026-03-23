import sqlite3

# Define database file name
DB_PATH = "catalog.db"

def create_connection():
    try:
        conn = sqlite3.connect(DB_PATH)
        print(f"✅ Connected to SQLite database: {DB_PATH}")
        return conn
    except sqlite3.Error as e:
        print("❌ SQLite connection error:", e)
        return None


if __name__ == "__main__":
    conn = create_connection()

    if conn:
        conn.close()
        print("✅ Connection closed")
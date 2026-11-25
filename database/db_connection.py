import sqlite3
import os

# Database file path (Project main folder lo 'pricetrack.db' create avuthundi)
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "pricetrack.db")

def get_connection():
    """SQLite database ki connect avvadaniki"""
    conn = sqlite3.connect(DB_PATH)
    # Foreign keys (ON DELETE CASCADE) work avvalante SQLite lo idi compulsory ON cheyali
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def initialize_database():
    """Tables lekapothe automatic ga create chesthundi"""
    conn = get_connection()
    cursor = conn.cursor()

    # 1. Products Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            category TEXT NOT NULL,
            base_unit TEXT NOT NULL
        )
    """)

    # 2. Purchases Table (ON DELETE CASCADE valla product delete chesthe history kuda delete avuthundi)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS purchases (
            purchase_id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            shop_name TEXT NOT NULL,
            total_price REAL NOT NULL,
            quantity REAL NOT NULL,
            unit TEXT NOT NULL,
            normalized_price REAL NOT NULL,
            purchase_date TEXT NOT NULL,
            FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE
        )
    """)

    conn.commit()
    conn.close()
    print(f"Database initialized successfully at: {DB_PATH}")

# Direct ga ee file run chesthe DB create avuthundi
if __name__ == "__main__":
    initialize_database()
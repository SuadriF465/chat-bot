import sqlite3

DB_NAME = "bot_database.db"

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS weather_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                username TEXT,
                city TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_settings (
                user_id INTEGER PRIMARY KEY,
                favorite_city TEXT
            )
        """)
        conn.commit()

def log_weather_request(user_id, username, city):

    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO weather_history (user_id, username, city) VALUES (?, ?, ?)",
            (user_id, username, city)
        )
        conn.commit()

def set_favorite_city(user_id, city):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO user_settings (user_id, favorite_city) VALUES (?, ?) "
            "ON CONFLICT(user_id) DO UPDATE SET favorite_city=excluded.favorite_city",
            (user_id, city)
        )
        conn.commit()

def get_favorite_city(user_id):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT favorite_city FROM user_settings WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        return row[0] if row else None
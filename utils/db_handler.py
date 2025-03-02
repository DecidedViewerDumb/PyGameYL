import sqlite3
from datetime import datetime
from pathlib import Path


class DBHandler:
    def __init__(self, db_name="records.db"):
        self.db_path = Path(__file__).parent.parent / db_name
        self.initialize_db()

    def initialize_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS records (
                    id INTEGER PRIMARY KEY,
                    player_name TEXT,
                    score INTEGER,
                    start_time DATETIME,
                    end_time DATETIME,
                    duration INTEGER GENERATED ALWAYS AS (
                        strftime('%s', end_time) - strftime('%s', start_time)
                    ) STORED
                )
            ''')
            conn.commit()

    def save_record(self, player_name, score, start_time, end_time):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO records (player_name, score, start_time, end_time)
                VALUES (?, ?, ?, ?)
            ''', (player_name, score, start_time.isoformat(), end_time.isoformat()))
            conn.commit()

    def get_records(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT player_name, end_time, score 
                FROM records 
                ORDER BY score DESC 
                LIMIT 10
            ''')
            return cursor.fetchall()


if __name__ == "__main__":
    db = DBHandler()
    test_time = datetime.now()
    db.save_record("ТестовыйИгрок", 1500, test_time, test_time)
    print(db.get_records())

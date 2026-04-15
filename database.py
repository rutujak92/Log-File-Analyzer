import sqlite3

class Database:
    def __init__(self, db_name="my_database.db"):
        self.db_name = db_name
        # self.create_database()

    def create_database(self):
        with sqlite3.connect(self.db_name) as connection:
            cursor = connection.cursor()
            cursor.execute('''CREATE TABLE log_entries (
        id            INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp     TEXT    NOT NULL,
        level         TEXT    NOT NULL,
        code          TEXT    NOT NULL,
        message       TEXT    NOT NULL,
        inserted_at   TEXT    NOT NULL DEFAULT (datetime('now'))
    )''')
        
    def insert_log_entry(self, timestamp, level, code, message):
        with sqlite3.connect(self.db_name) as connection:
            cursor = connection.cursor()
            timestamp_hour = timestamp[:13]  # Extract the hour part (YYYY-MM-DD HH)
            cursor.execute('''INSERT INTO log_entries (timestamp, level, code, message)
                              VALUES (?, ?, ?, ?)''',
                           (timestamp, level, code, message))

    def query_log_entries(self,query="SELECT * FROM log_entries"):
        with sqlite3.connect(self.db_name) as connection:
            cursor = connection.cursor()
            cursor.execute(query)
            return cursor.fetchall()

import sqlite3

class Database:
    def __init__(self, db_name="my_database.db"):
        self.db_name = db_name



    def insert_log_entry(self, timestamp, level, code, message, hour, source_file):
        with sqlite3.connect(self.db_name) as connection:
            cursor = connection.cursor()
            timestamp_hour = timestamp[:13]  # Extract the hour part (YYYY-MM-DD HH)
            cursor.execute('''INSERT INTO log_entries (timestamp, level, code, message,hour,source_file)
                              VALUES (?, ?, ?, ?, ?, ?)''',
                           (timestamp, level, code, message, timestamp_hour, source_file))
            connection.commit()

    def query_log_entries(self,query="SELECT * FROM log_entries"):
        with sqlite3.connect(self.db_name) as connection:
            cursor = connection.cursor()
            cursor.execute(query)
            return cursor.fetchall()

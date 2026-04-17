import sqlite3

def init_database(db_name="my_database.db", schema_file="schema.sql"):
    with sqlite3.connect(db_name) as connection:
        with open(schema_file, 'r') as f:
            schema = f.read()
        try:
            connection.executescript(schema)
            print(f"Database initialized: {db_name}")
        except sqlite3.Error as e:
            print(f"An error occurred while initializing the database: {e}")

if __name__ == "__main__":
    init_database()
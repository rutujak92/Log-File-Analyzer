import pytest
import os
import tempfile
import sqlite3
from database import Database


class TestDatabaseInitialization:
    """Test cases for Database initialization"""

    def test_database_init_default_name(self):
        """Test database initialization with default name"""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = os.path.join(tmpdir, "my_database.db")
            db = Database(db_path)
            assert db.db_name == db_path

    def test_database_init_custom_name(self):
        """Test database initialization with custom database name"""
        with tempfile.TemporaryDirectory() as tmpdir:
            custom_db = os.path.join(tmpdir, "custom_test.db")
            db = Database(custom_db)
            assert db.db_name == custom_db


class TestCreateDatabase:
    """Test cases for database creation"""

    def test_create_database_creates_file(self):
        """Test that create_database creates a database file"""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = os.path.join(tmpdir, "test.db")
            db = Database(db_path)
            db.create_database()
            assert os.path.exists(db_path)

    def test_create_database_creates_table(self):
        """Test that create_database creates the log_entries table"""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = os.path.join(tmpdir, "test.db")
            db = Database(db_path)
            db.create_database()

            with sqlite3.connect(db_path) as connection:
                cursor = connection.cursor()
                cursor.execute(
                    "SELECT name FROM sqlite_master WHERE type='table' AND name='log_entries'"
                )
                result = cursor.fetchone()
                assert result is not None
                assert result[0] == "log_entries"

    def test_create_database_table_structure(self):
        """Test that the log_entries table has the correct columns"""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = os.path.join(tmpdir, "test.db")
            db = Database(db_path)
            db.create_database()

            with sqlite3.connect(db_path) as connection:
                cursor = connection.cursor()
                cursor.execute("PRAGMA table_info(log_entries)")
                columns = cursor.fetchall()

                column_names = [col[1] for col in columns]
                assert "id" in column_names
                assert "timestamp" in column_names
                assert "level" in column_names
                assert "code" in column_names
                assert "message" in column_names
                assert "inserted_at" in column_names


class TestInsertLogEntry:
    """Test cases for inserting log entries"""

    @pytest.fixture
    def setup_db(self):
        """Setup a test database with table created"""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = os.path.join(tmpdir, "test.db")
            db = Database(db_path)
            db.create_database()
            yield db, db_path

    def test_insert_single_log_entry(self, setup_db):
        """Test inserting a single log entry"""
        db, db_path = setup_db
        db.insert_log_entry(
            "[2023-08-01 12:00:00]", "INFO", "app.module", "Test message"
        )

        result = db.query_log_entries()
        assert len(result) == 1
        assert result[0][1] == "[2023-08-01 12:00:00]"
        assert result[0][2] == "INFO"
        assert result[0][3] == "app.module"
        assert result[0][4] == "Test message"

    def test_insert_multiple_log_entries(self, setup_db):
        """Test inserting multiple log entries"""
        db, db_path = setup_db
        db.insert_log_entry(
            "[2023-08-01 12:00:00]", "INFO", "app", "First message"
        )
        db.insert_log_entry(
            "[2023-08-01 12:00:01]", "ERROR", "database", "Second message"
        )
        db.insert_log_entry(
            "[2023-08-01 12:00:02]", "WARNING", "auth", "Third message"
        )

        result = db.query_log_entries()
        assert len(result) == 3

    def test_insert_log_entry_different_levels(self, setup_db):
        """Test inserting log entries with different log levels"""
        db, db_path = setup_db
        levels = ["INFO", "ERROR", "WARNING", "DEBUG"]

        for i, level in enumerate(levels):
            db.insert_log_entry(
                f"[2023-08-01 12:00:{i:02d}]", level, "app", f"Message {i}"
            )

        result = db.query_log_entries()
        assert len(result) == 4

        for i, level in enumerate(levels):
            assert result[i][2] == level

    def test_insert_log_entry_with_special_characters(self, setup_db):
        """Test inserting log entry with special characters in message"""
        db, db_path = setup_db
        message = "Error: [500] Connection failed (retry: 3)"
        db.insert_log_entry(
            "[2023-08-01 12:00:00]", "ERROR", "app", message
        )

        result = db.query_log_entries()
        assert result[0][4] == message

    def test_insert_log_entry_with_quotes_in_message(self, setup_db):
        """Test inserting log entry with quotes in message"""
        db, db_path = setup_db
        message = "User 'admin' logged in with message: \"Success\""
        db.insert_log_entry(
            "[2023-08-01 12:00:00]", "INFO", "auth", message
        )

        result = db.query_log_entries()
        assert result[0][4] == message


class TestQueryLogEntries:
    """Test cases for querying log entries"""

    @pytest.fixture
    def setup_db_with_data(self):
        """Setup a test database with sample data"""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = os.path.join(tmpdir, "test.db")
            db = Database(db_path)
            db.create_database()

            # Insert sample data
            db.insert_log_entry(
                "[2023-08-01 12:00:00]", "INFO", "app", "Message 1"
            )
            db.insert_log_entry(
                "[2023-08-01 12:00:01]", "ERROR", "database", "Message 2"
            )
            db.insert_log_entry(
                "[2023-08-01 12:00:02]", "WARNING", "auth", "Message 3"
            )

            yield db

    def test_query_all_entries(self, setup_db_with_data):
        """Test querying all log entries"""
        db = setup_db_with_data
        result = db.query_log_entries()
        assert len(result) == 3

    def test_query_entries_returns_list(self, setup_db_with_data):
        """Test that query_log_entries returns a list"""
        db = setup_db_with_data
        result = db.query_log_entries()
        assert isinstance(result, list)

    def test_query_entries_with_where_clause(self, setup_db_with_data):
        """Test querying log entries with WHERE clause"""
        db = setup_db_with_data
        result = db.query_log_entries(
            "SELECT * FROM log_entries WHERE level='ERROR'"
        )
        assert len(result) == 1
        assert result[0][2] == "ERROR"

    def test_query_entries_with_order_by(self, setup_db_with_data):
        """Test querying log entries with ORDER BY"""
        db = setup_db_with_data
        result = db.query_log_entries(
            "SELECT * FROM log_entries ORDER BY timestamp DESC"
        )
        assert len(result) == 3
        assert "[2023-08-01 12:00:02]" in result[0][1]

    def test_query_entries_with_limit(self, setup_db_with_data):
        """Test querying log entries with LIMIT"""
        db = setup_db_with_data
        result = db.query_log_entries(
            "SELECT * FROM log_entries LIMIT 2"
        )
        assert len(result) == 2

    def test_query_entries_empty_result(self, setup_db_with_data):
        """Test querying with condition that returns no results"""
        db = setup_db_with_data
        result = db.query_log_entries(
            "SELECT * FROM log_entries WHERE level='CRITICAL'"
        )
        assert len(result) == 0
        assert isinstance(result, list)

    def test_query_specific_columns(self, setup_db_with_data):
        """Test querying specific columns"""
        db = setup_db_with_data
        result = db.query_log_entries(
            "SELECT level, message FROM log_entries WHERE level='INFO'"
        )
        assert len(result) == 1
        assert result[0][0] == "INFO"
        assert result[0][1] == "Message 1"


class TestIntegration:
    """Integration tests for Database class"""

    def test_full_workflow(self):
        """Test complete workflow: create DB, insert, query"""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = os.path.join(tmpdir, "workflow.db")
            db = Database(db_path)
            db.create_database()

            # Insert multiple entries
            db.insert_log_entry(
                "[2023-08-01 12:00:00]", "INFO", "app", "Application started"
            )
            db.insert_log_entry(
                "[2023-08-01 12:00:01]", "ERROR", "db", "Connection failed"
            )

            # Query all
            all_entries = db.query_log_entries()
            assert len(all_entries) == 2

            # Query specific level
            errors = db.query_log_entries(
                "SELECT * FROM log_entries WHERE level='ERROR'"
            )
            assert len(errors) == 1

    def test_database_persistence(self):
        """Test that data persists across connections"""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = os.path.join(tmpdir, "persist.db")

            # Create and insert
            db1 = Database(db_path)
            db1.create_database()
            db1.insert_log_entry(
                "[2023-08-01 12:00:00]", "INFO", "app", "Persisted message"
            )

            # Create new instance and query
            db2 = Database(db_path)
            result = db2.query_log_entries()
            assert len(result) == 1
            assert result[0][4] == "Persisted message"

    def test_insert_and_query_various_log_levels(self):
        """Test inserting and querying various log levels"""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = os.path.join(tmpdir, "levels.db")
            db = Database(db_path)
            db.create_database()

            log_data = [
                ("INFO", "app", "Info message"),
                ("WARNING", "module1", "Warning message"),
                ("ERROR", "module2", "Error message"),
                ("DEBUG", "module3", "Debug message"),
            ]

            for level, code, message in log_data:
                db.insert_log_entry(
                    "[2023-08-01 12:00:00]", level, code, message
                )

            # Verify all were inserted
            all_entries = db.query_log_entries()
            assert len(all_entries) == 4

            # Verify each level can be queried
            for level, _, _ in log_data:
                result = db.query_log_entries(
                    f"SELECT * FROM log_entries WHERE level='{level}'"
                )
                assert len(result) == 1
                assert result[0][2] == level

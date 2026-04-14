import pytest
import os
import tempfile
from main import read_log_file, parse_line


class TestParseLine:
    """Test cases for parse_line function"""

    def test_parse_valid_info_log(self):
        """Test parsing a valid INFO log line"""
        line = "[2023-08-01 12:00:00] INFO (app.module): This is a log message."
        result = parse_line(line)
        assert "Timestamp: [2023-08-01 12:00:00]" in result
        assert "Log Level: INFO" in result
        assert "Module: app.module" in result
        assert "Message: This is a log message." in result

    def test_parse_valid_error_log(self):
        """Test parsing a valid ERROR log line"""
        line = "[2023-08-01 12:30:45] ERROR (database): Connection failed."
        result = parse_line(line)
        assert "Timestamp: [2023-08-01 12:30:45]" in result
        assert "Log Level: ERROR" in result
        assert "Module: database" in result
        assert "Message: Connection failed." in result

    def test_parse_valid_warning_log(self):
        """Test parsing a valid WARNING log line"""
        line = "[2023-08-01 15:20:10] WARNING (auth): Invalid credentials."
        result = parse_line(line)
        assert "Log Level: WARNING" in result
        assert "Module: auth" in result

    def test_parse_valid_debug_log(self):
        """Test parsing a valid DEBUG log line"""
        line = "[2023-08-01 09:15:30] DEBUG (config): Loading configuration."
        result = parse_line(line)
        assert "Log Level: DEBUG" in result
        assert "Module: config" in result

    def test_parse_invalid_format(self):
        """Test parsing a line that doesn't match the expected format"""
        line = "This is not a valid log line"
        result = parse_line(line)
        assert result == "Line does not match the expected format."

    def test_parse_missing_timestamp(self):
        """Test parsing a line with missing timestamp"""
        line = "INFO (app.module): This is a log message."
        result = parse_line(line)
        assert result == "Line does not match the expected format."

    def test_parse_malformed_timestamp(self):
        """Test parsing a line with malformed timestamp"""
        line = "[2023-08-01] INFO (app.module): This is a log message."
        result = parse_line(line)
        assert result == "Line does not match the expected format."

    def test_parse_empty_line(self):
        """Test parsing an empty line"""
        line = ""
        result = parse_line(line)
        assert result == "Line does not match the expected format."

    def test_parse_message_with_special_characters(self):
        """Test parsing a message with special characters"""
        line = "[2023-08-01 12:00:00] ERROR (app): Error: [500] Internal error!"
        result = parse_line(line)
        assert "Message:" in result
        assert "[500]" in result

    def test_parse_message_with_parentheses(self):
        """Test parsing a message containing parentheses"""
        line = "[2023-08-01 12:00:00] INFO (app): User (admin) logged in successfully."
        result = parse_line(line)
        assert "User (admin) logged in successfully." in result


class TestReadLogFile:
    """Test cases for read_log_file function"""

    def test_read_valid_log_file(self):
        """Test reading a valid log file"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.log') as f:
            f.write("[2023-08-01 12:00:00] INFO (app): Start\n")
            f.write("[2023-08-01 12:00:01] ERROR (app): End\n")
            temp_file = f.name

        try:
            result = read_log_file(temp_file)
            assert isinstance(result, list)
            assert len(result) == 2
            assert "[2023-08-01 12:00:00]" in result[0]
            assert "[2023-08-01 12:00:01]" in result[1]
        finally:
            os.unlink(temp_file)

    def test_read_empty_log_file(self):
        """Test reading an empty log file"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.log') as f:
            temp_file = f.name

        try:
            result = read_log_file(temp_file)
            assert isinstance(result, list)
            assert len(result) == 0
        finally:
            os.unlink(temp_file)

    def test_read_single_line_log_file(self):
        """Test reading a log file with a single line"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.log') as f:
            f.write("[2023-08-01 12:00:00] INFO (app): Single line")
            temp_file = f.name

        try:
            result = read_log_file(temp_file)
            assert len(result) == 1
            assert "[2023-08-01 12:00:00]" in result[0]
        finally:
            os.unlink(temp_file)

    def test_read_nonexistent_file(self):
        """Test reading a file that doesn't exist"""
        with pytest.raises(FileNotFoundError):
            read_log_file("/nonexistent/path/to/file.log")

    def test_read_file_with_multiline_messages(self):
        """Test reading a file with lines containing various content"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.log') as f:
            f.write("[2023-08-01 12:00:00] INFO (app): Normal message\n")
            f.write("[2023-08-01 12:00:01] WARNING (app): Warning message\n")
            f.write("Invalid log line without proper format\n")
            temp_file = f.name

        try:
            result = read_log_file(temp_file)
            assert len(result) == 3
        finally:
            os.unlink(temp_file)

    def test_read_file_returns_list(self):
        """Test that read_log_file always returns a list"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.log') as f:
            f.write("[2023-08-01 12:00:00] INFO (app): Test\n")
            temp_file = f.name

        try:
            result = read_log_file(temp_file)
            assert isinstance(result, list)
        finally:
            os.unlink(temp_file)


class TestIntegration:
    """Integration tests for the log parser"""

    def test_parse_all_lines_from_file(self):
        """Test parsing all lines from a sample log file"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.log') as f:
            f.write("[2023-08-01 12:00:00] INFO (app): Start\n")
            f.write("[2023-08-01 12:00:01] ERROR (db): Connection failed\n")
            temp_file = f.name

        try:
            lines = read_log_file(temp_file)
            parsed_results = [parse_line(line) for line in lines]
            
            assert len(parsed_results) == 2
            assert "ERROR" in parsed_results[1]
            assert "Connection failed" in parsed_results[1]
        finally:
            os.unlink(temp_file)

    def test_parse_mixed_valid_and_invalid_lines(self):
        """Test parsing a file with mixed valid and invalid log lines"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.log') as f:
            f.write("[2023-08-01 12:00:00] INFO (app): Valid log\n")
            f.write("This is an invalid line\n")
            f.write("[2023-08-01 12:00:02] WARNING (app): Another valid log\n")
            temp_file = f.name

        try:
            lines = read_log_file(temp_file)
            parsed_results = [parse_line(line) for line in lines]
            
            assert "does not match" in parsed_results[1]
            assert "INFO" in parsed_results[0]
            assert "WARNING" in parsed_results[2]
        finally:
            os.unlink(temp_file)
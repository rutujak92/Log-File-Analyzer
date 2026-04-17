-- Create log_entries table
CREATE TABLE IF NOT EXISTS log_entries (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp     TEXT    NOT NULL,
    level         TEXT    NOT NULL,
    code          TEXT    NOT NULL,
    message       TEXT    NOT NULL,
    hour          INTEGER NOT NULL,
    source_file   TEXT    NOT NULL,
    inserted_at   TEXT    NOT NULL DEFAULT (datetime('now'))
);

-- Optional: Create indexes for faster queries
CREATE INDEX IF NOT EXISTS idx_level ON log_entries(level);
CREATE INDEX IF NOT EXISTS idx_timestamp ON log_entries(timestamp);
CREATE INDEX IF NOT EXISTS idx_code ON log_entries(code);


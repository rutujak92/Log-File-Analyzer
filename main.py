import re
import csv
import time
from database import Database
pattern = r"(\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\]) (\w+) \((.*?)\): (.*)"

def read_log_file(file_path):
    with open(file_path, "r") as f:
        lines= []
        for line in f.readlines():
            lines.append(line)
    return lines

def parse_line(line):
    split_logs= re.match(pattern, line)
    if split_logs:
        
        return list(split_logs.groups())
    else:
        return None
def main():
    file_path = "data/app.log"
    log_lines = read_log_file(file_path)
    db = Database()

    with open(f"output/output{time.time()}.csv", "a") as csvfile:
        for line in log_lines:
                parsed_line = parse_line(line)
                if parsed_line is not None:

                    db.insert_log_entry(*parsed_line)
                    writer = csv.writer(csvfile)
                    writer.writerow(parsed_line)
    print(db.query_log_entries("SELECT * FROM log_entries where level='ERROR'"))
if __name__ == "__main__":    main()

        
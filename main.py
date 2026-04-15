import re
import csv
import time
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
    with open(f"output/output{time.time()}.csv", "a") as csvfile:
        for line in log_lines:
                parsed_line = parse_line(line)
                if parsed_line is not None:
                    writer = csv.writer(csvfile)
                    writer.writerow(parsed_line)
if __name__ == "__main__":    main()

        
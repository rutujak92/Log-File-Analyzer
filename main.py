import re
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
        timestamp, log_level, module, message = split_logs.groups()
        return f"Timestamp: {timestamp}, Log Level: {log_level}, Module: {module}, Message: {message}"
    else:
        return "Line does not match the expected format."
def main():
    file_path = "data/app.log"
    log_lines = read_log_file(file_path)
    for line in log_lines:
        parsed_line = parse_line(line)
        print(parsed_line)
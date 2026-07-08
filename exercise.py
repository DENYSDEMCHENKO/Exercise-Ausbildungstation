import re
from collections import Counter, defaultdict

LOG_PATTERN = re.compile(
    r'(?P<host>\S+) \S+ \S+ \[(?P<timestamp>[^\]]+)\] '
    r'"(?P<request>[^"]*)" (?P<status>\d+) (?P<bytes>\S+)'
)


def parse_line(line):
    match = LOG_PATTERN.match(line)
    if not match:
        return None
    return match.groupdict()


def status_to_category(status):
    return f"{status[0]}xx"


def parse_logfile(path):
    host_counter = Counter()
    status_by_day = defaultdict(Counter)

    with open(path, "r", encoding="utf-8", errors="ignore") as logfile:
        for line in logfile:
            data = parse_line(line)
            if not data:
                continue
            host_counter[data["host"]] += 1
            day = data["timestamp"].split(":")[0]
            category = status_to_category(data["status"])
            status_by_day[day][category] += 1

    return host_counter, status_by_day


if __name__ == "__main__":
    host_counter, status_by_day = parse_logfile("logs.txt")
    print("Top 10 Hosts/IPs by total requests")
    print("-" * 35)
    for host, count in host_counter.most_common(10):
        print(f"{host:20} {count}")

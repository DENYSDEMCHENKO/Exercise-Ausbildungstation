import re
from collections import Counter

LOG_PATTERN = re.compile(
    r'(?P<host>\S+) \S+ \S+ \[(?P<timestamp>[^\]]+)\] '
    r'"(?P<request>[^"]*)" (?P<status>\d+) (?P<bytes>\S+)'
)

host_counter = Counter()

with open("logs.txt", "r", encoding="utf-8", errors="ignore") as logfile:
    for line in logfile:
        match = LOG_PATTERN.match(line)
        if not match:
            # Skip corrupted or malformed lines
            continue

        host = match.group("host")
        host_counter[host] += 1

print("Top 10 Hosts/IPs by total requests")
print("-" * 35)

for host, count in host_counter.most_common(10):
    print(f"{host:20} {count}")
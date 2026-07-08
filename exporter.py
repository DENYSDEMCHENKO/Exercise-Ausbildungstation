import time
import threading
from prometheus_client import start_http_server, Gauge
from exercise import parse_logfile
from ram_cpu_usage import get_system_metrics

LOG_FILE_PATH = "logs.txt"
UPDATE_INTERVAL_SECONDS = 15
HTTP_PORT = 8000

top_hosts_gauge = Gauge(
    "top_hosts_requests_total", "Requests per host (top 10)", ["host"]
)
status_by_day_gauge = Gauge(
    "http_requests_by_day_total", "HTTP requests by status category and day",
    ["day", "code"]
)
cpu_gauge = Gauge("host_cpu_usage_percent", "Current CPU usage percent")
ram_gauge = Gauge("host_ram_usage_percent", "Current RAM usage percent")


def refresh_metrics_once(host_counter, status_by_day):
    top_hosts_gauge.clear()
    for host, count in host_counter.most_common(10):
        top_hosts_gauge.labels(host=host).set(count)

    status_by_day_gauge.clear()
    for day, categories in status_by_day.items():
        for category, count in categories.items():
            status_by_day_gauge.labels(day=day, code=category).set(count)

    system_metrics = get_system_metrics()
    cpu_gauge.set(system_metrics["cpu_percent"])
    ram_gauge.set(system_metrics["ram_percent"])


def update_metrics_loop():
    host_counter, status_by_day = parse_logfile(LOG_FILE_PATH)

    while True:
        refresh_metrics_once(host_counter, status_by_day)
        print("Metrics updated")
        time.sleep(UPDATE_INTERVAL_SECONDS)


def main():
    start_http_server(HTTP_PORT)
    print(f"Serving metrics on :{HTTP_PORT}/metrics")

    updater_thread = threading.Thread(target=update_metrics_loop, daemon=True)
    updater_thread.start()

    while True:
        time.sleep(1)


if __name__ == "__main__":
    main()

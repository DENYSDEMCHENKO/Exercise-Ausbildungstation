from collections import Counter, defaultdict

import exporter


def _get_gauge_value(gauge, **labels):
    child = gauge.labels(**labels) if labels else gauge
    return child._value.get()


def test_refresh_metrics_once_sets_top_hosts(monkeypatch):
    host_counter = Counter({"1.2.3.4": 5, "5.6.7.8": 3})
    status_by_day = defaultdict(Counter)

    monkeypatch.setattr(
        exporter, "get_system_metrics",
        lambda: {"cpu_percent": 10.0, "ram_percent": 20.0}
    )

    exporter.refresh_metrics_once(host_counter, status_by_day)

    assert _get_gauge_value(exporter.top_hosts_gauge, host="1.2.3.4") == 5
    assert _get_gauge_value(exporter.top_hosts_gauge, host="5.6.7.8") == 3


def test_refresh_metrics_once_sets_status_by_day(monkeypatch):
    host_counter = Counter()
    status_by_day = defaultdict(Counter)
    status_by_day["01/Jul/1995"]["2xx"] = 10
    status_by_day["01/Jul/1995"]["4xx"] = 2

    monkeypatch.setattr(
        exporter, "get_system_metrics",
        lambda: {"cpu_percent": 0.0, "ram_percent": 0.0}
    )

    exporter.refresh_metrics_once(host_counter, status_by_day)

    assert _get_gauge_value(
        exporter.status_by_day_gauge, day="01/Jul/1995", code="2xx"
    ) == 10
    assert _get_gauge_value(
        exporter.status_by_day_gauge, day="01/Jul/1995", code="4xx"
    ) == 2


def test_refresh_metrics_once_sets_cpu_and_ram(monkeypatch):
    monkeypatch.setattr(
        exporter, "get_system_metrics",
        lambda: {"cpu_percent": 33.3, "ram_percent": 66.6}
    )

    exporter.refresh_metrics_once(Counter(), defaultdict(Counter))

    assert _get_gauge_value(exporter.cpu_gauge) == 33.3
    assert _get_gauge_value(exporter.ram_gauge) == 66.6


def test_refresh_metrics_once_clears_stale_hosts(monkeypatch):
    monkeypatch.setattr(
        exporter, "get_system_metrics",
        lambda: {"cpu_percent": 0.0, "ram_percent": 0.0}
    )

    exporter.refresh_metrics_once(Counter({"old.host": 100}), defaultdict(Counter))
    assert _get_gauge_value(exporter.top_hosts_gauge, host="old.host") == 100

    exporter.refresh_metrics_once(Counter({"new.host": 50}), defaultdict(Counter))

    samples = list(exporter.top_hosts_gauge.collect())[0].samples
    hosts_present = {s.labels["host"] for s in samples}
    assert "old.host" not in hosts_present
    assert "new.host" in hosts_present

import ram_cpu_usage


def test_get_system_metrics_returns_expected_keys(monkeypatch):
    monkeypatch.setattr(ram_cpu_usage.psutil, "cpu_percent", lambda interval=None: 42.0)

    class FakeMemory:
        percent = 55.5

    monkeypatch.setattr(ram_cpu_usage.psutil, "virtual_memory", lambda: FakeMemory())

    result = ram_cpu_usage.get_system_metrics()

    assert result == {"cpu_percent": 42.0, "ram_percent": 55.5}


def test_get_system_metrics_returns_numeric_types(monkeypatch):
    monkeypatch.setattr(ram_cpu_usage.psutil, "cpu_percent", lambda interval=None: 10)

    class FakeMemory:
        percent = 20

    monkeypatch.setattr(ram_cpu_usage.psutil, "virtual_memory", lambda: FakeMemory())

    result = ram_cpu_usage.get_system_metrics()

    assert isinstance(result["cpu_percent"], (int, float))
    assert isinstance(result["ram_percent"], (int, float))

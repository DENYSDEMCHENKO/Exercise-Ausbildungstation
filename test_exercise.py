from collections import Counter

from exercise import parse_line, status_to_category, parse_logfile

def test_parse_line_valid_extracts_all_fields():
    line = (
        '199.72.81.55 - - [01/Jul/1995:00:00:01 -0400] '
        '"GET /history/apollo/ HTTP/1.0" 200 6245\n'
    )
    result = parse_line(line)

    assert result is not None
    assert result["host"] == "199.72.81.55"
    assert result["timestamp"] == "01/Jul/1995:00:00:01 -0400"
    assert result["request"] == "GET /history/apollo/ HTTP/1.0"
    assert result["status"] == "200"
    assert result["bytes"] == "6245"


def test_parse_line_with_hostname_instead_of_ip():
    line = (
        'unicomp6.unicomp.net - - [01/Jul/1995:00:00:06 -0400] '
        '"GET /shuttle/countdown/ HTTP/1.0" 200 3985\n'
    )
    result = parse_line(line)

    assert result is not None
    assert result["host"] == "unicomp6.unicomp.net"


def test_parse_line_with_zero_bytes():
    line = (
        'burger.letters.com - - [01/Jul/1995:00:00:11 -0400] '
        '"GET /shuttle/countdown/liftoff.html HTTP/1.0" 304 0\n'
    )
    result = parse_line(line)

    assert result is not None
    assert result["status"] == "304"
    assert result["bytes"] == "0"


def test_parse_line_invalid_returns_none():
    assert parse_line("это не строка лога, просто мусор\n") is None


def test_parse_line_empty_string_returns_none():
    assert parse_line("") is None



def test_status_to_category_2xx():
    assert status_to_category("200") == "2xx"


def test_status_to_category_3xx():
    assert status_to_category("304") == "3xx"


def test_status_to_category_4xx():
    assert status_to_category("404") == "4xx"


def test_status_to_category_5xx():
    assert status_to_category("500") == "5xx"



def test_parse_logfile_counts_hosts_correctly(tmp_path):
    log_content = (
        '199.72.81.55 - - [01/Jul/1995:00:00:01 -0400] "GET /a HTTP/1.0" 200 100\n'
        '199.72.81.55 - - [01/Jul/1995:00:00:02 -0400] "GET /b HTTP/1.0" 404 0\n'
        'other.host - - [02/Jul/1995:00:00:03 -0400] "GET /c HTTP/1.0" 200 50\n'
    )
    log_file = tmp_path / "test_log.txt"
    log_file.write_text(log_content, encoding="utf-8")

    host_counter, _ = parse_logfile(str(log_file))

    assert host_counter["199.72.81.55"] == 2
    assert host_counter["other.host"] == 1
    assert isinstance(host_counter, Counter)


def test_parse_logfile_groups_status_by_day(tmp_path):
    log_content = (
        '199.72.81.55 - - [01/Jul/1995:00:00:01 -0400] "GET /a HTTP/1.0" 200 100\n'
        '199.72.81.55 - - [01/Jul/1995:00:00:02 -0400] "GET /b HTTP/1.0" 404 0\n'
        'other.host - - [02/Jul/1995:00:00:03 -0400] "GET /c HTTP/1.0" 200 50\n'
    )
    log_file = tmp_path / "test_log.txt"
    log_file.write_text(log_content, encoding="utf-8")

    _, status_by_day = parse_logfile(str(log_file))

    assert status_by_day["01/Jul/1995"]["2xx"] == 1
    assert status_by_day["01/Jul/1995"]["4xx"] == 1
    assert status_by_day["02/Jul/1995"]["2xx"] == 1
    assert "03/Jul/1995" not in status_by_day


def test_parse_logfile_skips_broken_lines(tmp_path):
    log_content = (
        '199.72.81.55 - - [01/Jul/1995:00:00:01 -0400] "GET /a HTTP/1.0" 200 100\n'
        'это сломанная строка без нужного формата\n'
        'other.host - - [01/Jul/1995:00:00:03 -0400] "GET /c HTTP/1.0" 200 50\n'
    )
    log_file = tmp_path / "test_log.txt"
    log_file.write_text(log_content, encoding="utf-8")

    host_counter, status_by_day = parse_logfile(str(log_file))

    assert sum(host_counter.values()) == 2
    assert status_by_day["01/Jul/1995"]["2xx"] == 2


def test_parse_logfile_empty_file_returns_empty_structures(tmp_path):
    log_file = tmp_path / "empty_log.txt"
    log_file.write_text("", encoding="utf-8")

    host_counter, status_by_day = parse_logfile(str(log_file))

    assert len(host_counter) == 0
    assert len(status_by_day) == 0

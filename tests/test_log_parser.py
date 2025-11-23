from src.log_analyzer.log_parser import LogParser


def test_log_parser_basic_parsing():
    """Test basic log parsing functionality"""
    parser = LogParser()

    test_lines = [
        "2024-01-01 00:00:01 ERROR Database connection failed",
        "2024-01-01 00:00:02 WARNING Slow query detected",
        "2024-01-01 00:00:03 INFO User login successful",
        "2024-01-01 00:00:04 INFO latency=150"
    ]

    events, timeline = parser.parse_lines(test_lines)

    # Check error and warning collection
    assert len(events["ERROR"]) == 1
    assert len(events["WARNING"]) == 1
    assert "Database connection failed" in events["ERROR"][0]

    # Check timeline events
    assert len(timeline) == 4
    assert timeline[0]["event"] == "ERROR"
    assert timeline[1]["event"] == "WARNING"


def test_log_parser_timestamp_extraction():
    """Test timestamp extraction from log lines"""
    parser = LogParser()

    test_line = "2024-01-01 12:34:56 INFO Test message"
    timestamp = parser.extract_timestamp(test_line)

    assert timestamp == "2024-01-01T12:34:56"


def test_log_parser_variable_parsing():
    """Test parsing of key=value pairs"""
    parser = LogParser()

    test_lines = [
        "2024-01-01 00:00:01 INFO latency=150",
        "2024-01-01 00:00:02 INFO memory_usage=75"
    ]

    events, timeline = parser.parse_lines(test_lines)

    # Should capture variables in timeline
    assert len(timeline) == 2
    assert timeline[0]["event"] == "latency"
    assert timeline[0]["value"] == 150
    assert timeline[1]["event"] == "memory_usage"
    assert timeline[1]["value"] == 75
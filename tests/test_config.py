from src.log_analyzer.config import *


def test_config_defaults():
    """Test that configuration has expected defaults"""
    assert CHUNK_SIZE == 5000
    assert QUEUE_MAX_SIZE == 100
    assert POLL_INTERVAL == 0.5
    assert NUM_PROCESSES == 3


def test_config_regex_patterns():
    """Test regex patterns for variable parsing"""
    test_line = "2024-01-01 00:00:01 INFO latency=150 memory_usage=75"

    matches = KEY_VAL_RE.findall(test_line)
    assert len(matches) == 2
    assert ("latency", "150") in matches
    assert ("memory_usage", "75") in matches
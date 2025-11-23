import pytest
import tempfile
import os


@pytest.fixture
def sample_log_file():
    """Fixture to create a temporary sample log file for testing"""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as f:
        # Write sample log data
        lines = [
            "2024-01-01 00:00:01 ERROR Database connection failed",
            "2024-01-01 00:00:02 WARNING Slow query detected",
            "2024-01-01 00:00:03 INFO User login successful",
            "2024-01-01 00:00:04 INFO latency=150",
            "2024-01-01 00:00:05 INFO memory_usage=75"
        ]
        for line in lines:
            f.write(line + '\n')
        temp_path = f.name

    yield temp_path
    # Cleanup
    os.unlink(temp_path)
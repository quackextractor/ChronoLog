import tempfile
import os
from src.log_analyzer.file_chunk_reader import FileChunkReader


def test_file_chunk_reader_basic():
    """Test basic chunk reading functionality"""
    # Create a temporary file with test content
    with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as f:
        for i in range(10):
            f.write(f"2024-01-01 00:00:{i:02d} INFO Test message {i}\n")
        temp_path = f.name

    try:
        reader = FileChunkReader(temp_path, chunk_size=3)
        chunks = list(reader)

        # Should read all chunks (10 lines / 3 per chunk = 4 chunks)
        assert len(chunks) >= 3
        assert sum(len(chunk) for chunk in chunks) == 10
    finally:
        os.unlink(temp_path)


def test_file_chunk_reader_empty_file():
    """Test reading from an empty file"""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as f:
        temp_path = f.name

    try:
        reader = FileChunkReader(temp_path, chunk_size=3)
        chunks = list(reader)
        assert len(chunks) == 0
    finally:
        os.unlink(temp_path)
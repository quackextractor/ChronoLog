import multiprocessing
import os
import time
import json
import hashlib
import pickle

INPUT_FILE_PATH = "../examples/sample.log"
CHUNK_SIZE = 1000
QUEUE_MAX_SIZE = 10
STATE_FILE = "parser_state.json"
SEEN_FILE = "seen_lines.pkl"
POLL_INTERVAL = 0.5

def save_state(position, seen_lines):
    """Persist read position and seen lines safely."""
    tmp_state = STATE_FILE + ".tmp"
    tmp_seen = SEEN_FILE + ".tmp"
    with open(tmp_state, "w") as f:
        json.dump({"position": position}, f)
    with open(tmp_seen, "wb") as f:
        pickle.dump(seen_lines, f)
    os.replace(tmp_state, STATE_FILE)
    os.replace(tmp_seen, SEEN_FILE)

def load_state():
    """Load last read position and seen lines."""
    position = 0
    seen_lines = set()
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            try:
                position = json.load(f).get("position", 0)
            except json.JSONDecodeError:
                position = 0
    if os.path.exists(SEEN_FILE):
        with open(SEEN_FILE, "rb") as f:
            try:
                seen_lines = pickle.load(f)
            except Exception:
                seen_lines = set()
    return position, seen_lines

def parse_lines_worker(lines, queue, stop_flag):
    if stop_flag.is_set():
        return
    local_events = {"ERROR": [], "WARNING": [], "latency": []}
    for line in lines:
        line = line.strip()
        for key in local_events:
            if key in line:
                local_events[key].append(line)
    queue.put(local_events)

def chunked_file_reader(file_path, start_pos=0, chunk_size=CHUNK_SIZE):
    with open(file_path, "r") as f:
        f.seek(start_pos)
        while True:
            chunk = []
            while len(chunk) < chunk_size:
                line = f.readline()
                if not line:
                    break
                chunk.append(line)
            if chunk:
                yield chunk, f.tell()
            else:
                current_size = os.path.getsize(file_path)
                if current_size < f.tell():  # rotation/truncation
                    f.seek(0)
                    yield [], 0
                else:
                    time.sleep(POLL_INTERVAL)

def live_parse(number_of_processes):
    manager = multiprocessing.Manager()
    queue = manager.Queue(maxsize=QUEUE_MAX_SIZE)
    stop_flag = multiprocessing.Event()
    pool = multiprocessing.Pool(number_of_processes)

    merged = {"ERROR": [], "WARNING": [], "latency": []}
    last_position, seen_lines = load_state()

    try:
        for chunk, new_pos in chunked_file_reader(INPUT_FILE_PATH, start_pos=last_position):
            if chunk:
                pool.apply_async(parse_lines_worker, args=(chunk, queue, stop_flag))
                last_position = new_pos

            while not queue.empty():
                result = queue.get()
                for key in merged:
                    for line in result[key]:
                        line_hash = hashlib.md5(line.encode()).hexdigest()
                        if line_hash not in seen_lines:
                            seen_lines.add(line_hash)
                            merged[key].append(line)

            # Periodically save state
            save_state(last_position, seen_lines)

    except KeyboardInterrupt:
        stop_flag.set()
    finally:
        pool.close()
        pool.join()

        while not queue.empty():
            result = queue.get()
            for key in merged:
                for line in result[key]:
                    line_hash = hashlib.md5(line.encode()).hexdigest()
                    if line_hash not in seen_lines:
                        seen_lines.add(line_hash)
                        merged[key].append(line)

        save_state(last_position, seen_lines)

    return merged

if __name__ == "__main__":
    result = live_parse(3)
    print(result)
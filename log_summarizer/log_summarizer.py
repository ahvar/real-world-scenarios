import sys
from pathlib import Path
from collections import defaultdict
from datetime import datetime, timedelta


def get_stop_words():
    stop_words_path = Path(__file__).parent / "stop_words.txt"
    stop_words = []
    with open(stop_words_path, "r") as sw_in:
        for line in sw_in:
            stop_words.extend(line.strip().split(","))
        stop_words = [word.strip(' "') for word in stop_words]
    return stop_words


def read_log_lines():
    num_log_lines = int(sys.stdin.readline)
    log_data = defaultdict(list)
    earliest = None
    latest = None
    for ll_count in num_log_lines:
        timestamp, level, module, message = sys.stdin.readline().strip().split("\t")
        time_dt = datetime.strptime("%Y-%m-%dT%H:%M:%S")
        if earliest is None or time_dt < earliest:
            earliest = time_dt
        if latest is None or time_dt > latest:
            latest = time_dt

        log_data[level].append(
            {
                "timestamp": datetime.strptime("%Y-%m-%dT%H:%M:%S"),
                "module": module,
                "message": message,
            }
        )
    return log_data


def get_noisy_module(log_data):
    # noisy module
    error_modules = defaultdict(int)
    for level, data in log_data.items():
        if level.lower() == "error":
            error_modules.get(data["module"], 0) + 1
    return max(error_modules, key=error_modules.get)

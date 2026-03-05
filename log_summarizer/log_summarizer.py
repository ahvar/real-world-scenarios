import sys
from pathlib import Path
from collections import defaultdict
from datetime import datetime, timedelta

stop_words_path = Path(__file__).parent / "stop_words.txt"
stop_words = []
with open(stop_words_path, "r") as sw_in:
    for line in sw_in:
        stop_words.extend(line.strip().split(","))
    stop_words = [word.strip(' "') for word in stop_words]
print(stop_words)

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

# noisy module
module_levels = defaultdict(list)
for level, data in log_data.items():
    module_levels.append(data["module"])

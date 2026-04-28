import sys
from collections import Counter
from collections import defaultdict
from datetime import datetime

total_lines = int(sys.stdin.readline())
levels = defaultdict(Counter)
messages = []
earliest = None
latest = None
for line in total_lines:
    timestamp, level, module, message = sys.stdin.readline().strip().split("\t")
    levels[module][level.lower()] += 1
    date_dt = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S")
    messages.append(message)
    if not earliest and not latest:
        date_dt = earliest
        date_dt = latest
    else:
        if date_dt < earliest:
            earliest = date_dt
        elif date_dt > latest:
            latest = date_dt
debug, info, warn, error = 0
noisest = None
err_max = 0
for module, counts in levels.items():
    debug += counts["debug"]
    info += counts["info"]
    warn += counts["warn"]
    error += counts["error"]
    if not err_max or err_max < counts["error"]:
        noisest = module

print(f"LEVEL_COUNTS debug={debug} info={info}, warn={warn}, error={error}")
print(f"TIME_RANGE first={earliest} last={latest}")
print(f"NOISY_MODULE {noisest}")

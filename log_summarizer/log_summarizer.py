import sys

from collections import defaultdict
from datetime import datetime, timedelta

n = int(sys.stdin.readline())
error_counts = {}
earliest = datetime.now()
latest = datetime.now()
for i in range(n):
    raw_line = sys.stdin.readline()
    time_str, level, module, message = raw_line.strip().split("\t")
    level_counts[module.lower()] = level_counts.get(module.lower(), (level.lower, 1))
    time_dt = datetime.strptime(time_str, "%Y-%m-%MT%H:%M:%S")
    if time_dt > latest:
        latest = time_dt
    elif time_dt < earliest:
        earliest = time_dt

noisiest = 
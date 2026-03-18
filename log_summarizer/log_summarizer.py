import sys
from collections import Counter
from datetime import datetime, timedelta


def read_stop_words():
    all_words = []
    with open("stop_words.txt", "r") as stop_in:
        for line in stop_in:
            words = line.strip().split(",")
            clean_words = [word.strip('"') for word in words]
            all_words.extend(clean_words)
    return all_words


def read_input():

    total = int(sys.stdin.readline())
    levels = Counter()
    first = datetime.today()
    last = datetime.today()
    noisy = Counter()
    words = Counter()
    for single in total:
        timestamp, level, module, message = sys.stdin.readline().strip().split("\t")
        levels[level] = levels.get(level, 0) + 1
        if level.lower() == "error":
            noisy[module] = noisy.get(module, 0) + 1
        ts_dt = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S")
        if timedelta(ts_dt) > first:
            first = ts_dt
        elif timedelta(ts_dt) < last:
            last = ts_dt


class TestSummarizer:

    def test_read_stop_words(self):
        words = read_stop_words()
        assert words[0] == "the"
        assert words[-1] == "be"

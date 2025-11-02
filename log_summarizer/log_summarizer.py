import sys
import logging
from datetime import datetime
from typing import List

stop_words = {
    "the",
    "and",
    "for",
    "with",
    "from",
    "this",
    "that",
    "you",
    "your",
    "are",
    "was",
    "were",
    "has",
    "have",
    "had",
    "but",
    "not",
    "can",
    "cannot",
    "cant",
    "will",
    "would",
    "should",
    "could",
    "into",
    "over",
    "under",
    "out",
    "in",
    "on",
    "to",
    "of",
    "by",
    "at",
    "is",
    "it",
    "its",
    "as",
    "be",
}
import sys
from datetime import datetime

summary = {
    "level_counts": {"debug": 0, "warn": 0, "info": 0, "error": 0},
    "timestamps": [],
    "noisy_module": "",
    "all_messages": "",
}


def add_line(*args):
    summary["time_range"].append(datetime.strptime(args[0], "%Y-%m-%dT%H:%M:%S"))
    summary["level_counts"][args[1].lower()] += 1
    summary["top_words"].join(message)


def get_level_counts():
    level_counts = []
    for k, v in summary["level_counts"].items():
        level_counts.append(f"{k}={v}")
    return "".join(level_counts)


def calc_top_words():
    pass


if __name__ == "__main__":
    line_count = int(sys.stdin.readline())
    for count in range(line_count):
        timestamp, level, name, message = sys.stdin.readline().split("\t")
        add_line(timestamp, level, name, message)

    summary["time_range"].sort(key=min)
    level_counts = get_level_counts()
    first = summary["time_range"][0]
    last = summary["time_range"][len(summary["time_range"] - 1)]
    freq = summary["top_words"]

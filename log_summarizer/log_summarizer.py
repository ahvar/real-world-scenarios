import sys
from datetime import datetime, timedelta

levels_and_modules = {"debug": None, "info": None, "warn": None, "error": None}

first_time = datetime.now()
last_time = datetime.now()
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


def set_time_range(date_dt):

    duration = timedelta(days=date_dt.day, hours=date_dt.hour, minutes=date_dt.minutes)
    if duration > first_time:
        first_time = duration
    if duration < last_time:
        last_time = duration


def read_input():
    log_line_count = int(sys.stdin.readline())
    for _ in log_line_count:
        timestamp, level, module, msg = sys.stdin.readline().strip().split("\t")
        date_dt = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S")


def solve(input_stream=sys.stdin, output_stream=sys.stdout):
    n = int(input_stream.readline().strip())

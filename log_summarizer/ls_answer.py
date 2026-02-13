#!/usr/bin/env python3
"""Log Summarizer - Analyzes application logs and produces summary statistics."""

import sys
import re
from collections import Counter
from typing import List, Tuple, Optional


# Stopwords to exclude from word frequency analysis
STOPWORDS = {
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


def parse_log_line(line: str) -> Optional[Tuple[str, str, str, str]]:
    """
    Parse a TSV log line into its components.

    Returns: (timestamp, level, module, message) or None if invalid
    """
    parts = line.strip().split("\t")
    if len(parts) != 4:
        return None
    return tuple(parts)


def tokenize_message(message: str) -> List[str]:
    """
    Extract valid words from a log message.

    Rules:
    - Only alphabetic characters (a-z)
    - Lowercase for case-insensitive comparison
    - Minimum length of 3 characters
    - Exclude stopwords
    """
    # Split on non-alphabetic characters and convert to lowercase
    words = re.findall(r"[a-zA-Z]+", message.lower())

    # Filter: length >= 3 and not in stopwords
    return [word for word in words if len(word) >= 3 and word not in STOPWORDS]


def solve(input_stream=sys.stdin, output_stream=sys.stdout):
    """
    Main logic: read logs, compute statistics, and output summary.
    """
    # Read number of log lines
    n = int(input_stream.readline().strip())

    # Initialize counters and trackers
    level_counts = Counter()  # Count of each log level
    error_by_module = Counter()  # Count of ERROR logs per module
    word_counts = Counter()  # Word frequency across all messages
    timestamps = []  # All timestamps for range calculation

    # Process each log line
    for _ in range(n):
        line = input_stream.readline()
        parsed = parse_log_line(line)

        if not parsed:
            continue  # Skip invalid lines

        timestamp, level, module, message = parsed

        # Track level counts
        level_counts[level] += 1

        # Track ERROR logs by module for noisy module detection
        if level == "ERROR":
            error_by_module[module] += 1

        # Track timestamps
        timestamps.append(timestamp)

        # Extract and count words from message
        words = tokenize_message(message)
        word_counts.update(words)

    # --- Output 1: LEVEL_COUNTS ---
    output_stream.write(
        f"LEVEL_COUNTS debug={level_counts.get('DEBUG', 0)} "
        f"info={level_counts.get('INFO', 0)} "
        f"warn={level_counts.get('WARN', 0)} "
        f"error={level_counts.get('ERROR', 0)}\n"
    )

    # --- Output 2: TIME_RANGE ---
    if timestamps:
        first_time = min(timestamps)
        last_time = max(timestamps)
        output_stream.write(f"TIME_RANGE first={first_time} last={last_time}\n")
    else:
        output_stream.write("TIME_RANGE first=none last=none\n")

    # --- Output 3: NOISY_MODULE ---
    if error_by_module:
        # Find max error count
        max_errors = max(error_by_module.values())
        # Get all modules with max errors, pick lexicographically smallest
        noisy_modules = [
            mod for mod, count in error_by_module.items() if count == max_errors
        ]
        noisy_module = min(noisy_modules)
        output_stream.write(f"NOISY_MODULE {noisy_module}\n")
    else:
        output_stream.write("NOISY_MODULE none\n")

    # --- Output 4: TOP_WORDS ---
    if word_counts:
        # Get top 5 words, sorted by count (desc) then alphabetically (asc)
        top_words = word_counts.most_common()
        # Sort: first by count descending, then by word ascending
        top_words.sort(key=lambda x: (-x[1], x[0]))
        top_5 = top_words[:5]

        word_pairs = [f"{word}={count}" for word, count in top_5]
        output_stream.write(f"TOP_WORDS {', '.join(word_pairs)}\n")
    else:
        output_stream.write("TOP_WORDS\n")


if __name__ == "__main__":
    solve()

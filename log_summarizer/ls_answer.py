#!/usr/bin/env python3
"""Log Summarizer - Analyzes application logs and produces summary statistics."""

import sys
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
    Extract valid words from a log message using only builtins.

    Rules:
    - Only alphabetic characters (a-z)
    - Lowercase for case-insensitive comparison
    - Minimum length of 3 characters
    - Exclude stopwords
    """
    words = []
    current_word = []

    # Manually extract alphabetic characters
    for char in message.lower():
        if char.isalpha():
            current_word.append(char)
        else:
            if current_word:
                word = "".join(current_word)
                if len(word) >= 3 and word not in STOPWORDS:
                    words.append(word)
                current_word = []

    # Don't forget the last word
    if current_word:
        word = "".join(current_word)
        if len(word) >= 3 and word not in STOPWORDS:
            words.append(word)

    return words


def count_items(items: List[str]) -> dict:
    """
    Count occurrences of items in a list.
    Replacement for collections.Counter.

    Returns: dict with item -> count mapping
    """
    counts = {}
    for item in items:
        counts[item] = counts.get(item, 0) + 1
    return counts


def get_top_n_sorted(counts: dict, n: int) -> List[Tuple[str, int]]:
    """
    Get top N items from a count dict, sorted by:
    1. Count (descending)
    2. Item name (ascending) for ties

    Returns: List of (item, count) tuples
    """
    # Convert dict to list of tuples
    items = list(counts.items())

    # Sort by count (descending), then by name (ascending)
    # Using negative count for descending order
    items.sort(key=lambda x: (-x[1], x[0]))

    return items[:n]


def solve(input_stream=sys.stdin, output_stream=sys.stdout):
    """
    Main logic: read logs, compute statistics, and output summary.
    """
    # Read number of log lines
    n = int(input_stream.readline().strip())

    # Initialize counters and trackers - using dicts instead of Counter
    level_counts = {}  # Count of each log level
    error_by_module = {}  # Count of ERROR logs per module
    all_words = []  # All words for frequency counting
    timestamps = []  # All timestamps for range calculation

    # Process each log line
    for _ in range(n):
        line = input_stream.readline()
        parsed = parse_log_line(line)

        if not parsed:
            continue  # Skip invalid lines

        timestamp, level, module, message = parsed

        # Track level counts
        level_counts[level] = level_counts.get(level, 0) + 1

        # Track ERROR logs by module for noisy module detection
        if level == "ERROR":
            error_by_module[module] = error_by_module.get(module, 0) + 1

        # Track timestamps
        timestamps.append(timestamp)

        # Extract words from message
        words = tokenize_message(message)
        all_words.extend(words)

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
    if all_words:
        # Count word frequencies
        word_counts = count_items(all_words)

        # Get top 5 words
        top_5 = get_top_n_sorted(word_counts, 5)

        word_pairs = [f"{word}={count}" for word, count in top_5]
        output_stream.write(f"TOP_WORDS {', '.join(word_pairs)}\n")
    else:
        output_stream.write("TOP_WORDS\n")


if __name__ == "__main__":
    solve()

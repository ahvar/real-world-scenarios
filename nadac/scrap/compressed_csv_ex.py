import csv
import lzma
from pathlib import Path


def count_rows(path: Path) -> int:
    total = 0
    with lzma.open(path, "rt", encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            total += 1
    return total

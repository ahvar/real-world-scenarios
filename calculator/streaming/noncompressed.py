import csv
import lzma
from pathlib import Path

plans_path = Path(__file__).parent.parent / "data" / "plans.csv"

def compress_data(path):
    with lzma.open(path, 'wt', encoding='utf-8', newline='\n') as fh:
        writer = csv.DictWriter(fh, fieldnames=


def count_rows_bad(path: Path) -> int:
    with lzma.open(path, "rt", encoding="utf-8", newline="\n") as fh:
        reader = csv.DictReader(fh)


if __name__ == "__main__":
    count_rows(plans_path)

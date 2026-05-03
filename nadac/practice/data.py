import csv
import lzma
import itertools
import random
from decimal import Decimal
from datetime import datetime
from pathlib import Path

FIELDNAMES = [
    "NDC Description",
    "NDC",
    "Old NADAC Per Unit",
    "New NADAC Per Unit",
    "Classification for Rate Setting",
    "Percent Change",
    "Primary Reason",
    "Start Date",
    "End Date",
    "Effective Date",
]


BASE_ROW = {
    "Classification for Rate Setting": "GENERIC",
    "Percent Change": "",
    "Primary Reason": "WAC CHANGE",
    "Start Date": "01/01/2020",
    "End Date": "01/07/2020",
    "Effective Date": "01/08/2020",
}


def make_row(index: int, old_price: Decimal, new_price: Decimal):
    return {
        **BASE_ROW,
        "NDC Description": f"DRUG {index}",
        "NDC": f"{index:011d}",
        "Old NADAC Per Unit": str(old_price),
        "New NADAC Per Unit": str(new_price),
    }


def write_fake_data(path: Path, row_count: int = 100, seed: int = 0):
    random.seed(seed)

    with lzma.open(path, "wt", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDNAMES)
        writer.writeheader()
        for index in range(row_count):
            old_price = Decimal(random.randint(100, 5000)) / Decimal("100")
            delta = Decimal(random.randint(-1500, 1500)) / Decimal("100")
            new_price = old_price + delta

            if new_price < 0:
                new_price = Decimal("0.01")

            writer.writerow(make_row(index, old_price, new_price))
    return path


def nadac_file():
    path = Path(__file__).parent / "nadac_sample.csv.xz"
    return write_fake_data

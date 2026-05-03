import pytest
import lzma
from pathlib import Path


@pytest.fixture()
def nadac_file():
    path = Path(__file__).parent / "nadac_sample.csv.xz"
    with lzma.open(path, "wt", encoding="utf-8", newline="") as fh:
        fh.write()

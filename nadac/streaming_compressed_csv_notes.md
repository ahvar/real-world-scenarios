# Streaming Compressed CSV with `lzma` in Python

When working with `lzma` and CSV in Python, it helps to separate two ideas:

- The **data format** is CSV.
- The **file encoding on disk** can be compressed with LZMA.

That means a file can still be "a CSV" even if the bytes stored on disk are compressed, such as a file named `data.csv.xz`.

## What Is Actually Stored?

If you open a plain CSV file, the bytes on disk are directly readable text.

If you open an LZMA-compressed CSV file, the bytes on disk are compressed binary data. Inside that compressed file is the original CSV text.

So this is the correct mental model:

compressed file on disk
-> `lzma.open(..., "rt")`
-> decompressed text stream
-> `csv.DictReader`
-> one CSV row at a time

## Why Use `lzma.open`?

`lzma.open` decompresses the file as you read it. In text mode (`"rt"`), it gives you a text stream that works well with `csv.DictReader`.

Example:

```python
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
```

## Is the Source Data Compressed or CSV?

Both statements can be true, depending on what you mean:

- **Logically**: it is CSV data.
- **Physically on disk**: it may be LZMA-compressed data.

So if you are using `lzma.open`, the file on disk is compressed. After decompression, Python sees normal CSV text.

## Practical Rule of Thumb

- Use `open(...)` for plain `.csv` files.
- Use `lzma.open(...)` for `.xz` or `.csv.xz` files.
- In both cases, `csv.DictReader` parses rows from a text stream.

## Why This Is Useful for Streaming

This pattern is memory-efficient because Python does not need to:

- decompress the entire file up front
- load the entire CSV into memory

Instead, it reads, decompresses, and parses incrementally. That makes it a good fit for large reporting jobs like the NADAC exercise.

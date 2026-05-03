# NADAC Top Price Change Report (Streaming Top-K)

Build a memory-efficient and performant Python program that processes NADAC (National Average Drug Acquisition Cost) comparison data and prints the top unique price increases and decreases within a given effective year.

This practice challenge is inspired by the CMS “NADAC Week-to-Week File Comparison” dataset field definitions:
- NDC Description
- NDC
- Old NADAC Per Unit
- New NADAC Per Unit
- Classification for Rate Setting
- Percent Change
- Primary Reason
- Start Date
- End Date
- Effective Date

## Goal

Implement `generate_nadac_top_price_change_report(year: int, count: int) -> str` that:

1. Streams a CSV dataset row-by-row (do not load into memory).
2. Filters rows to keep only those with an Effective Date in the requested `year`.
3. Computes the full-precision per-unit price change per row:

   `change = new_nadac_per_unit - old_nadac_per_unit`

4. Does **not** round `change` until rendering the final report.
5. Produces two Top-N lists:
   - Top `count` increases (largest positive changes)
   - Top `count` decreases (most negative changes)
6. Ensures uniqueness is based on:
   - `(NDC Description, full-precision change)`
   Duplicate pairs must be eliminated.
7. Orders results by the full-precision `change` (not rounded values).

## Output Format

Report must match this exact format:

Top 10 NADAC per unit price increases of 2020:
$1054.18: STELARA 45 MG/0.5 ML SYRINGE
$1048.40: STELARA 90 MG/MG SYRINGE
$420.33: SIMPONI 50 MG/0.5 ML PEN INJEC
...

Top 10 NADAC per unit price decreases of 2020:
-$117.40: DIHYDROERGOTAMINE MESYLATE 4 MG/ML NASAL SPRAY
-$100.02: STELARA 90 MG/ML SYRINGE
-$71.51: STELARA 90 MG/ML SYRINGE
...

Notes:
- There must be a blank line separating the two sections.
- Money must be rendered to 2 decimal places.
- Negative sign must appear before `$` (e.g., -$117.40).
- Do not add thousands separators.

## Constraints (Grading Rubric)

### Code quality (4/10)
- Clear decomposition into helper functions/classes.
- Well-named variables and functions.
- Reasonable error handling for malformed rows.
- Testable design.

### Memory (3.5/10)
- Must stream the CSV.
- Let N be the requested `count`.
- Working data structures should typically remain size <= N per list.
- Up to `2N + 1` total items across structures is acceptable.
- Any approach that stores more than `2N + 1` items fails the memory constraint.

### Performance (2.5/10)
- Optimize with large N in mind.
- Rows that cannot join the current Top-N should be rejected with constant-time checks.
- Avoid scanning the working Top-N list for each row.

## Allowed / Disallowed

- ✅ Use Python standard library (csv, heapq, decimal, datetime, lzma, argparse, pathlib).
- ✅ Use pytest for tests.
- ❌ Do not use pandas or sqlite3.

## Project Layout

- `data.py` – opens the compressed NADAC comparison CSV
- `report.py` – implement the report generator
- `main.py` – CLI entrypoint
- `test_report.py` – pytest tests (uses synthetic dataset)

## Running

```bash
python main.py --year 2020 --count 10
pytest -q

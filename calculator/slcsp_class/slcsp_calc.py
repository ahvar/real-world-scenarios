#!/usr/bin/env python3
"""
SLCSP CLI

Usage:
  python slcsp_cli.py --slcsp slcsp.csv --plans plans.csv --zips zips.csv > output.csv
"""
import sys
import csv
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from typing import List, Dict, Set, Tuple, Optional
import typer
import references as ref

app = typer.Typer(help="Compute the Second Lowest Cost Silver Plan (SLCSP) for ZIP codes.")


class SLCSPCalculator:
    """
    Loads CSVs, builds indices, and computes SLCSP values.
    Private state; read-only via properties. Column names come from `references.py`.
    """

    def __init__(self) -> None:
        self._slcsp_rows: List[Dict[str, str]] = []
        self._plans_rows: List[Dict[str, str]] = []
        self._zips_rows: List[Dict[str, str]] = []
        self._zip_to_areas: Dict[str, Set[Tuple[str, str]]] = {}
        self._area_to_rates: Dict[Tuple[str, str], List[Decimal]] = {}

    # ---- Read-only properties ----
    @property
    def slcsp_rows(self) -> List[Dict[str, str]]:
        return self._slcsp_rows

    @property
    def plans_rows(self) -> List[Dict[str, str]]:
        return self._plans_rows

    @property
    def zips_rows(self) -> List[Dict[str, str]]:
        return self._zips_rows

    @property
    def zip_to_areas(self) -> Dict[str, Set[Tuple[str, str]]]:
        return self._zip_to_areas

    @property
    def area_to_rates(self) -> Dict[Tuple[str, str], List[Decimal]]:
        return self._area_to_rates

    # ---- Public API ----
    def load_data(self, slcsp_path: Path, plans_path: Path, zips_path: Path) -> None:
        self._slcsp_rows = self._read_csv(slcsp_path, "slcsp.csv")
        self._plans_rows  = self._read_csv(plans_path,  "plans.csv")
        self._zips_rows   = self._read_csv(zips_path,   "zips.csv")
        self._build_indices()

    def compute_and_emit_stdout(self) -> None:
        """Emit CSV to stdout; preserves the original SLCSP row order."""
        out = csv.writer(sys.stdout, lineterminator="\n")
        out.writerow([ref.OUT_HEADER_ZIP, ref.OUT_HEADER_RATE])

        for row in self._slcsp_rows:
            zipcode = (row.get(ref.SLCSP_ZIPCODE_COL) or "").strip()
            rate = self._slcsp_for_zip(zipcode)
            out.writerow([zipcode, self._fmt_money(rate) if rate is not None else ""])

    # ---- Internals ----
    def _fmt_money(self, d: Decimal) -> str:
        return str(d.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))

    def _read_csv(self, path: Path, label: str) -> List[Dict[str, str]]:
        try:
            with path.open(newline="") as f:
                return list(csv.DictReader(f))
        except FileNotFoundError:
            typer.secho(f"Error: File not found -> {path}", fg=typer.colors.RED, err=True)
            sys.exit(1)
        except PermissionError:
            typer.secho(f"Error: Permission denied -> {path}", fg=typer.colors.RED, err=True)
            sys.exit(1)
        except csv.Error as e:
            typer.secho(f"Error: Failed to parse {label}: {e}", fg=typer.colors.RED, err=True)
            sys.exit(1)

    def _build_indices(self) -> None:
        self._zip_to_areas = self._map_rate_areas_for_zip(self._zips_rows)
        self._area_to_rates = self._silver_rates_by_area(self._plans_rows)

    def _map_rate_areas_for_zip(
        self, zips_rows: List[Dict[str, str]]
    ) -> Dict[str, Set[Tuple[str, str]]]:
        """
        Map zipcode -> set of (state, rate_area).
        Ambiguous if ZIP has multiple distinct (state, rate_area).
        """
        by_zip: Dict[str, Set[Tuple[str, str]]] = {}
        for r in zips_rows:
            zipcode = (r.get(ref.ZIPS_ZIPCODE_COL) or "").strip()
            state = (r.get(ref.ZIPS_STATE_COL) or "").strip()
            rate_area = (r.get(ref.ZIPS_RATE_AREA_COL) or "").strip()
            if zipcode and state and rate_area:
                by_zip.setdefault(zipcode, set()).add((state, rate_area))
        return by_zip

    def _silver_rates_by_area(
        self, plans_rows: List[Dict[str, str]]
    ) -> Dict[Tuple[str, str], List[Decimal]]:
        """
        Map (state, rate_area) -> sorted list of DISTINCT Decimal rates for Silver plans.
        """
        rates: Dict[Tuple[str, str], Set[Decimal]] = {}
        for r in plans_rows:
            metal = (r.get(ref.PLANS_METAL_LEVEL_COL) or "").strip().lower()
            if metal != ref.SILVER:
                continue

            state = (r.get(ref.PLANS_STATE_COL) or "").strip()
            rate_area = (r.get(ref.PLANS_RATE_AREA_COL) or "").strip()
            rate_str = (r.get(ref.PLANS_RATE_COL) or "").strip()
            if not (state and rate_area and rate_str):
                continue

            try:
                rate = Decimal(rate_str)
            except Exception:
                typer.secho(
                    f"Warning: Skipping invalid rate '{rate_str}' in plans.csv",
                    fg=typer.colors.YELLOW,
                    err=True,
                )
                continue

            key = (state, rate_area)
            rates.setdefault(key, set()).add(rate)

        return {k: sorted(v) for k, v in rates.items()}

    def _slcsp_for_zip(self, zipcode: str) -> Optional[Decimal]:
        areas = self._zip_to_areas.get(zipcode, set())
        if not areas or len(areas) != 1:
            return None
        (state, area) = next(iter(areas))
        silver_rates = self._area_to_rates.get((state, area), [])
        if len(silver_rates) < 2:
            return None
        return silver_rates[1]  # second-lowest DISTINCT silver rate


@app.command()
def run(
    slcsp: Path = typer.Option(..., "--slcsp", exists=True, file_okay=True, dir_okay=False, help="Path to slcsp.csv"),
    plans: Path = typer.Option(..., "--plans", exists=True, file_okay=True, dir_okay=False, help="Path to plans.csv"),
    zips:  Path = typer.Option(..., "--zips",  exists=True, file_okay=True, dir_okay=False, help="Path to zips.csv"),
):
    calc = SLCSPCalculator()
    calc.load_data(slcsp, plans, zips)
    calc.compute_and_emit_stdout()


def main():
    app()


if __name__ == "__main__":
    main()

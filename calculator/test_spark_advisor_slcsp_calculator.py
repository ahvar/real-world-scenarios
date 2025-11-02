import csv
from decimal import Decimal
from pathlib import Path
from typer.testing import CliRunner
import pytest

# Import your app + calculator
from slcsp_cli import SLCSPCalculator, app
import references as ref

runner = CliRunner()

def _write_csv(path: Path, header: list[str], rows: list[list[str]]) -> None:
    with path.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for r in rows:
            writer.writerow(r)

class TestSLCSP:
    def test_indices_and_second_lowest(self, tmp_path: Path):
        """Happy-path: one ZIP -> one area with >=2 silver plans: we get second-lowest distinct."""
        slcsp_p = tmp_path / "slcsp.csv"
        plans_p = tmp_path / "plans.csv"
        zips_p  = tmp_path / "zips.csv"

        # Input CSVs
        _write_csv(slcsp_p, [ref.SLCSP_ZIPCODE_COL, ref.OUT_HEADER_RATE], [["11111", ""]])

        _write_csv(
            plans_p,
            [ref.PLANS_STATE_COL, ref.PLANS_METAL_LEVEL_COL, ref.PLANS_RATE_COL, ref.PLANS_RATE_AREA_COL],
            [
                ["NY", "silver", "200.10", "1"],
                ["NY", "silver", "200.10", "1"],  # duplicate should be de-duplicated
                ["NY", "silver", "201.10", "1"],  # second distinct
                ["NY", "gold",   "150.00", "1"],  # non-silver ignored
            ],
        )

        _write_csv(
            zips_p,
            [ref.ZIPS_ZIPCODE_COL, ref.ZIPS_STATE_COL, ref.ZIPS_RATE_AREA_COL],
            [["11111", "NY", "1"]],
        )

        calc = SLCSPCalculator()
        calc.load_data(slcsp_p, plans_p, zips_p)

        # Indices built correctly
        assert calc.zip_to_areas == {"11111": {("NY", "1")}}
        assert calc.area_to_rates[("NY", "1")] == [Decimal("200.10"), Decimal("201.10")]

        # Compute result (capture stdout)
        from io import StringIO
        import sys
        buf, old = StringIO(), sys.stdout
        sys.stdout = buf
        try:
            calc.compute_and_emit_stdout()
        finally:
            sys.stdout = old

        lines = buf.getvalue().strip().splitlines()
        assert lines[0] == f"{ref.OUT_HEADER_ZIP},{ref.OUT_HEADER_RATE}"
        assert lines[1] == "11111,201.10"  # second-lowest DISTINCT

    def test_ambiguous_zip_leaves_blank(self, tmp_path: Path):
        """ZIP in multiple areas -> ambiguous -> blank rate."""
        slcsp_p = tmp_path / "slcsp.csv"
        plans_p = tmp_path / "plans.csv"
        zips_p  = tmp_path / "zips.csv"

        _write_csv(slcsp_p, [ref.SLCSP_ZIPCODE_COL, ref.OUT_HEADER_RATE], [["22222", ""]])

        _write_csv(
            plans_p,
            [ref.PLANS_STATE_COL, ref.PLANS_METAL_LEVEL_COL, ref.PLANS_RATE_COL, ref.PLANS_RATE_AREA_COL],
            [["CA", "silver", "300.00", "7"], ["CA", "silver", "305.00", "8"]],
        )

        _write_csv(
            zips_p,
            [ref.ZIPS_ZIPCODE_COL, ref.ZIPS_STATE_COL, ref.ZIPS_RATE_AREA_COL],
            [["22222", "CA", "7"], ["22222", "CA", "8"]],  # ambiguous
        )

        calc = SLCSPCalculator()
        calc.load_data(slcsp_p, plans_p, zips_p)

        from io import StringIO
        import sys
        buf, old = StringIO(), sys.stdout
        sys.stdout = buf
        try:
            calc.compute_and_emit_stdout()
        finally:
            sys.stdout = old

        lines = buf.getvalue().strip().splitlines()
        assert lines[1] == "22222,"  # blank

    def test_less_than_two_silver_rates_blank(self, tmp_path: Path):
        """Only one silver plan in area -> blank."""
        slcsp_p = tmp_path / "slcsp.csv"
        plans_p = tmp_path / "plans.csv"
        zips_p  = tmp_path / "zips.csv"

        _write_csv(slcsp_p, [ref.SLCSP_ZIPCODE_COL, ref.OUT_HEADER_RATE], [["33333", ""]])

        _write_csv(
            plans_p,
            [ref.PLANS_STATE_COL, ref.PLANS_METAL_LEVEL_COL, ref.PLANS_RATE_COL, ref.PLANS_RATE_AREA_COL],
            [["TX", "silver", "410.00", "2"]],
        )

        _write_csv(
            zips_p,
            [ref.ZIPS_ZIPCODE_COL, ref.ZIPS_STATE_COL, ref.ZIPS_RATE_AREA_COL],
            [["33333", "TX", "2"]],
        )

        calc = SLCSPCalculator()
        calc.load_data(slcsp_p, plans_p, zips_p)

        from io import StringIO
        import sys
        buf, old = StringIO(), sys.stdout
        sys.stdout = buf
        try:
            calc.compute_and_emit_stdout()
        finally:
            sys.stdout = old

        lines = buf.getvalue().strip().splitlines()
        assert lines[1] == "33333,"  # blank

    def test_output_order_and_rounding(self, tmp_path: Path):
        """Preserve slcsp.csv order and ensure two-decimal formatting/rounding."""
        slcsp_p = tmp_path / "slcsp.csv"
        plans_p = tmp_path / "plans.csv"
        zips_p  = tmp_path / "zips.csv"

        _write_csv(
            slcsp_p, [ref.SLCSP_ZIPCODE_COL, ref.OUT_HEADER_RATE], [["99999", ""], ["11111", ""], ["77777", ""]
        ])

        # Build: NY/1 has rates where second-lowest requires rounding to 2 decimals
        _write_csv(
            plans_p,
            [ref.PLANS_STATE_COL, ref.PLANS_METAL_LEVEL_COL, ref.PLANS_RATE_COL, ref.PLANS_RATE_AREA_COL],
            [
                ["NY", "silver", "200.105", "1"],  # rounds to 200.11 (half-up)
                ["NY", "silver", "201.1",   "1"],  # 201.10
                ["WA", "silver", "190.00",  "3"],
                ["WA", "silver", "195",     "3"],
            ],
        )

        _write_csv(
            zips_p,
            [ref.ZIPS_ZIPCODE_COL, ref.ZIPS_STATE_COL, ref.ZIPS_RATE_AREA_COL],
            [["11111", "NY", "1"], ["77777", "WA", "3"], ["99999", "TX", "9"]],  # 99999 has no matching plans
        )

        calc = SLCSPCalculator()
        calc.load_data(slcsp_p, plans_p, zips_p)

        from io import StringIO
        import sys
        buf, old = StringIO(), sys.stdout
        sys.stdout = buf
        try:
            calc.compute_and_emit_stdout()
        finally:
            sys.stdout = old

        lines = buf.getvalue().strip().splitlines()
        # Order preserved as in slcsp.csv
        assert lines[0] == "zipcode,rate"
        assert lines[1].startswith("99999,")  # no area -> blank
        assert lines[1] == "99999,"
        assert lines[2].startswith("11111,")  # NY/1
        # NY second-lowest distinct is 201.10 (since 200.105 -> 200.11, 201.1 -> 201.10)
        assert lines[2] == "11111,201.10"
        assert lines[3] == "77777,195.00"     # WA/3 second-lowest: 195.00

    def test_cli_end_to_end(self, tmp_path: Path):
        """Invoke the Typer CLI and assert emitted CSV."""
        slcsp_p = tmp_path / "slcsp.csv"
        plans_p = tmp_path / "plans.csv"
        zips_p  = tmp_path / "zips.csv"

        _write_csv(slcsp_p, [ref.SLCSP_ZIPCODE_COL, ref.OUT_HEADER_RATE], [["12345", ""], ["54321", ""]])

        _write_csv(
            plans_p,
            [ref.PLANS_STATE_COL, ref.PLANS_METAL_LEVEL_COL, ref.PLANS_RATE_COL, ref.PLANS_RATE_AREA_COL],
            [
                ["IL", "silver", "250.00", "14"],
                ["IL", "silver", "255.00", "14"],
                ["IL", "gold",   "180.00", "14"],
            ],
        )

        _write_csv(
            zips_p,
            [ref.ZIPS_ZIPCODE_COL, ref.ZIPS_STATE_COL, ref.ZIPS_RATE_AREA_COL],
            [["12345", "IL", "14"], ["54321", "IL", "99"]],
        )

        result = runner.invoke(
            app,
            [
                "run",
                "--slcsp", str(slcsp_p),
                "--plans", str(plans_p),
                "--zips",  str(zips_p),
            ],
        )
        assert result.exit_code == 0
        lines = result.stdout.strip().splitlines()
        assert lines[0] == "zipcode,rate"
        assert lines[1] == "12345,255.00"  # IL/14 second-lowest
        assert lines[2] == "54321,"        # IL/99 no silver -> blank

import csv
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

plans_path = Path(__file__).parent.parent / "data" / "plans.csv"
zips_path = Path(__file__).parent.parent / "data" / "zips.csv"
slcsp_zips_path = Path(__file__).parent.parent / "data" / "slcsp.csv"


@dataclass
class Location:
    zipcode: str
    state: str
    county_code: str
    name: str
    rate_area: int


@dataclass
class Plan:
    plan_id: str
    state: str
    metal_level: str
    rate: float
    rate_area: int


def get_slcsp_zip_codes():
    """Load the list of zip codes we need to find SLCSP for."""
    slcsp_zip_codes = []
    with open(slcsp_zips_path, "r") as slcsp_in:
        reader = csv.DictReader(slcsp_in)  # Fixed: pass file to DictReader
        for row in reader:
            slcsp_zip_codes.append(row["zipcode"])
    return slcsp_zip_codes


def get_plans():
    """Load all plans from CSV into Plan dataclass objects."""
    plans = []
    with open(plans_path, "r") as plans_in:
        reader = csv.DictReader(plans_in)
        for row in reader:
            row["rate"] = float(row["rate"])
            row["rate_area"] = int(row["rate_area"])
            plans.append(Plan(**row))
    return plans


def get_locations():
    """Load all locations from CSV into Location dataclass objects."""
    locations = []
    with open(zips_path, "r") as zips_in:
        reader = csv.DictReader(zips_in)
        for row in reader:
            row["rate_area"] = int(row["rate_area"])
            locations.append(Location(**row))
    return locations


def main():
    """
    Calculate the second-lowest cost silver plan (SLCSP) for each zipcode.

    Logic:
    1. For each zipcode, find all rate areas (state, rate_area pairs)
    2. If zipcode spans multiple rate areas, return empty string
    3. Get all silver plans for that rate area
    4. Sort unique rates and return second-lowest (index 1)
    5. If fewer than 2 unique rates, return empty string
    """
    slcsp_zip_codes = get_slcsp_zip_codes()
    locations = get_locations()
    plans = get_plans()

    # Build a lookup: zipcode -> set of (state, rate_area) tuples
    rate_areas_by_zipcode = defaultdict(set)
    for location in locations:
        rate_areas_by_zipcode[location.zipcode].add(
            (location.state, location.rate_area)
        )

    # Build a lookup: (state, rate_area) -> list of silver plan rates
    silver_rates_by_rate_area = defaultdict(list)
    for plan in plans:
        if plan.metal_level.lower() == "silver":
            silver_rates_by_rate_area[(plan.state, plan.rate_area)].append(plan.rate)

    # Calculate SLCSP for each zipcode
    print("zipcode,rate")
    for zipcode in slcsp_zip_codes:
        rate_areas = rate_areas_by_zipcode.get(zipcode, set())

        # Ambiguous if zipcode spans multiple rate areas
        if len(rate_areas) != 1:
            print(f"{zipcode},")
            continue

        # Get the single rate area for this zipcode
        state, rate_area = next(iter(rate_areas))

        # Get all unique silver rates for this rate area, sorted
        rates = sorted(set(silver_rates_by_rate_area.get((state, rate_area), [])))

        # Need at least 2 unique rates to have a second-lowest
        if len(rates) < 2:
            print(f"{zipcode},")
        else:
            # Second-lowest is at index 1
            print(f"{zipcode},{rates[1]:.2f}")


class TestSLCSP:

    def test_get_plans(self):
        plans = get_plans()
        assert plans != None
        assert plans[-1].plan_id == "10412345604"
        assert plans[0].plan_id == "11512345601"
        print(plans[0])

    def test_get_locations(self):
        locations = get_locations()
        assert locations != None
        assert locations[0].zipcode == "64148"

    def test_get_slcsp_zip_codes(self):
        slcsp_zip_codes = get_slcsp_zip_codes()
        assert slcsp_zip_codes != None
        assert len(slcsp_zip_codes) == 10
        assert "64148" in slcsp_zip_codes
        assert "29745" in slcsp_zip_codes


if __name__ == "__main__":
    main()

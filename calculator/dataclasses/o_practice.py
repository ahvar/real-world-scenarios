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


slcsp_zip_codes = []
with open(slcsp_zips_path, "r") as slcsp_in:
    reader = csv.DictReader()
    for row in reader:
        slcsp_zip_codes.append(row["zipcode"])


def get_plans():
    plans = []
    with open(plans_path, "r") as plans_in:
        reader = csv.DictReader(plans_in)
        for row in reader:
            row["rate"] = float(row["rate"])
            row["rate_area"] = int(row["rate_area"])
            plans.append(Plan(**row))
    return plans


def get_locations():
    locations = []
    with open(zips_path, "r") as zips_in:
        reader = csv.DictReader(zips_in)
        for row in reader:
            row["rate_area"] = int(row["rate_area"])
            locations.append(Location(**row))
    return locations


def main():
    locations = get_locations()
    plans = get_plans()
    for zipcode in slcsp_zip_codes:
        rate_areas = [
            (location.state, location.rate_area)
            for location in locations
            if location.zipcode == zipcode
        ]


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

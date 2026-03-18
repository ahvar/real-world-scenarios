from pathlib import Path
from collections import defaultdict

plans_path = Path(__file__).parent.parent / "data" / "plans.csv"
slcsp_path = Path(__file__).parent.parent / "data" / "slcsp.csv"
zips_path = Path(__file__).parent.parent / "data" / "zips.csv"


def get_silver_rate_by_rate_area():
    rate_by_rate_area = defaultdict(list)
    with open(plans_path, "r") as plans_in:
        header = next(plans_in)
        for line in plans_in:
            plan_id, state, metal_level, rate, rate_area = line.strip().split(",")
            if metal_level.lower() == "silver":
                rate_by_rate_area[(state, rate_area)].append(float(rate))
    return rate_by_rate_area


def get_slcsp_zipcode():
    slcsp_zip_codes = []
    with open(slcsp_path, "r") as slcsp_in:
        header = next(slcsp_in)
        for line in slcsp_in:
            zipcode = line.strip().split(",")[0]
            slcsp_zip_codes.append(zipcode)
    return slcsp_zip_codes


def get_rate_area_by_zipcode():
    rate_areas = defaultdict(set)
    with open(zips_path, "r") as zips_in:
        header = next(zips_in)
        for line in zips_in:
            zipcode, state, cc, name, rate_area = line.strip().split(",")
            rate_areas[zipcode].add((state, rate_area))
    return rate_areas


def calculate_slcsp():
    rate_by_rate_area = get_silver_rate_by_rate_area()
    slcsp_zipcodes = get_slcsp_zipcode()
    rate_areas = get_rate_area_by_zipcode()
    output = []
    for zipcode in rate_areas:
        rate_areas = rate_areas.get(zipcode)
        if len(rate_areas) != 1:
            output.append((zipcode, ""))
            continue
        state, rate_area = next(iter(rate_areas))
        rates = sorted(set(rate_by_rate_area.get((state, rate_area), [])))


class TestSLCSPCalculator:

    def setup_method(self):
        pass

    def test_get_silver_rate(self):
        rate_by_rate_area = get_silver_rate_by_rate_area()
        assert ("MO", "3") in rate_by_rate_area
        assert rate_by_rate_area.get(("MO", "3")) == [310.50, 320.75, 335.25]

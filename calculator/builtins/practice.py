import json
import pprint
from pathlib import Path
from collections import defaultdict

pp = pprint.PrettyPrinter(indent=4)


def get_rates_by_rate_area():
    rates_by_rate_area = defaultdict(list)
    plans_path = Path(__file__).parent.parent / "data" / "plans.csv"
    with open(plans_path, "r") as plans_in:
        header = next(plans_in)
        for line in plans_in:
            plan_id, state, metal_level, rate, rate_area = line.strip().split(",")
            if metal_level.lower() == "silver":
                rates_by_rate_area[(state, rate_area)].append(float(rate))
    return rates_by_rate_area


def get_slcsp_zipcodes():
    slcsp_zipcodes = []
    slcsp_zipcode_path = Path(__file__).parent.parent / "data" / "slcsp.csv"
    with open(slcsp_zipcode_path, "r") as slcsp_in:
        header = next(slcsp_in)
        for line in slcsp_in:
            zipcode = line.strip().split(",")[0]
            slcsp_zipcodes.append(zipcode)
    return slcsp_zipcodes


def get_rate_area_zips():
    rate_area_by_zipcode = defaultdict(set)
    rate_areas_path = Path(__file__).parent.parent / "data" / "zips.csv"
    with open(rate_areas_path, "r") as ra_in:
        header = next(ra_in)
        for line in ra_in:
            zipcode, state, cc, name, rate_area = line.strip().split(",")
            rate_area_by_zipcode[zipcode].add((state, rate_area))
    return rate_area_by_zipcode


def calculate_slcsp_premium():
    rates_by_rate_area = get_rates_by_rate_area()
    slcsp_zipcodes = get_slcsp_zipcodes()
    rate_area_by_zipcode = get_rate_area_zips()
    output = []
    for zipcode in slcsp_zipcodes:
        rate_areas = rate_area_by_zipcode.get(zipcode, set())
        if len(rate_areas) != 1:
            output.append[(zipcode, "")]
            continue
        state, rate_area = next(iter(rate_areas))
        rates = sorted(set(rates_by_rate_area[(state, rate_area), []]))
        if len(rates) < 2:
            output.append((zipcode, ""))
        else:
            output.append((zipcode, f"{rates[1]:.2f}"))

    for (
        zipcode,
        rate,
    ) in output:
        print(f"{zipcode}, {rate}")


if __name__ == "__main__":
    calculate_slcsp_premium()


class TestSLCSPCalculator:

    def test_get_rates_by_rate_area(self):
        rates_by_rate_area = get_rates_by_rate_area()
        pp.pprint(rates_by_rate_area)
        for rate_area in [("MO", "3"), ("KY", "4"), ("PA", "7")]:
            assert rate_area in rates_by_rate_area

    def test_get_slcsp_zipcodes(self):
        slcsp_zipcodes = get_slcsp_zipcodes()
        pp.pprint(slcsp_zipcodes)
        for zip in ["64148", "40813", "51012"]:
            assert zip in slcsp_zipcodes

    def test_get_rate_area_zips(self):
        rate_area_zips = get_rate_area_zips()
        pp.pprint(rate_area_zips)
        assert len(rate_area_zips["41101"]) == 1

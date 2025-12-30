from collections import defaultdict
from pathlib import Path

import pytest

plans_filepath = Path(__file__).resolve().parent.parent / "data" / "plans.csv"
slcsp_filepath = Path(__file__).resolve().parent.parent / "data" / "slcsp.csv"
zips_filepath = Path(__file__).resolve().parent.parent / "data" / "zips.csv"


def get_rates_by_rate_area():
    rates_by_rate_area = defaultdict(list)
    with open(plans_filepath, "r") as plans_in:
        plans_header = next(plans_in)
        for line in plans_in:
            plan_id, state, metal_level, rate, rate_area = line.strip().split(",")
            if metal_level == "Silver":
                rates_by_rate_area[(state, rate_area)].append(float(rate))
    return rates_by_rate_area


def get_slcsp_zips():
    slcsp_zips = []
    with open(slcsp_filepath, "r") as slcsp_in:
        slcsp_headers = next(slcsp_in)
        for line in slcsp_in:
            zipcode = line.strip().split(",")[0]
            slcsp_zips.append(zipcode)
    return slcsp_zips


def get_zips():
    zips_by_rate_area = defaultdict(set)
    with open(zips_filepath, "r") as zips_in:
        zips_header = next(zips_in)
        for line in zips_in:
            zipcode, state, cc, name, rate_area = line.strip().split(",")
            zips_by_rate_area[zipcode].add((state, rate_area))


if __name__ == "__main__":
    output = []
    slcsp_zipcodes = get_slcsp_zips()
    all_rates = get_rates_by_rate_area()
    zips_by_rate_area = get_zips()
    for zipcode in slcsp_zipcodes:
        rate_areas = zips_by_rate_area.get(zipcode, set())
        if len(rate_areas) != 1:
            output.append((zipcode, ""))
            continue
        state, rate_area = next(iter(rate_areas))
        rates = sorted(set(all_rates.get((state, rate_area), [])))
        if len(rates) < 2:
            output.append((zipcode, ""))
        else:
            output.append((zipcode, f"{rates[1]:.2f}"))
    import sys

    print("zipcode, rate")
    for zipcode, rate in output:
        print(f"{zipcode}, {rate}")


class TestSLCSPCalculator:

    def test_get_rates_by_rate_area(self):
        rates_by_rate_area = get_rates_by_rate_area()
        assert ("KS", "9") in rates_by_rate_area
        assert ("KY", "4") in rates_by_rate_area

    def test_get_slcsp_zips(self):
        slcsp_zips = get_slcsp_zips()
        for code in ("64148", "67118", "40813"):
            assert code in slcsp_zips

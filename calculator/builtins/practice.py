import json
from pathlib import Path
from collections import defaultdict

slcsp_zipcodes_file = Path(__file__).parent.parent / "data" / "slcsp.csv"
zipcodes = Path(__file__).parent.parent / "data" / "zips.csv"
plans_file = Path(__file__).parent.parent / "data" / "plans.csv"


def get_plan_rates_by_rate_area():
    plan_rates_by_rate_area = defaultdict(list)
    with open(plans_file, "r") as plans_in:
        header = next(plans_in)
        for line in plans_in:
            plan_id, state, metal_level, rate, rate_area = line.strip().split(",")
            if metal_level.lower() == "silver":
                plan_rates_by_rate_area[(state, rate_area)].append(float(rate))
    return plan_rates_by_rate_area


def get_slcsp_zipcodes():
    slcsp_zipcodes = []
    with open(slcsp_zipcodes_file, "r") as slcsp_in:
        header = next(slcsp_in)
        for line in slcsp_in:
            zipcode = line.strip().split(",")[0]
            slcsp_zipcodes.append(zipcode)
    return slcsp_zipcodes


def get_rate_area_by_zipcode():
    rate_area_by_zipcode = defaultdict(set)
    with open(zipcodes, "r") as zip_in:
        header = next(zip_in)
        for line in zip_in:
            zipcode, state, cc, name, rate_area = line.strip().split(",")
            rate_area_by_zipcode[zipcode].add((state, rate_area))
    return rate_area_by_zipcode


if __name__ == "__main__":
    slcsp_zipcodes = get_slcsp_zipcodes()
    rate_area_by_zipcode = get_rate_area_by_zipcode()
    plan_rate_by_rate_area = get_plan_rates_by_rate_area()
    output = []
    for zipcode in slcsp_zipcodes:
        # the zipcode will not be here if there is more than one rate area (e.g. 29745)
        rate_areas = rate_area_by_zipcode.get(zipcode, set())
        if len(rate_areas) != 1:
            output.append((zipcode, ""))
            continue
        state, rate_area = next(iter(rate_areas))
        rates = sorted(set(plan_rate_by_rate_area.get((state, rate_area), [])))
        if len(rates) < 2:
            output.append((zipcode, ""))
        else:
            output.append((zipcode, f"{rates[1]:.2f}"))


class TestSLCSPCalculator:

    def test_get_plan_rates_by_rate_area(self):
        plan_rates_by_rate_area = get_plan_rates_by_rate_area()

        for state, rate_area in [("MO", "3"), ("KS", "9"), ("PA", "7")]:
            assert (state, rate_area) in plan_rates_by_rate_area

    def test_get_slcsp_zipcodes(self):
        slcsp_zipcodes = get_slcsp_zipcodes()
        for zipcode in ["64148", "67118", "40813"]:
            assert zipcode in slcsp_zipcodes

    def test_get_rate_area_by_zipcode(self):
        rate_area_by_zipcode = get_rate_area_by_zipcode()
        rate_areas = [3, 9, 4, 7, 2, 5, 8, 6, 12, 7, 4]
        for zipcode, items in rate_area_by_zipcode.items():
            state, rate_area = next(iter(items))
            assert int(rate_area) in rate_areas

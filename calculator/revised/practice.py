from pathlib import Path
from collections import defaultdict

slcsp_zipcodes_path = Path(__file__).parent.parent / "data" / "slcsp.csv"
zipcodes_path = Path(__file__).parent.parent / "data" / "zips.csv"
plans_path = Path(__file__).parent.parent / "data" / "plans.csv"


def get_plan_rates_by_rate_area():
    rates_by_rate_area = defaultdict(list)
    with open(plans_path, "r") as plans_in:
        header = next(plans_in)
        for line in plans_in:
            plan_id, state, metal_level, rate, rate_area = line.strip().split(",")
            if metal_level.lower() == "silver":
                rates_by_rate_area[(state, rate_area)] = float(rate)
    return rates_by_rate_area


def get_slcsp_zipcodes():
    slcsp_zipcodes = []
    with open(slcsp_zipcodes_path, "r") as zip_in:
        header = next(zip_in)
        for line in zip_in:
            zipcode = line.strip().split(",")[0]
            slcsp_zipcodes.append(zipcode)

    return slcsp_zipcodes


def get_rate_area_by_zipcode():
    rate_area_by_zip = defaultdict(set())
    with open(zipcodes_path, "r") as zip_in:
        header = next(zip_in)
        for line in zip_in:
            zipcode, state, cc, name, rate_area = line.strip().split(",")
            rate_area_by_zip[zipcode].add((state, rate_area))


if __name__ == "__main__":
    rates_by_rate_area = get_plan_rates_by_rate_area()
    slcsp_zipcodes = get_slcsp_zipcodes()
    rate_area_by_zip = get_rate_area_by_zipcode()
    output = []
    for zipcode in slcsp_zipcodes:
        rate_areas = rate_area_by_zip.get(zipcode, set())
        if len(rate_areas) != 1:
            output.append((zipcode, ""))
            continue
        state, rate_area = next(iter(rate_areas))
        rates = sorted(set(rates_by_rate_area.get((state, rate_area), [])))
        if len(rates) < 2:
            output.append((zipcode, ""))


class TestCalculator:

    def test_get_plan_rates_by_rate_area(self):
        rates_by_rate_area = get_plan_rates_by_rate_area()
        assert ("MO", "3") in rates_by_rate_area
        assert ("PA", "7") in rates_by_rate_area

    def test_get_slcsp_zipcodes(self):
        slcsp_zipcodes = get_slcsp_zipcodes()
        assert "64148" in slcsp_zipcodes

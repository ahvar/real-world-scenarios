from collections import defaultdict
from pathlib import Path

plans_path = (Path(__file__).parent.parent / "data" / "plans.csv").resolve()
slcsp_path = (Path(__file__).parent.parent / "data" / "slcsp.csv").resolve()
zipcode_path = (Path(__file__).parent.parent / "data" / "zips.csv").resolve()


def parse_plans():
    rates_by_rate_area = defaultdict(list)
    with open(plans_path, "r") as plans_in:
        plans_header = next(plans_in)
        for line in plans_in:
            plan_id, state, metal_level, rate, rate_area = line.strip().split(",")
            if metal_level == "Silver":
                rates_by_rate_area[(state, rate_area)].append(float(rate))
    return rates_by_rate_area


def parse_slcsp_zips():
    slcsp_zipcodes = []
    with open(slcsp_path, "r") as slcsp_in:
        slcsp_header = next(slcsp_in)
        for line in slcsp_in:
            slcsp_zipcode = line.strip().split(",")[0]
            slcsp_zipcodes.append(slcsp_zipcode)
    return slcsp_zipcodes


def parse_zipcodes():
    rate_areas_by_zipcode = defaultdict(set)
    with open(zipcode_path, "r") as zips_in:
        zips_header = next(zips_in)
        for line in zips_in:
            zipcode, state, cc, name, rate_area = line.strip().split(",")
            rate_areas_by_zipcode[zipcode].add((state, rate_area))
    return rate_areas_by_zipcode


if __name__ == "__main__":
    rates_by_rate_area = parse_plans()
    slcsp_zips = parse_slcsp_zips()
    rate_areas_by_zipcode = parse_zipcodes()
    output = []
    for zip in slcsp_zips:
        # use the zipcode to get the state and rate_area
        rate_areas = rate_areas_by_zipcode.get(zip, set())
        if len(rate_areas) != 1:
            output.append((zip, ""))
            continue
        state, rate_area = next(iter(rate_areas))
        rates = sorted(set(rates_by_rate_area.get((state, rate_area), [])))
        if len(rates) < 2:
            output.append((zip, ""))
        else:
            output.append((zip, f"{rates[1]:.2f}"))


class TestSLCSPCalculator:

    def test_parse_plans(self):
        rates_by_rate_area = parse_plans()
        assert ("KS", "9") in rates_by_rate_area
        assert ("MO", "3") in rates_by_rate_area
        assert ("FL", "12") in rates_by_rate_area

    def test_parse_slcsp_zips(self):
        slcsp_zips = parse_slcsp_zips()
        for zip in ("64148", "40813", "41101"):
            assert zip in slcsp_zips

    def test_parse_zipcodes(self):
        rate_areas_by_zipcode = parse_zipcodes()
        assert rate_areas_by_zipcode.get("64148") == ("MO", "3")

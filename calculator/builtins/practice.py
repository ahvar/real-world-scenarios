from collections import defaultdict
from pathlib import Path


class SLCSPCalculator:

    def __init__(self):
        self._plans_path = Path(__file__).parent.parent / "data" / "plans.csv"
        self._slcsp_zip = Path(__file__).parent.parent / "data" / "slcsp.csv"
        self._zips_path = Path(__file__).parent.parent / "data" / "zips.csv"
        self._plan_rate_by_rate_area = defaultdict(list)
        self._slcsp_zipcodes = []
        self._rate_area_by_zipcode = defaultdict(set)
        self._output = []

    def read_plans(self):
        with open(self._plans_path, "r") as plans_in:
            header = next(plans_in)
            for line in plans_in:
                plan_id, state, metal_level, rate, rate_area = line.strip().split(",")
                if metal_level.lower() == "silver":
                    self._plan_rate_by_rate_area[(state, rate_area)] = float(rate)

    def read_slcsp_zip(self):
        with open(self._slcsp_zip, "r") as slcsp_zip_in:
            header = next(slcsp_zip_in)
            for line in slcsp_zip_in:
                zipcode = line.strip().split(",")[0]
                self._slcsp_zipcodes.append(zipcode)

    def read_zips(self):
        with open(self._zips_path, "r") as zips_in:
            header = next(zips_in)
            for line in zips_in:
                zipcode, state, cc, name, rate_area = line.strip().split(",")
                self._rate_area_by_zipcode[zipcode].add((state, rate_area))

    def calculate_slcsp(self):
        for zipcode in self._slcsp_zipcodes:
            rate_area = self._rate_area_by_zipcode.get(zipcode, set())
            if len(rate_area) != 1:
                self._output.append((zipcode, ""))
                continue
            state, rate_area = next(iter(rate_area))
            rates = sorted(self._plan_rate_by_rate_area[(state, rate_area)])
            if len(rates) < 2:
                self._output.append((zipcode, ""))
            else:
                self._output.append((zipcode, f"{rates[1]:.2f}"))

    @property
    def plans(self):
        return self._plan_rate_by_rate_area

    @property
    def slcsp_zip(self):
        return self._slcsp_zipcodes

    @property
    def zipcodes(self):
        return self._rate_area_by_zipcode


class TestSlcspCalculator:

    def setup_method(self):
        self.slcsp_calculator = SLCSPCalculator()

    def test_read_plans(self):
        self.slcsp_calculator.read_plans()
        assert ("MO", "3") in self.slcsp_calculator.plans

    def test_read_slcsp_zip(self):
        self.slcsp_calculator.read_slcsp_zip()
        assert "64148" in self.slcsp_calculator.slcsp_zip

    def test_read_zips(self):
        self.slcsp_calculator.read_zips()
        assert "64148" in self.slcsp_calculator.zipcodes
        assert self.slcsp_calculator.zipcodes["64148"] == {("MO", "3")}

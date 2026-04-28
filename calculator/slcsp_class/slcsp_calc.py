from pathlib import Path
from collections import defaultdict

data_path = Path(__file__).parent.parent / "data"


class Calculator:

    def __init__(self):
        self._plan_rates = defaultdict(list)
        self._slcsp_zipcodes = []
        self._rate_areas = defaultdict(set)
        self._output = []

        for filename in ("plans.csv", "slcsp.csv", "zips.csv"):
            self.read_data(filename)

    def read_data(self, filename):
        with open(data_path / filename, "r") as file_in:
            header = next(file_in)
            if filename == "plans.csv":
                for line in file_in:
                    plan_id, state, metal_level, rate, rate_area = line.strip().split(
                        ","
                    )
                    if metal_level.lower() == "silver":
                        self._plan_rates[(state, rate_area)].append(float(rate))
            elif filename == "slcsp.csv":
                for line in file_in:
                    zipcode = line.strip().split()[0]
                    self._slcsp_zipcodes.append(zipcode)
            elif filename == "zips.csv":
                for line in file_in:
                    zipcode, state, cc, name, rate_area = line.strip().split(",")
                    self._rate_areas[zipcode].add((state, rate_area))

    def calculate_slcsp(self):
        for zipcode in self._slcsp_zipcodes:
            rate_areas = self._rate_areas.get(zipcode, set())
            if len(rate_areas) != 1:
                self._output.append((zipcode, ""))
                continue
            state, rate_area = rate_areas
            rates = sorted(set(self._plan_rates.get((state, rate_area), [])))
            if len(rates) < 2:
                self._output.append((zipcode, ""))
            else:
                self._output.append((zipcode, f"{rates[1]:.2f}"))


class TestCalculator:
    def setup_method(self):
        self.calculator = Calculator()

    def test_read_data(self):
        assert ("MO", "3") in self.calculator._plan_rates
        assert "64148" in self.calculator._slcsp_zipcodes

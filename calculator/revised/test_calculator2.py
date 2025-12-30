import pytest
from calculator2 import get_rates_by_rate_area


class TestSLCSPCalculator:

    def test_get_rates_by_rate_area(self):
        rates_by_rate_area = get_rates_by_rate_area()
        assert ("KS", "9") in rates_by_rate_area
        assert ("KY", "4") in rates_by_rate_area

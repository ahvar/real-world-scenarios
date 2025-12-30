import pytest

from attempt import get_users_by_customer


class TestAttempt:

    def test_get_users_by_customer(self):
        users_by_customer = get_users_by_customer()
        assert 1 in users_by_customer
        assert 2 in users_by_customer
        assert 3 in users_by_customer
        assert 4 in users_by_customer

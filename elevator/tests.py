from practice import Elevator, Request, RequestType
import pytest


class TestElevator:
    def setup_method(self):
        self._elevator = Elevator()

    def test_add_request(self):
        # add nominal
        request = Request(2, RequestType.PICKUP_UP)
        self._elevator.add_request(request)
        assert len(self._elevator.requests) == 1

        request2 = Request(-1, RequestType.PICKUP_UP)
        self._elevator.add_request(request2)
        assert len(self._elevator.requests) == 1

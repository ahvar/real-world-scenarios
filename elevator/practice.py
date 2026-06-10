from enum import Enum


class RequestType(Enum):
    PICKUP_UP = 1
    PICkUP_DOWN = 2
    DESTINATION = 3


class Direction(Enum):
    UP = "UP"
    DOWN = "DOWN"
    IDLE = "IDLE"


class Request:
    def __init__(self, floor, request_type):
        self._floor = floor
        self._type = request_type

    @property
    def floor(self):
        return self._floor

    @property
    def request_type(self):
        return self._request_type

    def __eq__(self, other):
        return other.floor == self._floor and other.request_type == self._request_type

    def __hash__(self):
        pass


class Elevator:
    def __init__(self):
        self._current_floor = 0
        self._direction = Direction.IDLE
        self._requests = set()

    def add_request(self, request) -> bool:
        if not 0 <= request.floor <= 9:
            return False
        if request.floor == self._current_floor:
            return True
        if request in self._requests:
            return False
        self._requests.add(request)
        return True

    def step(self):
        if not self._requests:
            self._direction = Direction.IDLE
            return
        if self._direction.IDLE:
            nearest = self._get_nearest()
            if nearest.floor > self._current_floor:
                self._direction = Direction.UP
            else:
                self._direction = Direction.DOWN
        pickup_type = (
            RequestType.PICKUP_UP
            if self._direction == Direction.UP
            else RequestType.PICkUP_DOWN
        )
        pickup_request = Request(self._current_floor, pickup_type)
        destination_request = Request(self._current_floor, RequestType.DESTINATION)

    def _get_nearest(self):
        min_diff = int("inf")
        nearest = None
        for r in self._requests:
            if not nearest:
                nearest = r
                continue
            curr_diff = abs(self._current_floor - r.floor)
            if curr_diff == min_diff:
                nearest = r if r.floor < nearest.floor else nearest
            elif curr_diff < min_diff:
                min_diff = curr_diff
                nearest = r
        return nearest

    def has_requests_ahead(self, direction):
        pass

    def has_requests_at_or_beyond(self, floor, direction):
        pass

    @property
    def current_floor(self):
        return self._current_floor

    @property
    def direction(self):
        return self._direction


class ElevatorController:

    def __init__(self):
        self._elevators = []

    def request_elevator(self, floor, request_type):
        pass

    def step(self):
        pass

    def select_best_elevator(self, request):
        pass

    def find_committed_to_floor(self, request):
        pass

    def find_nearest_idle(self, floor):
        pass

    def find_nearest(self, floor):
        pass

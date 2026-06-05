from enum import Enum


class Direction(Enum):
    UP = "UP"
    DOWN = "DOWN"
    IDLE = "IDLE"


class RequestType(Enum):
    PICKUP_UP = "PICKUP_UP"
    PICKUP_DOWN = "PICKUP_DOWN"
    DESTINATION = "DESTINATION"


class Request:
    def __init__(self, floor, type):
        self._floor = floor
        self._type = type

    @property
    def floor(self):
        return self._floor

    @property
    def type(self):
        return self._type

    def __eq__(self, other):
        return self._floor == other.floor and self._type == other.type

    def __hash__(self):
        return hash((self._floor, self._type))


class Elevator:
    def __init__(self):
        self._current_floor = 0
        self._requests = set()
        self._direction = Direction.IDLE

    def add_request(self, request):
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
        if self._direction == Direction.IDLE:
            closest = sorted(
                (r for r in self._requests),
                key=lambda x: abs(x.floor - self._current_floor),
            )[0]

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

    @property
    def requests(self):
        return self._requests


class ElevatorController:

    def __init__(self):
        self._elevators = [Elevator()] * 3

    def request_elevator(self, floor, type):
        if not isinstance(type, RequestType):
            return
        request = Request(floor, type)
        elevator = self.select_best_elevator(request)
        elevator.add_request(request)

    def step(self):
        pass

    def select_best_elevator(self, request) -> Elevator:
        pass

    def find_committed_to_floor(self, request):
        pass

    def find_nearest_idle(self, floor):
        pass

    def find_nearest(self, floor):
        pass


if __name__ == "__main__":
    controller = ElevatorController()

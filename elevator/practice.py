from enum import Enum
from typing import Set, List
from dataclasses import dataclass


class Direction(Enum):
    UP = 1
    DOWN = 2
    IDLE = 3


class RequestType(Enum):
    PICKUP_UP = 1
    PICKUP_DOWN = 2
    DESTINATION = 3

class Request:
    def __init__(self, floor: int, type: RequestType):
        self.floor = floor
        self.type = type
    
    def get_floor(self) -> int:
        return self.floor
    
    def get_type(self) -> RequestType:
        return self.type

    def __eq__(self, other):
        if not isinstance(other, Request):
            return False
        return self.floor == other.floor and self.type == other.type

    def __hash__(self):
        return hash((self.floor, self.type))


class Elevator:

    def __init__(self):
        self._current_floor = 0
        self._direction = Direction.IDLE
        self._requests = set()

    def add_request(self, request: RequestType) -> bool:
        pass

    def step(self):
        pass


class ElevatorController:

    def __init__(self):
        self._elevators: List[Elevator] = []

    def request_elevator(self, floor, request_type):
        if floor < 0 or floor > 9:
            return False
        if request_type == 

    def request_destination(self, elevator_id, floor) -> bool:
        pass


class ElevatorUser:
    pass

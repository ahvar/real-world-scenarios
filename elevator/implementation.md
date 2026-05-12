# Elevator Implementation Guide

This guide is meant to help you implement the system yourself without reading the reference solution first.

## 1. Core Types To Define

The official solution uses four core types:

### `RequestType`

Purpose:

- distinguishes the three kinds of requests the system understands

Members:

- `PICKUP_UP`
- `PICKUP_DOWN`
- `DESTINATION`

### `Request`

Purpose:

- represents one stop request as a `(floor, type)` pair
- allows requests to be stored in a `set`

Attributes:

- `floor`: requested floor number
- `type`: one of the `RequestType` enum values

Member functions:

- `__init__(floor, type)`
- `get_floor()`
- `get_type()`
- `__eq__(other)`
- `__hash__()`

### `Direction`

Purpose:

- represents the current motion state of an elevator

Members:

- `UP`
- `DOWN`
- `IDLE`

`IDLE` is required so an elevator with no active work has a clean state.

### `Elevator`

Purpose:

- tracks one elevator's state
- owns movement logic and stop logic

Attributes:

- `current_floor`: current location of the elevator
- `direction`: current `Direction`
- `requests`: a `set` of `Request` objects

Member functions:

- `__init__()`
- `add_request(request)`
- `step()`
- `has_requests_ahead(direction)`
- `has_requests_at_or_beyond(floor, direction)`
- `get_current_floor()`
- `get_direction()`

### `ElevatorController`

Purpose:

- owns the system's elevators
- accepts hall calls
- selects which elevator should handle a hall call
- advances the full simulation

Attributes:

- `elevators`: a list containing the three `Elevator` objects

Member functions:

- `__init__()`
- `request_elevator(floor, type)`
- `step()`
- `select_best_elevator(request)`
- `find_committed_to_floor(request)`
- `find_nearest_idle(floor)`
- `find_nearest(floor)`

## 2. How The Objects Work Together

- `ElevatorController` receives hall calls from outside the elevator.
- It wraps each hall call in a `Request`.
- It chooses the best elevator for that request.
- It delegates the request to that elevator through `add_request()`.
- Each elevator owns its own `step()` logic and moves independently.

In this official solution, destination requests are modeled with `RequestType.DESTINATION`, but there is no separate `controller.request_destination(...)` API. A destination request is still just a `Request` added to an elevator.

## 3. Class-By-Class Implementation Plan

### `RequestType`

Implementation steps:

1. Define an enum named `RequestType`.
2. Add three values: `PICKUP_UP`, `PICKUP_DOWN`, and `DESTINATION`.
3. Use numeric enum values, matching the official solution.

### `Request`

Implementation steps:

1. Store `floor` and `type` in the constructor.
2. Add `get_floor()` so callers do not reach into the attribute directly.
3. Add `get_type()` for the same reason.
4. Implement `__eq__()` so two requests compare equal when both floor and type match.
5. Implement `__hash__()` so `Request` can live inside a `set`.

Why this matters:

- the elevator stores requests in a set
- set membership and deduplication depend on correct equality and hashing

### `Direction`

Implementation steps:

1. Define an enum named `Direction`.
2. Add `UP`, `DOWN`, and `IDLE`.
3. Use `IDLE` as the default state for new elevators.

### `Elevator.__init__()`

Implementation steps:

1. Initialize `current_floor` to `0`.
2. Initialize `direction` to `Direction.IDLE`.
3. Initialize `requests` to an empty set.

### `Elevator.add_request(request)`

Purpose:

- validates and stores one request for this elevator

Implementation steps:

1. Reject the request if the floor is outside `0..9`.
2. If the request is for the current floor, return `True` as a successful no-op.
3. If the exact request is already present, return `False`.
4. Otherwise add the request to the set and return `True`.

### `Elevator.step()`

Purpose:

- advance one elevator by one simulation tick

Implementation steps:

1. If there are no requests, set direction to `IDLE` and return.
2. If direction is `IDLE`, scan the request set and choose the nearest request.
3. Use distance from `current_floor` as the primary comparison.
4. If two requests are equally near, choose the lower floor as the tie-breaker.
5. Set direction to `UP` if the chosen request is above the current floor, otherwise set it to `DOWN`.
6. Build the two requests that could be served at the current floor:
	`pickup_request = Request(current_floor, PICKUP_UP or PICKUP_DOWN depending on direction)` and `destination_request = Request(current_floor, DESTINATION)`.
7. If either of those requests is in the set, remove them.
8. If removing them leaves no requests, set direction to `IDLE`.
9. Return immediately after stopping. Do not move on the same tick.
10. If nothing should be served now, call `has_requests_ahead(direction)`.
11. If there is nothing ahead in the current direction, reverse the direction and return.
12. Otherwise move exactly one floor in the current direction.

Important behavior:

- an elevator can travel toward a floor without stopping there yet
- when moving up, it does not stop for `PICKUP_DOWN`
- when moving down, it does not stop for `PICKUP_UP`

### `Elevator.has_requests_ahead(direction)`

Purpose:

- decides whether the elevator should keep moving in its current direction

Implementation steps:

1. Loop through every request in the set.
2. If direction is `UP`, return `True` if any request floor is above `current_floor`.
3. If direction is `DOWN`, return `True` if any request floor is below `current_floor`.
4. If no request qualifies, return `False`.

This method checks any request ahead, regardless of request type.

### `Elevator.has_requests_at_or_beyond(floor, direction)`

Purpose:

- helps the controller decide whether a moving elevator is already committed to a path that reaches the requested floor

Implementation steps:

1. Loop through each request in the elevator.
2. For `UP`, check whether any request is at or above the requested floor and is either `PICKUP_UP` or `DESTINATION`.
3. For `DOWN`, check whether any request is at or below the requested floor and is either `PICKUP_DOWN` or `DESTINATION`.
4. Return `True` as soon as such a request is found.
5. Otherwise return `False`.

This is what makes the official dispatch strategy more precise than simple "moving toward the floor" logic.

### `Elevator.get_current_floor()` and `Elevator.get_direction()`

Purpose:

- expose the minimum state the controller needs for dispatch decisions

Implementation steps:

1. Return `current_floor` from `get_current_floor()`.
2. Return `direction` from `get_direction()`.

### `ElevatorController.__init__()`

Implementation steps:

1. Create exactly three `Elevator` objects.
2. Store them in `self.elevators` as a list.

### `ElevatorController.request_elevator(floor, type)`

Purpose:

- entry point for hall calls from building floors

Implementation steps:

1. Reject the request if the floor is outside `0..9`.
2. Reject the request if the type is `DESTINATION`.
3. Wrap the call as `Request(floor, type)`.
4. Call `select_best_elevator(request)`.
5. If no elevator is returned, return `False`.
6. Otherwise pass the request into that elevator's `add_request()` and return the result.

### `ElevatorController.step()`

Purpose:

- advances the full system by one tick

Implementation steps:

1. Loop through `self.elevators`.
2. Call `step()` on each one.

### `ElevatorController.select_best_elevator(request)`

Purpose:

- centralizes dispatch strategy

Implementation steps:

1. First call `find_committed_to_floor(request)`.
2. If it returns an elevator, use it.
3. Otherwise call `find_nearest_idle(request.get_floor())`.
4. If that returns an elevator, use it.
5. Otherwise fall back to `find_nearest(request.get_floor())`.

### `ElevatorController.find_committed_to_floor(request)`

Purpose:

- finds a moving elevator that is already headed in the correct direction and already committed to passing or reaching the requested floor

Implementation steps:

1. Read the floor from the request.
2. Convert request type to the matching `Direction`.
3. Loop through all elevators.
4. Skip elevators whose current direction does not match.
5. Skip elevators that have already passed the floor.
6. Skip elevators that are not committed to going at or beyond that floor by calling `has_requests_at_or_beyond(floor, direction)`.
7. Among the remaining elevators, choose the one with the smallest distance to the floor.
8. Return that elevator, or `None` if none qualify.

### `ElevatorController.find_nearest_idle(floor)`

Purpose:

- finds the closest idle elevator

Implementation steps:

1. Loop through all elevators.
2. Consider only those whose direction is `IDLE`.
3. Track the one with the minimum distance from the requested floor.
4. Return it, or `None` if no idle elevator exists.

### `ElevatorController.find_nearest(floor)`

Purpose:

- fallback dispatch when no committed or idle elevator is available

Implementation steps:

1. Start with the first elevator as the current best candidate.
2. Compute its distance from the floor.
3. Loop through all elevators.
4. If any elevator is closer, replace the current best candidate.
5. Return the nearest elevator.

## 4. Recommended Build Order

1. Define `RequestType` and `Direction`.
2. Implement `Request` including equality and hashing.
3. Implement the `Elevator` constructor and `add_request()`.
4. Implement `has_requests_ahead()` and `has_requests_at_or_beyond()`.
5. Implement `step()` for the elevator.
6. Implement the controller constructor and `step()`.
7. Implement `request_elevator()`.
8. Implement `select_best_elevator()` and the three helper selection methods.

## 5. Common Failure Modes In This Solution

- forgetting to implement `__hash__()` on `Request`
- forgetting that duplicate requests should return `False` in `add_request()`
- moving on the same tick that the elevator stops
- reversing and moving in the same tick
- stopping for `PICKUP_DOWN` while moving `UP`, or vice versa
- using only direction matching in dispatch and omitting the `has_requests_at_or_beyond()` commitment check

If you follow the structure above, your implementation will match the official solution closely, including the extra dispatch precision used by `find_committed_to_floor()`.
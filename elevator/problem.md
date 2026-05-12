# Elevator System Practice Problem

Design an elevator control system for a building.

The system should simulate multiple elevators serving multiple floors. It must accept hall calls from building floors, accept destination selections from inside an elevator, and advance time in discrete ticks.

## Requirements

Implement a simulation with these fixed constraints:

- The building has 10 floors, numbered `0` through `9`.
- The system manages 3 elevators.
- Each elevator starts at floor `0`.
- A person on a floor can request an elevator by pressing either `UP` or `DOWN`.
- Once inside an elevator, a passenger can request one or more destination floors.
- The controller decides which elevator should handle each hall call.
- The simulation advances one unit at a time through a `step()` method.
- The system must support multiple outstanding requests at once.

## Request Types

There are two categories of stops:

- Hall call: a floor plus a direction (`UP` or `DOWN`)
- Destination: a floor selected from inside an elevator

Hall calls are direction-sensitive. If an elevator is moving up, it should not stop to pick up a passenger waiting to go down unless it has reversed and is now traveling down.

## Validation Rules

- Invalid floor numbers should be rejected.
- Invalid request types should be rejected.
- Requesting the current floor should be treated as a no-op that succeeds.
- Duplicate requests should not create duplicate work.

## Out Of Scope

Do not model any of the following:

- Elevator capacity or weight limits
- Door state or door timing
- Emergency stop behavior
- Hardware integration or concurrency primitives
- Dynamic configuration of floor or elevator counts
- UI or rendering

## Behavior Expectations

The core movement behavior should be efficient and predictable:

- An elevator continues in its current direction while there is still work ahead.
- It stops for matching hall calls in its direction of travel.
- It always stops for destination requests at its current floor.
- When there is no more work ahead in its current direction, it reverses.
- When there are no pending requests at all, it becomes idle.

## Example Scenario

1. Elevator A is idle at floor `0`.
2. Someone on floor `4` requests `UP`.
3. The controller dispatches an elevator and adds that hall call.
4. A few ticks later, the elevator reaches floor `4` and stops.
5. The passenger enters and selects floor `8`.
6. The elevator continues upward until it reaches floor `8`, then stops.
7. If no more requests remain, the elevator becomes idle.
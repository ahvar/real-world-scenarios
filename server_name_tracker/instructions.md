# Server Name Tracker

## Overview

You are implementing a small server-name allocation system.

A hostname is made from:
- A host type (e.g., `"api"`, `"web"`, `"db"`)
- Followed immediately by a positive integer ID starting at 1

**Examples:** `api1`, `api2`, `web1`, `db12`

## Classes to Implement

You must implement three classes:

1. **`Tracker`** (base class)
2. **`SilentTracker`** (inherits `Tracker`)
3. **`NonSilentTracker`** (inherits `Tracker`)

### Methods

Each tracker supports:
- `allocate(hostType) -> str`
- `deallocate(hostName) -> None`

Trackers start empty (no servers allocated at construction time).

## Hostname Rules

A hostname is considered validly formatted if:
- `hostType` is one or more letters (you can assume lowercase letters if you want)
- The numeric suffix is an integer ≥ 1
- No leading zeros in the numeric part (`api01` is invalid)

**Valid:**
- ✅ `api1`, `web12`

**Invalid:**
- ❌ `api0`, `api01`, `1api`, `api`, `api-1`

If a malformed hostname is passed to `deallocate`, treat it as an invalid operation.

## Allocation Behavior

`allocate(hostType)` must return a hostname that:
- Uses the provided `hostType`
- Uses the smallest positive integer not currently allocated for that host type

### Example (starting from empty):

```python
allocate("api")     # → api1
allocate("api")     # → api2
deallocate("api1")
allocate("api")     # → api1 (reuses the freed smallest id)
```

### Important:
- Allocation is tracked per host type independently
- `api1` and `web1` can both exist at the same time

## Deallocation Behavior

`deallocate(hostName)` should "free" that hostname so it can be reused later.

If `hostName` is not currently allocated (or is malformed), that is an invalid operation, and the behavior depends on the subclass:

### SilentTracker

Invalid deallocation is a no-op (do nothing) and returns `None`.

### NonSilentTracker

Invalid deallocation must raise an error (any exception type is OK) with a message like:
```
"Invalid Operation"
```

### Examples of Invalid Deallocation:
- Deallocating a name that was never allocated (`api99`)
- Deallocating a name twice (`api1` deallocated two times)
- Malformed hostname (`api01`, `api`, `api0`, etc.)

## Performance Requirement

Assume up to **~100k operations**. Your solution should be efficient (avoid scanning from 1 every time).

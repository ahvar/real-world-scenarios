import heapq
import re
from abc import ABC, abstractmethod


class Tracker(ABC):
    def __init__(self):
        self._host_types = {}

    def _bucket(self, host_type: str):
        if host_type not in self._host_types:
            self._host_types[host_type] = {
                "next_id": 1,
                "free_ids": [],
                "allocated": set(),
            }
        return self._host_types[host_type]

    def _parse_hostname(self, host_name):
        """Parse hostname, return (host_type, num) or None if invalid."""
        m = re.fullmatch(r"([a-zA-Z]+)([1-9]\d*|0)", host_name)
        if not m:
            return None
        host_type = m.group(1)
        num_str = m.group(2)
        num = int(num_str)

        # Check for invalid cases: 0 or leading zeros
        if num < 1:
            return None
        if len(num_str) > 1 and num_str[0] == "0":
            return None

        return host_type, num

    @abstractmethod
    def allocate(self, hostType: str) -> str:
        """
        Return the allocated hostname (e.g., 'api1').
        Must allocate the smallest available positive integer for this hostType.
        """
        pass

    @abstractmethod
    def deallocate(self, hostName: str) -> None:
        """
        Free hostName if currently allocated.
        If invalid operation, defer to self._on_invalid_operation().
        """
        pass


class SilentTracker(Tracker):
    """Tracker that silently ignores invalid deallocation operations."""

    def allocate(self, hostType: str) -> str:
        bucket = self._bucket(hostType)

        if bucket["free_ids"]:
            server_id = heapq.heappop(bucket["free_ids"])
        else:
            server_id = bucket["next_id"]
            bucket["next_id"] += 1

        bucket["allocated"].add(server_id)
        return f"{hostType}{server_id}"

    def deallocate(self, hostName: str) -> None:
        # Parse hostname - if invalid, silently return
        parsed = self._parse_hostname(hostName)
        if parsed is None:
            return

        host_type, num = parsed

        # If host type doesn't exist, silently return
        if host_type not in self._host_types:
            return

        bucket = self._host_types[host_type]

        # If not allocated, silently return
        if num not in bucket["allocated"]:
            return

        # Valid deallocation
        bucket["allocated"].remove(num)
        heapq.heappush(bucket["free_ids"], num)


class NonSilentTracker(Tracker):
    """Tracker that raises an exception on invalid deallocation operations."""

    def allocate(self, hostType: str) -> str:
        bucket = self._bucket(hostType)

        if bucket["free_ids"]:
            server_id = heapq.heappop(bucket["free_ids"])
        else:
            server_id = bucket["next_id"]
            bucket["next_id"] += 1

        bucket["allocated"].add(server_id)
        return f"{hostType}{server_id}"

    def deallocate(self, hostName: str) -> None:
        # Parse hostname - if invalid, raise exception
        parsed = self._parse_hostname(hostName)
        if parsed is None:
            raise Exception("Invalid Operation")

        host_type, num = parsed

        # If host type doesn't exist, raise exception
        if host_type not in self._host_types:
            raise Exception("Invalid Operation")

        bucket = self._host_types[host_type]

        # If not allocated, raise exception
        if num not in bucket["allocated"]:
            raise Exception("Invalid Operation")

        # Valid deallocation
        bucket["allocated"].remove(num)
        heapq.heappush(bucket["free_ids"], num)

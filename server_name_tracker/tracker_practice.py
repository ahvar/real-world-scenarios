import heapq
import re
from abc import ABC, abstractmethod


class Tracker(ABC):
    def __init__(self):
        # TODO: initialize your data structures
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
        m = re.fullmatch(f"([A-Za-z]+)([0-9])", host_name)
        if not m:
            raise ValueError("malformed hostname")
        host_type = m.group(1)
        num_str = m.group(2)

        if len(num_str) > 1 and num_str[0] == "0":
            raise ValueError("Leading zeros not allowed")

        num = int(num_str)
        if num < 1:
            raise ValueError("ID must be >= 1")
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

    def _on_invalid_operation(self) -> None:
        """
        Hook method. Base class doesn't decide behavior.
        Subclasses MUST override.
        """
        raise NotImplementedError


class SilentTracker(Tracker):

    def __init__(self):
        super().__init__()

    def allocate(self, hostType: str) -> str:
        """
        Return the allocated hostname (e.g., 'api1').
        Must allocate the smallest available positive integer for this hostType.
        """

        bucket = self._bucket(hostType)

        if bucket["free_ids"]:
            server_id = heapq.heappop(bucket["free_ids"])
        else:
            server_id = bucket["next_id"]
            bucket["next_id"] += 1

        bucket["allocated"].add(server_id)

        return f"{hostType}{server_id}"

    def deallocate(self, hostName: str) -> None:
        """
        Free hostName if currently allocated.
        If invalid operation, defer to self._on_invalid_operation().
        """
        try:
            host_type, num = self._parse_hostname(hostName)
        except ValueError:
            self._on_valid_operation()
            return

        if host_type not in self._host_types:
            self._on_invalid_operation()
            return

        bucket = self._host_types[host_type]

        if num not in bucket["allocated"]:
            self._on_invalid_operation()
            return

        bucket["allocated"].remove(num)

        heapq.heappush(bucket["free_ids"], num)

        return None


class NonSilentTracker(Tracker):

    def __init__(self):
        super().__init__()

    def allocate(self, hostType: str) -> str:
        """
        Return the allocated hostname (e.g., 'api1').
        Must allocate the smallest available positive integer for this hostType.
        """
        # TODO
        raise NotImplementedError

    def deallocate(self, hostName: str) -> None:
        """
        Free hostName if currently allocated.
        If invalid operation, defer to self._on_invalid_operation().
        """
        # TODO
        raise NotImplementedError

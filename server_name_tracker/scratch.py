from collections import defaultdict
from abc import ABC, abstractmethod
import re
import heapq


class Tracker(ABC):
    def __init__(self):
        """
        - _hosttypes manages the host types and ids
        """
        super().__init__()
        self._hosttypes = defaultdict(dict)

    def _bucket(self):
        return {"next_id": 1, "free_ids": [], "allocated": set()}

    @abstractmethod
    def allocate(self):
        pass

    @abstractmethod
    def deallocate(self):
        pass


class SilentTracker(Tracker):

    def allocate(self, hosttype) -> str:
        if hosttype not in self._hosttypes:
            b = self._bucket()
            self._hosttypes[hosttype] = b
            id = b["next_id"]
            b["next_id"] += 1
            b["allocated"].add(id)
            return f"{hosttype}{id}"
        b = self._hosttypes[hosttype]
        if b["free_ids"]:
            id = heapq.heappop(b["free_ids"])
            b["allocated"].add(id)
            return f"{hosttype}{id}"
        id = b["next_id"]
        b["next_id"] += 1
        b["allocated"].add(id)
        return f"{hosttype}{id}"

    def deallocate(self, servername):
        m = re.fullmatch(r"([a-z]+)([1-9][0-9]+)", servername)
        if not m:
            return
        hosttype, id = m.group(1), m.group(2)
        if hosttype not in self._hosttypes:
            return
        b = self._hosttypes[hosttype]
        if id in b["allocated"]:
            b["allocated"].remove(id)
            heapq.heappush(b["free_ids"], id)

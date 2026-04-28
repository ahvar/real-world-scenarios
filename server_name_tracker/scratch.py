from abc import ABC, abstractmethod
import heapq
import re
from collections import defaultdict


class Tracker(ABC):
    def __init__(self):
        """
        :params _hosttypes: dictionary of hosttypes
        """
        self._hosttypes = defaultdict(dict)

    def _bucket(self):
        """
        Return a dict for managing the ids for a new hosttype
        """
        return {"next_id": 1, "free_ids": [], "allocated": set()}

    @abstractmethod
    def allocate(self):
        pass

    @abstractmethod
    def deallocate(self):
        pass

    @property
    def hosttypes(self):
        return self._hosttypes


class SilentTracker(Tracker):
    def __init__(self):
        super().__init__()

    def allocate(self, hosttype):
        # no hosts of this type exist; start tracking
        if hosttype not in self._hosttypes:
            b = self._bucket()
            id = b["next_id"]
            b["next_id"] += 1
            b["allocated"].add(id)
            self._hosttypes[hosttype] = b
            return f"{hosttype}{id}"
        # we're tracking this hosttype and have ids available for assignment
        if self._hosttypes[hosttype]["free_ids"]:
            id = heapq.heappop(self._hosttypes[hosttype]["free_ids"])
            self._hosttypes[hosttype]["allocated"].add(id)
            return f"{hosttype}{id}"
        # we're tracking this hosttype and need to create an id for assignment
        id = self._hosttypes[hosttype]["next_id"]
        self._hosttypes[hosttype]["next_id"] += 1
        self._hosttypes[hosttype]["allocated"].add(id)
        return f"{hosttype}{id}"

    def deallocate(self, servername):
        match = re.fullmatch(r"([a-zA-Z]+)([1-9]\d*|0)", servername)
        if not match:
            return
        hosttype = match.group(1)
        id_str = match.group(2)
        id = int(id_str)

        if hosttype not in self._hosttypes:
            return
        bucket = self._hosttypes[hosttype]
        bucket["allocated"].discard(id)
        heapq.heappush(bucket["free_ids"], id)


class NonSilentTracker(Tracker):
    def __init__(self):
        super().__init__()

    def allocate(self, hosttype):
        pass

    def deallocate(self, servername):
        pass


class TestTracker:

    def setup_method(self):
        pass

    def test_silent_tracker(self):
        self.silent_tracker = SilentTracker()
        self.silent_tracker.allocate("api")
        assert self.silent_tracker.hosttypes["api"] == {
            "next_id": 2,
            "free_ids": [],
            "allocated": {1},
        }

from abc import ABC, abstractmethod
from collections import defaultdict
import heapq


class Tracker(ABC):
    def __init__(self):
        super().__init__()
        self._hosttypes = defaultdict(dict)

    def _bucket(self):
        return {"next_id": 1, "free_ids": [], "allocated": set()}

    def allocate(self, hosttype):
        """"""
        hostname = ""
        # no hostnames of this hosttype yet
        if hosttype not in self._hosttypes:
            b = self._bucket()
            id = b["next_id"]
            b["next_id"] += 1
            b["allocated"].add(id)
            self._hosttypes[hosttype] = b
            return f"{hosttype}{id}"
        # there are free ids that can be used to allocate the next
        # hostname of this hosttype
        if self._hosttypes[hosttype]["free_ids"]:
            id = heapq.heappop(self._hosttypes["hosttype"]["free_ids"])
        # there are no free ids; take the next id
        else:
            id = self._hosttypes[hosttype]["next_id"]
            self._hosttypes[hosttype]["next_id"] += 1
            self._hosttypes[hosttype]["allocated"].add(id)
        hostname = f"{hosttype}{id}"
        return hostname

    @abstractmethod
    def deallocate(self, servername):
        """"""

    @property
    def hosttypes(self):
        return self._hosttypes

    @hosttypes.setter
    def hosttypes(self, hosttypes):
        self._hosttypes = hosttypes


class SilentTracker(Tracker):

    def allocate(self, hosttype):
        super().allocate(hosttype)

    def deallocate(self, hostname):
        return super().deallocate()


class NonSilentTracker(Tracker):

    def allocate(self, hosttype):
        return super().allocate(hosttype)

    def deallocate(self, hostname):
        return super().deallocate()


class TestTracker:
    def setup_method(self):
        self.silent_tracker = SilentTracker()

    def test_add_hosttype(self):
        self.silent_tracker.allocate("api")
        assert len(self.silent_tracker.hosttypes["api"]["allocated"]) == 1
        assert self.silent_tracker.hosttypes["api"]["next_id"] == 2
        assert self.silent_tracker.hosttypes["api"]["allocated"] == {1}

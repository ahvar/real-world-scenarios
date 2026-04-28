from abc import ABC, abstractmethod
from collections import defaultdict
import heapq
import re


class Tracker(ABC):
    def __init__(self):
        super().__init__()
        self._hosttypes = defaultdict(dict)

    def _bucket(self):
        return {"next_id": 1, "free_ids": [], "allocated": set()}

    def allocate(self, hosttype):
        # not tracking servers for hosttype
        if hosttype not in self._hosttypes:
            b = self._bucket()  # new container
            id = b.get("next_id")  # get id for this server
            b["next_id"] += 1  # bump to get next id
            b["allocated"].add(id)  # store curr id as allocated
            self._hosttypes[hosttype].append(b)  # add new hosttype
            return f"{hosttype}{id}"  # return servername
        b = self._hosttypes[hosttype]
        if b["free_ids"]:  # ids available
            id = heapq.heappop(b["free_ids"])  # get next sequential id
            self._hosttypes[hosttype] = b  # NOTE: is this assignment necessary?
            return f"{hosttype}{id}"  # return the server name
        id = b["next_id"]
        b["next_id"] += 1
        b["allocated"].add(id)
        self._hosttypes[hosttype] = b  # NOTE: is this assignment necessary?
        return f"{hosttype}{id}"

    @abstractmethod
    def deallocate(self, hostname):
        pass


class SilentTracker(Tracker):

    def deallocate(self, hostname):
        """ """
        m = re.fullmatch(hostname, r"([a-z]+)([1-9]+)")  # parse the hostname
        if not m:  # return if invalid hostname
            return
        hosttype, id = m.groups()
        b = self._hosttypes.get(hosttype, {})
        if not b:  # not tracking servers for this hosttype
            return
        heapq.heappush(id, b["free_ids"])  # free the id
        b["allocated"].discard(id)  # drop it so we know its available


class NonSilentTracker(Tracker):

    def deallocate(self, hostname):
        super().deallocate(hostname)

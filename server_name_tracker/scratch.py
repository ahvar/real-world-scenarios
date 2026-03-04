from collections import defaultdict
import heapq, re


class Tracker:

    def __init__(self):
        self.hosttypes = {}

    def valid_name(self, hosttype) -> bool:
        pass

    def allocate(self, hosttype) -> str:
        # no servers being tracked for this hosttype
        if hosttype not in self.hosttypes:
            # make a new entry in the hosttypes dict and an object for managing ids
            self.hosttypes[hosttype] = {
                "next_id": 1,
                "free_ids": [],
                "allocated": set(),
            }
            # get the next id; 1 in this case because there are no servers of this hosttype
            id = self.hosttypes[hosttype].get("next_id")
            # add the id to the set of allocated ids for this hosttype
            self.hosttypes[hosttype]["allocated"].add(id)
            # bump the next_id count
            self.hosttypes[hosttype]["next_id"] += 1
            # return the server name
            return f"{hosttype}{id}"

        # there are already servers for this hosttype and there are some ids available to use
        # for this new allocation operation
        if self.hosttypes[hosttype]["free_ids"]:
            # pop the next id off the heap
            id = heapq.heappop(self.hosttypes[hosttype]["free_ids"])
            # add it to the allocated set
            self.hosttypes[hosttype]["allocated"].add(id)
            # return the server name
            return f"{hosttype}{id}"
        if not self.hosttypes[hosttype]["free_ids"]:
            # get the next id
            id = self.hosttypes[hosttype].get("next_id")
            # bump the next id
            self.hosttypes[hosttype]["next_id"] += 1
            # add it to the allocated set
            self.hosttypes[hosttype]["allocated"].add(id)
            return f"{hosttype}{id}"

    def parse_server_name(self, hostname):
        for c in hostname:
            if c.isdigit():
                return hostname[: hostname.index(c)], int(hostname[hostname.index(c) :])

    def parse_server_name_regex(self, servername):
        m = re.match(f"^([a-zA-Z_-]+)(\d+)$", servername)
        if m:
            return m.group(1), int(m.group(2))
        return None, None

    def deallocate(self, hostname):
        # parse hosttype and id
        hosttype, id = self.parse_server_name(hostname)
        if hosttype not in self.hosttypes:
            print(f"error: {hosttype} not allocated")
            return
        # remove id from allocated
        self.hosttypes[hosttype]["allocated"].remove(id)
        # push to the heap; Olog(n) time ?
        heapq.heappush(self.hosttypes[hosttype]["free_ids"], id)


class TestTracker:
    def setup_method(self):
        self.tracker = Tracker()

    def test_allocate(self):
        assert self.tracker.allocate("api") == "api1"
        assert self.tracker.allocate("api") == "api2"
        assert self.tracker.allocate("api") == "api3"

from abc import ABC, abstractmethod
from collections import defaultdict
from flask import render_template
from app.main import bp
import re, heapq


class Tracker(ABC):

    def __init__(self):
        super().__init__()
        self._hosttypes = defaultdict(dict)

    def _bucket(self):
        return {"next_id": 1, "free_ids": [], "allocated": set()}

    def _valid_hosttype(self, hosttype):
        # TODO: FIX!
        m = re.fullmatch(r"[a-z]+")
        if not m:
            return False
        return True

    def allocate(self, hosttype) -> str:
        if not self._valid_hosttype(hosttype):
            return
        if hosttype not in self._hosttypes:
            b = self._bucket()
            id = b["next_id"]
            b["next_id"] += 1
            b["allocated"].add(id)
            self._hosttypes[hosttype] = b
            return f"{hosttype}{id}"
        if self._hosttypes[hosttype]["free_ids"]:
            id = heapq.heappop(self._hosttypes[hosttype]["free_ids"])
            self._hosttypes[hosttype]["allocated"].add(id)
            return f"{hosttype}{id}"
        id = self._hosttypes[hosttype]["next_id"]
        self._hosttypes[hosttype]["next_id"] += 1
        self._hosttypes[hosttype]["allocated"].add(id)
        return f"{hosttype}{id}"

    @abstractmethod
    def deallocate(self, hostname) -> str:
        pass


class SilentTracker(Tracker):

    def deallocate(self, hostname):
        return super().deallocate(hostname)


class NonSilentTracker(Tracker):

    def deallocate(self, hostname):
        return super().deallocate(hostname)


@bp.route("/", methods=["GET", "PUT"])
@bp.route("/index", methods=["GET", "PUT"])
def index():
    return render_template("index.html", messsages=[])

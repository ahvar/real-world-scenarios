from abc import ABC, abstractmethod
from flask import render_template
from app.main import bp
import re
import heapq


@bp.route("/", methods=["GET"])
@bp.route("/index", methods=["GET"])
def index():
    return render_template("index.html", messages=[])


@bp.route("/allocate", methods=["POST"])
def allocate():
    pass


@bp.route("/deallocate/<hostname>")
def deallocate():
    pass


class Tracker(ABC):

    def __init__(self):
        super().__init__()
        self._hosttype = {}

    def _valid_hostname(self, hostname):
        return re.fullmatch(r"([a-z]+)([1-9][0-9]*)", hostname) is not None

    def _valid_hosttype(self, hosttype):
        return re.fullmatch(r"[a-z]+", hosttype) is not None

    def _parse_hostname(self, hostname):
        match = re.fullmatch(r"([a-z]+)([1-9][0-9]*)")
        hosttype = match.group(0)
        id = match.group(1)
        return hosttype, id

    def _deallocate_known(self, hosttype):
        b = self._hosttype.get(hosttype)
        heapq.heappush(b["free_ids"], id)  # free the id
        b["allocated"].discard(id)  # deallocate
        self._hosttype = b  # reassign

    def _bucket(self):
        return {"next_id": 1, "free_ids": [], "allocated": set()}

    def allocate(self, hosttype) -> str:
        if not self._valid_hosttype(hosttype):  # invalid hosttype; no op
            return
        if hosttype not in self._hosttype:  # new hosttype; start tracking
            b = self._bucket()
            id = b["next_id"]
            b["next_id"] += 1
            b["allocated"].add(id)
            self._hosttype[hosttype] = b
            return f"{hosttype}{id}"
        b = self._hosttype[hosttype]  # already tracking this hosttype
        id = None
        if b["free_ids"]:  # free ids available
            id = heapq.heappop(b["free_ids"])
            b["allocated"].add(id)
        else:  # get the next id -> bump it -> allocate it
            id = b["next_id"]
            b["next_id"] += 1
            b["allocated"].add(id)
        return f"{hosttype}{id}"

    @abstractmethod
    def deallocate(self, hostname):
        pass


class SilentTracker(Tracker):

    def deallocate(self, hostname):
        if not self._valid_hostname(hostname):  # invalid hostname; no op
            return
        hosttype, id = self._parse_hostname(hostname)
        if (
            hosttype not in self._hosttype
        ):  # cannot deallocate untracked hosttype; no op
            return
        self._deallocate_known(hosttype)


class NonSilentTracker(Tracker):

    def deallocate(self, hostname):
        if not self._valid_hostname(hostname):  # invalid hostname; no op
            raise Exception("Invalid hostname")
        hosttype, id = self._parse_hostname(hostname)
        if (
            hosttype not in self._hosttype
        ):  # cannot deallocate untracked hosttype; no op
            raise Exception("Hosttype not tracked")
        self._deallocate_known(hosttype)

import heapq
import re
from collections import defaultdict

server_names = defaultdict(lambda: {"next_id": 1, "free_ids": [], "allocated": set()})
HOST_RE = re.compile(f"^([a-zA-Z]+)([1-9][0-9]*)$")


def bucket():
    return {"next_id": 1, "free_ids": [], "allocated": set()}


def allocate(hosttype):
    b = server_names[hosttype]

    if b["free_ids"]:
        id_num = heapq.heappop(b["free_ids"])
    else:
        id_num = b["next_id"]
        b["next_id"] += 1

    b["allocated"].add(id_num)
    return f"{hosttype}{id_num}"


def parse_id(servername):
    m = HOST_RE.fullmatch(servername)
    if not m:
        return None
    hosttype, id_str = m.groups()
    return hosttype, int(id_str)


def deallocate(servername):
    if hosttype not in server_names:
        return
    hosttype, id = parse_id(servername)
    server_names[hosttype]["allocated"].remove(id)
    heapq.heappush(server_names[hosttype]["free_ids"], id)

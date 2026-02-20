import heapq

hosttypes = {}


def bucket():
    return {"next_id": 1, "free_ids": [], "allocated": set()}


def allocate(hosttype):
    server_name = ""
    # if free_ids has something, use the smallest free_id
    if hosttypes[hosttype]["free_ids"]:
        id = heapq.heappop(hosttypes[hosttype]["free_ids"])
    else:
        id = hosttypes[hosttype]["next_id"]
        hosttypes[hosttype]["allocated"].add(id)
        hosttypes[hosttype]["next_id"] += 1


def deallocate(hosttype):
    pass


names = [("api", allocate), ("web", deallocate), ("db", deallocate), ("api", allocate)]

for server, operation in names:
    operation(server)

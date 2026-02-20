from abc import ABC, abstractmethod


class Tracker(ABC):
    def __init__(self):
        super().__init__()

    def allocate(self):
        pass

    def deallocate(self):
        pass

    def _bucket(self):
        return {"next_server_id": 1, "free_ids": [], "allocated": set()}

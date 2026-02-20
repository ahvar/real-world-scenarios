from collections import defaultdict
import heapq


class Potluck:

    def __init__(self):
        self._participants = []
        self._dishes = {}
        self._rounds = []

    def add_participant(self, member_id) -> bool:
        """
        Add participant. If participant already exists, do not
        add and return False

        :param member_id: the participant's member ID
        """
        if member_id in self._participants:
            return False

        self._participants.append(member_id)
        return True

    def remove_participant(self, member_id) -> bool:
        """
        Remove participant and their dish if they brought one.

        :param self: Description
        :param member_id: Description
        :return: Description
        :rtype: bool
        """
        if member_id not in self._participants:
            return False
        if member_id in self._dishes:
            del self._dishes[member_id]
        self._participants.pop(member_id)
        return True

    def add_dish(self, member_id, dish_name):
        if not self._valid_name(member_id):
            return False
        
    def _new_round(self, round_id):
        


    def _current_round(self):
        return heapq.heappop(self._rounds)

    def _valid_name(self, member_id):
        return True

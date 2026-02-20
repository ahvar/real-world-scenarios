from collections import defaultdict
import heapq, re


class Potluck:

    def __init__(self):
        self._participants = set()
        self._dishes = {}
        # self._rounds = []

    def add_participant(self, member_id) -> bool:
        """
        Add participant. If participant already exists, do not
        add and return False

        :param member_id: the participant's member ID
        """
        if not self._valid_name(member_id):
            print("invalid name")
            return False
        if member_id in self._participants:
            print("participant already exists")
            return False

        self._participants.add(member_id)
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
        self._participants.remove(member_id)
        return True

    def add_dish(self, member_id, dish_name) -> bool:
        if not self._valid_name(member_id):
            print("invalid member ID")
            return False
        if member_id in self._dishes:
            print(f"{member_id} already has a dish in this round")
            return False
        self.dishes[member_id] = dish_name
        return True

    def _valid_name(self, member_id):
        """
        Valid member_id can be any alphanumeric combo

        :param self: Description
        :param member_id: Description
        """
        m = re.fullmatch("[A-Za-z0-9]+", member_id)
        return m is not None

    @property
    def participants(self):
        return self._participants

    @participants.setter
    def participants(self, participants):
        self._participants = participants

    @property
    def dishes(self):
        return self._dishes

    @dishes.setter
    def dishes(self, dishes):
        self._dishes = dishes


class TestPotluck:

    def setup_method(self):
        self.potluck = Potluck()
        self.potluck.add_participant("susan")

    def teardown_method(self):
        self.potluck.participants = []
        self.potluck.dishes = {}

    def test_add_participant(self):
        # Test 1: nominal
        assert self.potluck.add_participant("susan1") == True
        assert self.potluck.participants == {"susan", "susan1"}
        # Test 2: invalid character
        assert self.potluck.add_participant("j#ohn") == False
        assert self.potluck.participants == {"susan", "susan1"}

        # Test 3: member already exists
        assert self.potluck.add_participant("susan") == False
        assert self.potluck.participants == {"susan", "susan1"}

    def test_remove_participants(self):
        assert self.potluck.remove_participant("susan") == True
        assert self.potluck.participants == set()

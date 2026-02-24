from collections import defaultdict
from datetime import datetime
from utils.potluck_logger import init_potluck_logger
import heapq, re, logging

cs_pl_logger = logging.getLogger("Potluck")


class Potluck:

    def __init__(self):
        self._participants = {}
        self._dishes = {}
        self._votes = {}
        # self._rounds = []

    def add_participant(self, member_id) -> bool:
        """
        Add participant. If participant already exists, do not
        add and return False

        :param member_id: the participant's member ID
        """
        if not self._valid_name(member_id):
            cs_pl_logger.error("Invalid name: %s", member_id)
            return False
        if member_id in self._participants:
            cs_pl_logger.debug("participant already exists: %s", member_id)
            return False

        self._participants[member_id] = datetime.now()
        cs_pl_logger.info("Participant added: %s", member_id)
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
            cs_pl_logger.debug("This member is not a participant: %s", member_id)
            return False
        if member_id in self._dishes:
            cs_pl_logger.info(
                "Removing this participant's dish: %s", self._dishes[member_id]
            )
            del self._dishes[member_id]
        cs_pl_logger.info("Removing participant: %s", member_id)
        del self._participants[member_id]
        return True

    def add_dish(self, member_id, dish_name) -> bool:
        if not self._valid_name(member_id):
            cs_pl_logger.error(
                "The dish could not be aded because the member name is invalid: %s",
                member_id,
            )
            return False
        if member_id in self._dishes:
            cs_pl_logger.debug("%s already added a dish this round", member_id)
            return False
        if member_id not in self._participants:
            cs_pl_logger.debug(
                "the dish could not be added because the member is not a participant: %s",
                member_id,
            )
            return False
        cs_pl_logger.info("Adding %s's dish: %s", member_id, dish_name)
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

    def vote(self, member_id: str, vote_id: str) -> bool:
        """
        This method will allow a participant to cast a vote for a dish.
        Each participant can cast a vote only once per round. If a participant
        tries to vote again or if the member_id isn't valid, the method returns
        False

        :params member_id: the member id
        :params vote_id: the voter id
        """
        if not self._valid_name(member_id):
            cs_pl_logger.error("Member ID is invalid: %s")
            return False
        if member_id not in self._participants:
            cs_pl_logger.debug("%s is not a participant", member_id)
            return False
        if vote_id in self._votes:
            cs_pl_logger.debug("%s already voted", member_id)
            return False
        cs_pl_logger.info("Casting %s's vote. Vote ID: %s", member_id, vote_id)
        self._votes[member_id] = vote_id
        return True

    def dish_of_the_day(self) -> str:
        """ """

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


if __name__ == "__main__":
    pl_logging_utils = init_potluck_logger()
    potluck = Potluck()
    potluck.add_participant("susan")
    potluck.add_participant("fred")

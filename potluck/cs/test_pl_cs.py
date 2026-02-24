from pl_cs import Potluck


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

    def test_add_dish(self):
        # Test 1: nominal
        assert self.potluck.add_dish("susan", "casserole") == True
        # Test 2: member already added a dish
        assert self.potluck.add_dish("susan", "salad") == False
        # Test 3: non-member
        assert self.potluck.add_dish("mike", "shark") == False

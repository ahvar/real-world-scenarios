import sqlite3


class Potluck:

    def __init__(self, db_path=":memory:"):
        self._dishes = {}
        self._participants = set()
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self._init_db_tables()

    def add_participant(self, member_id: str) -> bool:
        """
        if participant with given id already exists, does
        not add participant, returns False

        :param self: Description
        :param member_id: Description
        :type member_id: str
        :return: Description
        :rtype: bool
        """
        if member_id in self._participants:
            return False
        self._participants.add(member_id)
        try:
            self.cursor.execute("INSERT INTO members(id) VALUES (?)", (member_id,))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def remove_participants(self, member_id: str) -> bool:
        """
        Docstring for remove_participants

        :param self: Description
        :param member_id: Description
        :type member_id: str
        :return: Description
        :rtype: bool
        """
        if member_id not in self._participants:
            return False
        self._participants.remove(member_id)
        if member_id in self._dishes:
            del self._dishes[member_id]

        self.cursor.execute("DELETE FROM members WHERE id = ?", (member_id,))
        self.conn.commit()
        return True

    def add_dish(self, member_id, dish_name) -> bool:
        if self._dishes.get(member_id):
            return False
        self._dishes[member_id] = dish_name

        self.cursor.execute(
            "INSERT INTO dishes(name, member_id) VALUES(?,?)", (dish_name, member_id)
        )
        self.conn.commit()
        return True

    def _init_db_tables(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS dishes(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                member_id TEXT NOT NULL,
                FOREIGN KEY (member_id) REFERENCES members(id) ON DELETE CASCADE
            
            )
            """
        )

        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS members(
                id INTEGER PRIMARY KEY
            )
            """
        )
        self.conn.commit()

    def close(self):
        if self.conn:
            self.conn.close()

    def __enter__(self):
        return self

    def __exit__(self):
        self.close()

    def get_all_participants(self):
        sql = """
        SELECT id 
        FROM members
        """
        self.cursor.execute(sql)
        return [row[0] for row in self.cursor.fetchall()]

    def get_dishes_by_member(self, member_id: str):
        sql = """
        SELECT name
        FROM dishes
        WHERE member_id = ?
        """
        self.cursor.execute(sql, (member_id,))
        return [row[0] for row in self.cursor.fetchall()]

    def get_all_dishes_with_members(self):
        sql = """
        SELECT m.id, d.name
        FROM members m
        JOIN dishes d
        ON m.id = d.member_id
        """
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    @property
    def participants(self):
        return self._participants

    @property
    def dishes(self):
        return self._dishes


class TestPotluck:

    def setup_method(self):
        self._potluck = Potluck()

    def teardown_method(self):
        pass

    def test_add_participant(self):
        self._potluck.add_participant("abc")
        self._potluck.add_participant("def")
        assert len(self._potluck.participants) == 2
        assert self._potluck.add_participant("abc") == False
        assert self._potluck.participants == {"abc", "def"}

    def test_remove_participants(self):
        self._potluck.add_participant("abc")
        self._potluck.add_participant("def")
        self._potluck.add_participant("ghi")
        self._potluck.add_dish("ghi", "lasagna")
        assert self._potluck.dishes == {"ghi": "lasagna"}
        self._potluck.remove_participants("ghi")

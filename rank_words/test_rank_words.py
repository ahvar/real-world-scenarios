import unittest
from rank_words import calculate_word_value


class TestRankWords(unittest.TestCase):

    def test_calculate_word_value(self):
        ab = "ab"
        cab = "cab"
        self.assertEqual(calculate_word_value(ab), 3)
        self.assertEqual(calculate_word_value(cab), 6)

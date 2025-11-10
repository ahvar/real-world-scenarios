import unittest
from rank_words import calculate_word_value


class TestWordRank(unittest.TestCase):

    def test_calculate_word(self):
        ab = "ab"
        self.assertEqual(3, calculate_word_value(ab))

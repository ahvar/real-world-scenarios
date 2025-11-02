import unittest

from rank_words import calculate_word_value


class TestRankWords(unittest.TestCase):
    def setUp(self):
        self.words = ["ab", "bc"]
        self.expected = [3, 4]

    def test_calculate_word_value(self):
        actual = [calculate_word_value(word) for word in self.words]
        self.assertEqual(actual, self.expected)

import sys


def calculate_word_val(word):
    total = 0
    for c in word.lower():
        if c.isalpha():

            total += ord(c) - ord("a") + 1
    return total


if __name__ == "__main__":
    output = []
    input_num = int(sys.stdin.readline())
    for num in input_num:
        word = sys.stdin.readline().strip()
        if calculate_word_val(word) == 100:
            output.append(word)
    output.sort(key=len)
    for word in output:
        print(word)


class TestRankWords:

    def test_calculate_word(self):
        word1 = "ca"
        word2 = "abc"
        assert calculate_word_val(word1) == 4
        assert calculate_word_val(word2) == 6

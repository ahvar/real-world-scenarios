"""
give each letter in each word a numerical value equal to its position in the alphabet.
so "a" is 1 and "z" is 26. Punctuatiion and whitespace is 0. find words where the sum of
the value of the letters is 100. print the list fo words ordered from shortest to longest.

the first line of the input will be an integer representing the number of inputs

sample input:


10
acalephe
decolor
estheses
heroize
paviors
speer
stower
tsoris
unmiter
sample


output:
stower
tsoris
paviors
unmiter
estheses
"""

import sys


def calculate_word_value(word):
    total = 0
    for char in word:
        if char.isalpha():
            total += ord(char) - ord("a") + 1
    return total


if __name__ == "__main__":
    max_words = int(sys.stdin.readline())

    output = []
    for count in range(max_words):
        word = sys.stdin.readline().strip().lower()
        if calculate_word_value(word) == 100:
            output.append(word)

    output.sort(key=len)

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


def calculate_word_value(word) -> int:
    total = 0
    for char in word:
        if char.isalpha():
            total += ord(char) - ord("a") + 1
    return total


if __name__ == "__main__":
    output = []
    word_count = int(sys.stdin.readline())
    for count in range(word_count):
        word = sys.stdin.readline()
        if calculate_word_value(word.lower().strip()) == 100:
            output.append(word.strip())
    output.sort(key=len)
    for word in output:
        print(word)

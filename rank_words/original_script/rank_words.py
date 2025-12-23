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


def calculate_word(word):
    total = 0
    for c in word.lower():
        if c.isalpha():
            total += ord(c) - ord("a") + 1
    return total


count = int(sys.stdin.readline())
result = []
for _ in range(count):
    word = sys.stdin.readline().strip()
    if calculate_word(word) == 100:
        result.append(word)
result.sort(key=len)
for word in result:
    print(word)

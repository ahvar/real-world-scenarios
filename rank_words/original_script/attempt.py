import sys


def calculate(word):
    total = 0
    for c in word.lower():
        if c.isalpha():
            total += ord(c) - ord("a") + 1
    return total


n = int(sys.stdin.readline())
all_words = []
for i in range(n):
    word = sys.stdin.readline().strip()
    if calculate(word) == 100:
        all_words.append(word)
all_words.sort(key=len)
for word in all_words:
    print(word)

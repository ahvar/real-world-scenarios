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

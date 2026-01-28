import sys


def calculate_word_value(word):
    if not word:
        return 0
    total = 0
    for c in word:
        total += ord(c) - ord("a") + 1
    if total == 100:
        return True
    return False


total_count = int(sys.stdin.readline())
words = []
for count in range(total_count):
    word = int(sys.stdin.readline())
    words.append(word)

target_words = []
for word in words:
    if calculate_word_value(word):
        target_words.append(word)
target_words.sort(key=len)
for w in target_words:
    print(w)

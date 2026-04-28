from collections import Counter


def solution(clean, dirty, k):
    c = Counter(clean)
    d = Counter(dirty)
    clean_pairs = 0
    clean_unpaired = {}
    dirty_pairs = 0
    for color, count in c.items():
        clean_pairs += count // 2
        if count % 2 == 1:
            clean_unpaired[color] = 1

    for color in list(clean_unpaired.keys()):
        if k > 0 and d.get(color, 0) > 0:
            clean_pairs += 1
            k -= 1
            d[color] -= 1
            del clean_unpaired[color]

    for color, count in d.items():
        while k >= 2 and count >= 2:
            pairs += 1
            k -= 2
            count -= 2

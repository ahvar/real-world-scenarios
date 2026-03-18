from collections import Counter


def solution(k, c, d):
    clean = Counter(c)
    dirty = Counter(d)
    pairs = 0
    unmatched = {}
    # count pairs from clean socks and track unpaired
    for color, count in clean.items():
        pairs += count // 2
        if count % 2 == 1:
            unmatched[color] += 1

    for color in list(unmatched.keys()):
        if k > 0 and dirty.get(color, 0) > 0:
            pairs += 1
            k -= 1
            dirty[color] -= 1
            del unmatched[color]  # there would only be one unmatched

    for color, count in dirty.items():
        while k >= 2 and count >= 2:
            pairs += 1
            k -= 2
            count -= 2
    return pairs

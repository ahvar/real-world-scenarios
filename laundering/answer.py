from collections import Counter


def solution(k, clean, dirty):
    clean_count = Counter(clean)
    dirty_count = Counter(dirty)

    pairs = 0
    unpaired = {}
    # count pairs from clean socks and track unpaired
    for color, count in clean_count.items():
        pairs += count // 2
        if count % 2 == 1:
            unpaired[color] = 1
    # match unpaired clean socks with dirty socks (1 wash = 1 pair)
    for color in list(unpaired.keys()):
        if k > 0 and dirty_count.get(color, 0) > 0:
            pairs += 1
            k -= 1
            dirty_count[color] -= 1
            del unpaired[color]
    # wash pairs of dirty socks (2 washes = 1 pair)
    for color, count in dirty_count.items():
        while k >= 2 and count >= 2:
            pairs += 1
            k -= 2
            count -= 2
    return pairs

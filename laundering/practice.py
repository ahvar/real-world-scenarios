from collections import Counter, defaultdict

def solution(clean, dirty, k):
    clean_socks = Counter(clean)
    dirty_socks = Counter(dirty)
    clean_pairs = defaultdict(int)
    unpaired_clean = defaultdict(int)
    dirty_pairs = defaultdict(int)
    for color, count in clean_socks.items():
        pairs = count // 2
        if clean_pairs.get(color, 0) == 0:
            clean_pairs
        unpaired = count % 2
        if unpaired:
            unpaired_clean[color] = count % 2

    for color in unpaired_clean.keys():
        if dirty_socks.get(color, 0) != 0 and k > 0:
            dirty_socks[color] -= 1
            k -= 1
            clean_pairs.get(color, 0) += 1
    for color, count in dirty_socks.items():
        pairs = count // 2
        unpaired = count % 2
        if k >= 2:
            clean_pairs.get(color, 0) += pairs
    return sum(clean_pairs.values())

        
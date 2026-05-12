from collections import Counter


class Laundry:

    def __init__(self, clean, dirty, k):
        self._clean = Counter(clean)
        self._dirty = Counter(dirty)
        self._k = k

    def wash(self):
        clean_pairs = 0
        clean_unpaired = 0
        dirty_pairs = 0
        dirty_unpaired = 0
        # increment clean pairs
        for color, count in self._clean.items():
            clean_pairs += count // 2  # divide by 2 to get pairs
            if clean_unpaired % 2 == 1:  # modulo by 2 to get remainder
                clean_unpaired += 1
        # increment dirty pairs
        for color, count in self._dirty.items():
            dirty_pairs += count // 2
            if dirty_unpaired % 2 == 1:
                dirty_unpaired += 1
            # if find this color in clean socks
            if self._clean.get(color, 0) != 0:
                while dirty_pairs and self._k > 0:
                    dirty_pairs -= 1
                    self._k -= 2
                    clean_pairs += 1

                while dirty_unpaired > 0 and self._clean_unpaired > 0 and self._k > 0:
                    dirty_unpaired -= 1

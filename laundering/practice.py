from collections import Counter


class Laundry:

    def solution(self, clean, dirty, k):
        clean_count = Counter(clean)
        dirty_count = Counter(dirty)
        pairs = 0
        unpaired_count = {}
        for color, count in clean_count.items():
            pairs += count // 2
            unpaired = count % 2
            if unpaired:
                unpaired_count[color] = 1

        for color, count in dirty_count.items():
            dirty_pairs = count // 2
            dirty_unpaired = count % 2

            while k > 0 and dirty_pairs > 0:
                pairs += 1
                k -= 2
                dirty_pairs -= 2

            if dirty_unpaired:
                while k > 0 and unpaired_count.get(color, 0) > 0:
                    pairs += 1
                    unpaired_count[color] -= 1
                    k -= 1
        return pairs


class TestLaundry:
    def setup_method(self):
        self.laundry = Laundry()

    def test_solution(self):
        assert self.laundry.solution([1, 2, 1, 1], [1, 4, 3, 2, 4], 2) == 3

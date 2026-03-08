def solution(k, clean, dirty):
    colors = {1: "red", 2: "green", 3: "brown", 4: "purple"}
    n, m = len(clean), len(dirty)
    clean_stack = [clean[0]]
    pairs = 0
    for sock in clean[1:]:
        if clean_stack and colors.get(clean_stack[-1]) == colors.get(sock):
            pairs += 1
            clean_stack.pop()
        else:
            clean_stack.append(sock)
    dirty_stack = [dirty[0]]
    for sock in dirty[1:]:
        if k <= 0:
            break
        if dirty_stack and colors.get(sock) == colors.get(dirty_stack[-1]):
            pairs += 1
            k -= 1
            dirty_stack.pop()
    return pairs


class TestSolution:
    def test_solution(self):
        k = 2
        c = [1, 2, 1, 1]
        d = [1, 4, 3, 2, 4]
        assert solution(k, c, d) == 3

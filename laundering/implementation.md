# Sock Pairing Implementation Plan

## Problem Summary
Bob wants to maximize pairs of clean, same-colored socks for his trip. He can wash at most K dirty socks to help achieve this goal.

**Inputs:**
- `K`: maximum socks the washing machine can clean
- `C`: array of clean sock colors
- `D`: array of dirty sock colors

**Output:** Maximum number of clean sock pairs

---

## Algorithm Strategy

### Key Observations
1. **Existing pairs**: First count pairs already available from clean socks
2. **Priority 1 - Complete pairs**: If a clean sock is unpaired, washing ONE matching dirty sock creates a new pair (cost: 1 wash)
3. **Priority 2 - New pairs from dirty**: Washing TWO dirty socks of the same color creates a new pair (cost: 2 washes)

### Steps
1. Count occurrences of each color in clean socks
2. Calculate existing pairs: `count // 2` for each color
3. Track unpaired clean socks: `count % 2` for each color
4. For colors with unpaired clean socks, check dirty pile for matches (costs 1 wash per pair)
5. With remaining wash capacity, wash pairs of dirty socks (costs 2 washes per pair)

---

## Implementation 1: Basic Approach

**Focus:** Correctness over performance. Simple data structures and explicit loops.

### Data Structures
- Lists for iteration
- Dictionary built manually with loops

### Steps
1. Create a dictionary to count clean sock colors using a basic loop
2. Calculate pairs from clean socks: `sum(count // 2 for count in clean_counts.values())`
3. Track colors with unpaired socks (where `count % 2 == 1`)
4. Create a dictionary to count dirty sock colors using a basic loop
5. Iterate through unpaired clean sock colors:
   - If matching dirty sock exists and `K > 0`: increment pairs, decrement K, decrement dirty count
6. With remaining K, iterate through dirty counts:
   - While `count >= 2` and `K >= 2`: increment pairs, decrement K by 2, decrement count by 2

---

## Implementation 2: Optimized Approach

**Focus:** Performance optimization using Python's `collections.Counter` and efficient iteration patterns.

### Data Structures
- `collections.Counter` for O(1) average lookups and built-in counting
- Process dirty socks in sorted order by count (descending) to maximize pairs with remaining washes

### Optimizations
1. **Counter class**: Eliminates manual dictionary building with cleaner, faster code
2. **Single-pass pair calculation**: Use `sum()` with generator expression
3. **Sorted dirty processing**: When washing dirty pairs, prioritize colors with more socks to maximize output
4. `Counter.most_common()` returns elements sorted by frequency, allowing early exit when K is exhausted
5. `Counter` handles missing keys gracefully (returns 0), avoiding `KeyError` checks

---

## Test Case Walkthrough

**Input:** `K=2, C=[1,2,1,1], D=[1,4,3,2,4]`

| Step | Description | Pairs | K remaining |
|------|-------------|-------|-------------|
| Initial | Clean counts: {1:3, 2:1}, Dirty counts: {1:1, 4:2, 3:1, 2:1} | 0 | 2 |
| Step 1 | Pairs from clean: color 1 → 3//2=1, color 2 → 1//2=0 | 1 | 2 |
| Step 2 | Unpaired clean: color 1 (3%2=1), color 2 (1%2=1) | 1 | 2 |
| Step 2a | Match color 1: wash 1 dirty red sock | 2 | 1 |
| Step 2b | Match color 2: wash 1 dirty green sock | 3 | 0 |
| Step 3 | K=0, no more washing | 3 | 0 |

**Output:** 3 ✓

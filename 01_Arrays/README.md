# 📦 01 · Arrays — Python Lists (Dynamic Arrays)

> **DSA-Leetcode-Journey** › `01_Arrays`

---

## 📖 Concept Explanation (Plain English)

An **array** is the most fundamental data structure: an ordered collection of items stored at **contiguous memory locations**. Think of it like a row of numbered lockers — each locker (element) has a fixed address (index), so you can jump directly to any one of them in O(1) time.

Python does **not** have a built-in static array. Instead, it provides **Lists**, which are **dynamic arrays** under the hood.

### How Python Lists Grow

A Python list does not allocate just enough memory for its current elements. It over-allocates a buffer of spare slots so that future appends are cheap. Here is exactly what happens step-by-step:

1. You create `nums = []`. Python allocates a small internal buffer (0 slots of payload capacity).
2. You call `nums.append(1)`. The buffer is full, so Python allocates a **new, larger block** — roughly 1.125× the previous capacity — copies all existing elements into it, and discards the old block.
3. The next few appends land in the spare slots at no extra cost.
4. When the buffer fills again, the resize cycle repeats.

Because resizes happen exponentially less frequently as the list grows, the **amortised cost of a single append is O(1)** even though the occasional resize is O(n).

```python
import sys

nums = []
for i in range(9):
    nums.append(i)
    print(f"len={len(nums):>2}  allocated_bytes={sys.getsizeof(nums)}")

# len= 1  allocated_bytes=88    ← first resize: grabbed spare slots
# len= 2  allocated_bytes=88
# len= 3  allocated_bytes=88
# len= 4  allocated_bytes=88
# len= 5  allocated_bytes=120   ← second resize
# ...
# Notice: byte jumps only occur at certain lengths, not every append.
```

### Key Mental Model

The memory address of index `i` is simply:

```
address(i) = base_address + i × element_size
```

That arithmetic is why **random access is O(1)**. Insertion or deletion in the **middle**, however, forces every element after that position to shift — making those operations O(n).

---

## ⏱️ Big O Complexity — Python List Operations

| Operation | Syntax | Time | Space | Notes |
|---|---|---|---|---|
| Access by index | `a[i]` | **O(1)** | O(1) | Direct memory-offset arithmetic |
| Assign by index | `a[i] = x` | **O(1)** | O(1) | Overwrites in place; no shifting |
| Length | `len(a)` | **O(1)** | O(1) | Cached as a struct field; never recomputed |
| Append | `a.append(x)` | **O(1)** amortised | O(1) | Occasional O(n) resize, but rare |
| Pop last | `a.pop()` | **O(1)** | O(1) | No shifting; buffer shrinks lazily |
| Insert at index | `a.insert(i, x)` | **O(n)** | O(1) | All elements after `i` must shift right |
| Delete at index | `del a[i]` | **O(n)** | O(1) | All elements after `i` must shift left |
| Pop at index | `a.pop(i)` | **O(n)** | O(1) | Shift left after removal |
| Search (unsorted) | `x in a` | **O(n)** | O(1) | Linear scan; no structure to exploit |
| Slice | `a[i:j]` | **O(k)** | O(k) | k = j − i; copies into a new list |
| Reverse in-place | `a.reverse()` | **O(n)** | O(1) | Two-pointer swap (see snippet below) |
| Sort | `a.sort()` | **O(n log n)** | O(log n) | Timsort; stable, in-place |
| Extend / concat | `a + b` | **O(n + m)** | O(n + m) | Allocates a brand-new list |

> **Space note:** Auxiliary space is measured excluding the input list itself unless stated otherwise.

---

## 🌍 Real-World Applications

Arrays (and their Python List equivalent) are the default container in almost every layer of a modern software stack.

### Data Science & Machine Learning
NumPy's `ndarray` and Pandas' `Series` / `DataFrame` are both built on top of contiguous C arrays. Every matrix multiplication, normalisation pass, or feature-engineering pipeline operates on arrays. The reason vectorised NumPy operations outperform Python loops by 100× is entirely down to CPU cache efficiency: iterating a contiguous block of floats triggers hardware prefetching; jumping between scattered objects does not.

### Backend APIs & JSON Responses
REST and GraphQL APIs return collections as JSON arrays. When a `/products` endpoint returns a list of 50 items, the server builds a Python list, serialises it to JSON, and the client parses it back into an array (JavaScript `Array`, Dart `List`, Swift `Array`). Pagination logic — `items[offset : offset + limit]` — is a direct O(k) slice on that list.

### UI State Management
Front-end frameworks (React, Vue, Flutter) store component state — todo items, notification feeds, search results — in arrays. Rendering a list of 10,000 rows efficiently using "virtual scrolling" relies on slicing the visible window from the full array in O(k) time rather than rendering all 10,000 DOM nodes.

### Graph & Tree Algorithms
Adjacency lists (the standard graph representation), BFS/DFS queues, recursion stacks, and dynamic-programming tables are all implemented as arrays. Every shortest-path or topological-sort algorithm you will encounter in later folders depends on the O(1) access and O(1) append properties covered in this folder.

### Databases & Buffer Pools
Relational databases store table pages in buffer-pool arrays in memory. An index scan reads a contiguous range of page slots — a direct application of O(1) random access. Write-ahead logs append records to an in-memory array before flushing to disk.

---

## 🐍 Python Code Snippet — Two-Pointer Array Reversal

The **two-pointer** pattern is one of the most reusable tools in array problem-solving. Place one pointer at each end and march them inward, swapping as you go. Every element is visited exactly once — O(n) time, O(1) space.

```python
# ─────────────────────────────────────────────────────────────────
# Two-Pointer Array Reversal
# Time:  O(n)  — each element is visited exactly once
# Space: O(1)  — only two index variables; the swap is in-place
#
# Core insight: the element at index `left` and the element at
# index `right` are symmetric partners. Swap them, then converge.
# ─────────────────────────────────────────────────────────────────

def reverse_in_place(nums: list) -> list:
    left, right = 0, len(nums) - 1

    while left < right:
        nums[left], nums[right] = nums[right], nums[left]  # swap
        left  += 1
        right -= 1

    return nums   # same list object, mutated in place


# ── For comparison: slice reversal (creates a NEW list) ───────────
# Time:  O(n)  |  Space: O(n)
def reverse_new_copy(nums: list) -> list:
    return nums[::-1]


# ── Quick demo ────────────────────────────────────────────────────
if __name__ == "__main__":
    original = [1, 2, 3, 4, 5]

    copy      = original.copy()
    reversed_ = reverse_in_place(copy)
    print("In-place :", reversed_)          # [5, 4, 3, 2, 1]
    print("Same obj? :", reversed_ is copy) # True — no new list

    print("New copy :", reverse_new_copy(original)) # [5, 4, 3, 2, 1]
    print("Original :", original)                   # [1, 2, 3, 4, 5]
```

### Two-Pointer — Step-by-Step Visualisation

```
nums = [1, 2, 3, 4, 5]
        ↑           ↑
      left=0      right=4     swap(1, 5)  →  [5, 2, 3, 4, 1]

nums = [5, 2, 3, 4, 1]
           ↑     ↑
         left=1 right=3       swap(2, 4)  →  [5, 4, 3, 2, 1]

nums = [5, 4, 3, 2, 1]
              ↑
           left=2
           right=2             left >= right  →  stop

Result: [5, 4, 3, 2, 1]  ✅
```

---

## ✅ LeetCode Problem Tracker

| # | Problem | Difficulty | Core Pattern | Status |
|---|---|---|---|---|
| 217 | [Contains Duplicate](https://leetcode.com/problems/contains-duplicate/) | 🟢 Easy | Hash Set membership check | - [ ] |
| 1 | [Two Sum](https://leetcode.com/problems/two-sum/) | 🟢 Easy | Hash Map complement lookup | - [ ] |
| 121 | [Best Time to Buy & Sell Stock](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/) | 🟢 Easy | Single-pass running minimum | - [ ] |
| 238 | [Product of Array Except Self](https://leetcode.com/problems/product-of-array-except-self/) | 🟡 Medium | Prefix & suffix product pass | - [ ] |

### Checkbox version (for local tracking)

- [ ] **LC 217 — Contains Duplicate** · Add each element to a `set` as you iterate. If `num` is already in the set before insertion, return `True`. O(n) time, O(n) space. Alternative: `return len(nums) != len(set(nums))` — same complexity, one line.

- [ ] **LC 1 — Two Sum** · Use a `dict` mapping each value to its index. For every element, check whether `target - num` already exists in the map. If so, return `[map[target - num], i]`. O(n) time, O(n) space.

- [ ] **LC 121 — Best Time to Buy & Sell Stock** · Track `min_price` as a running minimum. At each index, update `max_profit = max(max_profit, price - min_price)`. O(n) time, O(1) space — no nested loops needed.

- [ ] **LC 238 — Product of Array Except Self** · First pass (left-to-right): build a `prefix` array where `prefix[i]` = product of all elements to the left of `i`. Second pass (right-to-left): multiply each `prefix[i]` by a running `suffix` product. No division, O(n) time, O(1) auxiliary space (output array excluded).

---

## 💡 Common Array Patterns — Quick Reference

```
Pattern                   When to reach for it
───────────────────────── ────────────────────────────────────────────────────
Two Pointers              Reversal, pair sums, palindrome checks, sorted arrays
Sliding Window            Subarray max/min/sum within a fixed or variable window
Hash Map / Hash Set       Duplicate detection, complement lookup, frequency count
Prefix / Suffix Products  Problems requiring "all except self" aggregations
Kadane's Algorithm        Maximum subarray sum (LC 53)
Binary Search             Searching or inserting in a sorted array in O(log n)
```

---

## 🗂️ Folder Structure

```
01_Arrays/
├── README.md                     
├── contains_duplicate.py         ← LC 217
├── two_sum.py                    ← LC 1
├── buy_sell_stock.py             ← LC 121
└── product_except_self.py        ← LC 238
```

---

## 🔗 Further Reading

- [Python list internals — CPython source](https://github.com/python/cpython/blob/main/Objects/listobject.c)
- [Time Complexity — Python Wiki](https://wiki.python.org/moin/TimeComplexity)
- [How Python lists work — Ned Batchelder](https://nedbatchelder.com/text/iter.html)
- [NeetCode Arrays Roadmap](https://neetcode.io/roadmap)

---

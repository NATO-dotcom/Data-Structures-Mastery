# 🔗 03 · Linked Lists — Singly Linked Lists in Python

> **DSA-Leetcode-Journey** › `03_LinkedLists`

---

## 📖 Concept Explanation (Plain English)

A **singly linked list** is a linear data structure made up of **nodes** scattered anywhere across memory, stitched together by **pointers**. Unlike an array — where every element sits in a neat, contiguous block — a linked list has no fixed address pattern. Each node holds two things: its **value** and a **pointer (reference) to the next node** in the sequence. The last node points to `None`, marking the end of the list.

### The Key Mental Model: A Treasure Hunt

Think of a linked list as a treasure hunt. The starting clue (the **head** pointer) tells you where to find the first location. That location contains a value and a clue pointing to the next location. You **must follow every clue in sequence** — there is no shortcut to jump directly to stop number 5 without passing through stops 1, 2, 3, and 4 first.

```
HEAD
 │
 ▼
┌───────┬──────┐    ┌───────┬──────┐    ┌───────┬──────┐    ┌───────┬──────┐
│  val  │ next │───▶│  val  │ next │───▶│  val  │ next │───▶│  val  │ None │
│   1   │      │    │   2   │      │    │   3   │      │    │   4   │      │
└───────┴──────┘    └───────┴──────┘    └───────┴──────┘    └───────┴──────┘
  addr: 0x4A2C        addr: 0x9F10        addr: 0x1B88        addr: 0xC301
```

The nodes live at completely different memory addresses — `0x4A2C`, `0x9F10`, `0x1B88`, `0xC301` — connected only by the `next` pointer stored inside each one.

### Arrays vs. Linked Lists — The Core Trade-off

| | Array (Python List) | Singly Linked List |
|---|---|---|
| **Memory layout** | Contiguous block | Scattered nodes anywhere in heap |
| **Random access** | O(1) — index arithmetic | O(n) — must traverse from head |
| **Insert / Delete at head** | O(n) — must shift everything | **O(1)** — rewire one pointer |
| **Insert / Delete at tail** | O(1) amortised (append) | O(n) — must walk to the end* |
| **Insert / Delete in middle** | O(n) — shift required | O(n) — traverse + O(1) rewire |
| **Memory overhead** | Low (dense packing) | Higher (each node stores a pointer) |

> \* O(1) if a `tail` pointer is maintained separately (common in production implementations).

### Why "Scattered Memory" Is Both a Strength and a Weakness

**Strength:** Insertion and deletion at the head are truly O(1). No elements need to shift. You simply create a new node, point its `next` at the current head, and update the head reference. This makes linked lists ideal for stacks and queues where all action happens at the ends.

**Weakness:** There is no index arithmetic. To read the 500th element you must walk 499 pointers. This also means **poor cache performance** — modern CPUs prefetch contiguous memory blocks into cache, but scattered nodes cause frequent cache misses, making traversal slower in practice than the O(n) figure alone suggests.

---

## ⏱️ Big O Complexity — Singly Linked List Operations

| Operation | Time Complexity | Space Complexity | Notes |
|---|---|---|---|
| Access by index | **O(n)** | O(1) | Must walk from head — no index arithmetic |
| Search by value | **O(n)** | O(1) | Linear scan; no structure to exploit |
| Insert at head | **O(1)** | O(1) | Create node, point to old head, update head |
| Insert at tail | **O(n)** | O(1) | Walk to last node, then append; O(1) with tail pointer |
| Insert after node* | **O(1)** | O(1) | Given the node reference — just rewire two pointers |
| Delete at head | **O(1)** | O(1) | Move head to head.next |
| Delete at tail | **O(n)** | O(1) | Must reach second-to-last node to unlink |
| Delete by value | **O(n)** | O(1) | Search O(n) + unlink O(1) |
| Reverse (iterative) | **O(n)** | O(1) | Three-pointer walk — covered in snippet below |
| Reverse (recursive) | **O(n)** | O(n) | Call stack depth equals list length |
| Detect cycle | **O(n)** | O(1) | Floyd's slow/fast pointer algorithm |
| Find middle node | **O(n)** | O(1) | Slow/fast pointer — fast moves 2× speed |
| Merge two sorted lists | **O(n + m)** | O(1) | Iterative pointer comparison; no extra array |

> \* "Given the node reference" means you already hold a direct pointer to that node — no traversal needed.

---

## 🌍 Real-World Applications

Linked lists are one of those structures that rarely surface in high-level APIs yet quietly underpin dozens of features you use every day.

### Undo / Redo in Editors
Text editors, design tools (Figma, Photoshop), and IDEs model edit history as a linked list of state snapshots. Every keystroke appends a new node. Pressing **Ctrl+Z** walks one node backward; **Ctrl+Y** walks one forward. A doubly linked list is typically used here so that traversal in both directions is O(1).

### Browser History
Your browser's Back and Forward buttons are backed by a doubly linked list of visited URLs. Navigating to a new page appends a node; clicking Back moves the current pointer to `node.prev`; clicking Forward moves it to `node.next`. Tab restoration after a crash re-builds this list from serialised state.

### Hash Map Collision Resolution (Chaining)
Python's `dict` and Java's `HashMap` both handle hash collisions via **separate chaining** — each bucket in the underlying array holds the head of a singly linked list of key-value pairs that share the same hash. When two keys collide, a new node is prepended to that bucket's list. Lookup walks the short chain doing key equality checks.

### OS Memory Allocation
The kernel's free-memory manager maintains a **free list** — a linked list of available memory blocks. `malloc` searches this list for a block large enough to satisfy an allocation request, unlinks it, and returns it. `free` prepends the released block back to the list. The entire heap allocator is built on O(1) insert-at-head linked list operations.

### Music / Video Playlists
Streaming services model playback queues as doubly linked lists, enabling O(1) skip-forward, skip-back, and insert-next operations without rebuilding the entire queue. Shuffle mode re-wires the `next` pointers rather than copying track data.

---

## 🐍 Python Code Snippet — `ListNode` Class & Iterative List Reversal

```python
# ─────────────────────────────────────────────────────────────────
# 1. Node Definition
#    The universal building block used in nearly every LeetCode
#    linked-list problem. LeetCode pre-defines this class for you,
#    but understanding it from scratch is essential.
# ─────────────────────────────────────────────────────────────────

class ListNode:
    def __init__(self, val: int = 0, next: "ListNode | None" = None):
        self.val  = val   # the payload — any value the node stores
        self.next = next  # pointer to the next node, or None


# ─────────────────────────────────────────────────────────────────
# 2. Helper utilities (not asked in interviews, but useful locally)
# ─────────────────────────────────────────────────────────────────

def build_list(values: list[int]) -> ListNode | None:
    """Convert a Python list into a linked list; return the head."""
    if not values:
        return None
    head = ListNode(values[0])
    current = head
    for v in values[1:]:
        current.next = ListNode(v)
        current = current.next
    return head


def list_to_array(head: ListNode | None) -> list[int]:
    """Convert a linked list back to a Python list (for printing)."""
    result, current = [], head
    while current:
        result.append(current.val)
        current = current.next
    return result


# ─────────────────────────────────────────────────────────────────
# 3. Reverse a Linked List — Iterative (LeetCode 206)
#
# Time:  O(n)  — single pass through all n nodes
# Space: O(1)  — only three pointer variables; no extra structure
#
# Core insight: walk the list once, reversing each arrow as you go.
# Three pointers track: the node just processed (prev), the current
# node being re-wired (curr), and the node not yet touched (next_node).
# ─────────────────────────────────────────────────────────────────

def reverse_list(head: ListNode | None) -> ListNode | None:
    prev = None       # will become the new tail (points to None)
    curr = head       # starts at the old head

    while curr:
        next_node  = curr.next   # 1. save the remainder of the list
        curr.next  = prev        # 2. reverse the arrow
        prev       = curr        # 3. advance prev one step forward
        curr       = next_node   # 4. advance curr one step forward

    return prev   # prev is now pointing at the new head


# ─────────────────────────────────────────────────────────────────
# 4. Reverse a Linked List — Recursive (alternative)
#
# Time:  O(n)  — visits every node once
# Space: O(n)  — call stack depth equals the number of nodes ⚠️
# ─────────────────────────────────────────────────────────────────

def reverse_list_recursive(head: ListNode | None) -> ListNode | None:
    if not head or not head.next:
        return head                          # base case: 0 or 1 node

    new_head = reverse_list_recursive(head.next)   # recurse to the end
    head.next.next = head   # make the next node point BACK at head
    head.next      = None   # break the original forward link
    return new_head


# ─────────────────────────────────────────────────────────────────
# 5. Visualisation of the iterative reversal
# ─────────────────────────────────────────────────────────────────
#
# Initial:   None ← ? ? ?     1 → 2 → 3 → 4 → None
#                              ↑
#                             curr (prev=None)
#
# Step 1:   prev=None, curr=1, next_node=2
#           1.next = None  →   None ← 1    2 → 3 → 4 → None
#           prev=1, curr=2
#
# Step 2:   prev=1,    curr=2, next_node=3
#           2.next = 1    →   None ← 1 ← 2    3 → 4 → None
#           prev=2, curr=3
#
# Step 3:   prev=2,    curr=3, next_node=4
#           3.next = 2    →   None ← 1 ← 2 ← 3    4 → None
#           prev=3, curr=4
#
# Step 4:   prev=3,    curr=4, next_node=None
#           4.next = 3    →   None ← 1 ← 2 ← 3 ← 4
#           prev=4, curr=None  → loop ends
#
# Return prev (4) as the new head.  ✅


# ─────────────────────────────────────────────────────────────────
# 6. Quick demo
# ─────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    original = [1, 2, 3, 4, 5]
    head     = build_list(original)

    print("Original :", list_to_array(head))          # [1, 2, 3, 4, 5]

    reversed_head = reverse_list(head)
    print("Reversed :", list_to_array(reversed_head)) # [5, 4, 3, 2, 1]
```

---

## ✅ LeetCode Problem Tracker

| # | Problem | Difficulty | Core Pattern | Status |
|---|---|---|---|---|
| 206 | [Reverse Linked List](https://leetcode.com/problems/reverse-linked-list/) | 🟢 Easy | Iterative three-pointer / recursive | - [ ] |
| 21 | [Merge Two Sorted Lists](https://leetcode.com/problems/merge-two-sorted-lists/) | 🟢 Easy | Two-pointer merge with dummy head node | - [ ] |
| 141 | [Linked List Cycle](https://leetcode.com/problems/linked-list-cycle/) | 🟢 Easy | Floyd's slow/fast (tortoise & hare) | - [ ] |

### Checkbox version (for local tracking)

- [ ] **LC 206 — Reverse Linked List** · Use three pointers: `prev = None`, `curr = head`. On each iteration save `next_node = curr.next`, flip `curr.next = prev`, then advance both pointers. Return `prev` as the new head. O(n) time, O(1) space.

- [ ] **LC 21 — Merge Two Sorted Lists** · Create a `dummy = ListNode(0)` sentinel and a `tail` pointer starting there. At each step, compare `l1.val` and `l2.val`, attach the smaller node to `tail.next`, and advance both `tail` and that list's pointer. Append whichever list still has nodes. Return `dummy.next`. O(n + m) time, O(1) space.

- [ ] **LC 141 — Linked List Cycle** · Use Floyd's algorithm: initialise `slow = fast = head`. Move `slow` one step and `fast` two steps per iteration. If `fast` or `fast.next` becomes `None`, there is no cycle — return `False`. If `slow == fast` at any point, a cycle exists — return `True`. O(n) time, O(1) space.

---

## 💡 Common Linked List Patterns — Quick Reference

```
Pattern                    When to reach for it
────────────────────────── ───────────────────────────────────────────────────
Three-pointer reversal     Reversing a list or a sub-section of it (LC 92, 206)
Dummy / sentinel head      Simplifies edge cases when the head itself may change
Slow / fast pointers       Cycle detection, finding the middle, kth from end
Merge two sorted lists     Sorted merge, sort-list problems (LC 21, 148)
Recursive unwinding        Problems solved elegantly by processing tail-first
In-place re-linking        Partition list, odd-even grouping (LC 86, 328)
```

---

## 🗂️ Folder Structure

```
03_LinkedLists/
├── README.md                    ← you are here
├── list_node.py                 ← shared ListNode class + helpers
├── reverse_linked_list.py       ← LC 206
├── merge_two_sorted_lists.py    ← LC 21
└── linked_list_cycle.py         ← LC 141
```

---

## 🔗 Further Reading

- [Python `object` model and references](https://docs.python.org/3/reference/datamodel.html)
- [Floyd's Cycle Detection Algorithm — original paper](https://en.wikipedia.org/wiki/Cycle_detection#Floyd's_tortoise_and_hare)
- [CPython dict implementation (chaining)](https://github.com/python/cpython/blob/main/Objects/dictobject.c)
- [NeetCode Linked Lists Roadmap](https://neetcode.io/roadmap)

---
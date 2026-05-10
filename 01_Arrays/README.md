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

## 📚 File Guide

This folder contains comprehensive examples demonstrating core array concepts and operations in Python:

### 1️⃣ Array Types & Initialization

#### [array_types.py](array_types.py)
**Purpose:** Demonstrates different ways to create and classify arrays in Python.

**Key Concepts:**
- **Fixed-size arrays:** Creating an array with predetermined capacity
  ```python
  arr = [0] * 5  # Creates [0, 0, 0, 0, 0]
  ```
- **Dynamic arrays:** Empty lists that grow as needed
  ```python
  arr = []  # Grows dynamically when you add elements
  ```
- **Dimensionality:** 1D arrays (lists), 2D arrays (nested lists), and higher dimensions

**Use Case:** Understanding the different structures available before working with arrays.

---

### 2️⃣ Array Traversal — Types & Methods

Traversal is the process of visiting each element in an array. Understanding the distinction between **traversal types** and **traversal methods** is key:

#### **Traversal Types (Direction of iteration):**
- **Linear:** Forward direction (start → end: index 0 to len-1)
- **Reverse:** Backward direction (end → start: index len-1 to 0)

#### **Traversal Methods (Programming construct):**
- **For Loop:** Index-based iteration using `range()`
- **Foreach Loop:** Value-based iteration (direct element access)
- **While Loop:** Manual counter management with custom condition

---

#### 📋 Traversal Type: LINEAR (Forward)

**[Linear_traversal.py](Linear_traversal.py)** — Example using Foreach Method

**Pattern:** Start at index 0, visit each element sequentially until the end

```python
arr = [1, 2, 3, 4, 5]
for element in arr:
    print(element)  # Output: 1 2 3 4 5
```

**Complexity:** Time O(n), Space O(1)

**Use Cases:** Processing data in order, summing values, searching for elements.

---

#### 📋 Traversal Type: REVERSE (Backward)

**[Reverse_traversal.py](Reverse_traversal.py)** — Example using For Loop Method

**Pattern:** Start at the last index and move backwards

```python
arr = [1, 2, 3, 4, 5]
for i in range(len(arr) - 1, -1, -1):
    print(arr[i])  # Output: 5 4 3 2 1
```

**Complexity:** Time O(n), Space O(1)

**Use Cases:** Reading arrays backwards, undo operations, validating palindromes.

---

#### 🔧 Traversal Method: FOR LOOP (Index-Based using range())

**[ForLoop_Traversal.py](ForLoop_Traversal.py)** — Index-based iteration using `range()`

**Pattern:** Use index variable `i` to access elements

```python
arr = [1, 2, 3, 4, 5]
for i in range(len(arr)):
    print(arr[i])  # Output: 1 2 3 4 5
```

**Complexity:** Time O(n), Space O(1)

**Use When:** You need the index value for calculations or conditional logic.

---

#### 🔧 Traversal Method: FOREACH LOOP (Value-Based, NOT Range-Based)

**[ForeachLoop_Traversal.py](ForeachLoop_Traversal.py)** — Direct element value access

**Pattern:** Direct iteration over element values without index access

```python
arr = [1, 2, 3, 4, 5]
for value in arr:
    print(value)  # Output: 1 2 3 4 5
```

**Complexity:** Time O(n), Space O(1)

**Use When:** You only need element values. Most Pythonic and readable. **Note: This is value-based, NOT range-based.**

---

#### 🔧 Traversal Method: WHILE LOOP (Manual Counter)

**[WhileLoop_Traversal.py](WhileLoop_Traversal.py)** — Manual counter management

**Pattern:** Manually control the loop with explicit counter and condition

```python
arr = [1, 2, 3, 4, 5]
i = 0
while i < len(arr):
    print(arr[i])
    i += 1
```

**Complexity:** Time O(n), Space O(1)

**Use When:** You need fine-grained control (conditionally skip, jump indices, etc.).

---

#### 📊 Quick Comparison: All 6 Combinations

| Traversal Type | For Loop | Foreach Loop | While Loop |
|---|---|---|---|
| **LINEAR** | `for i in range(len(arr))` | `for val in arr` | `i = 0; while i < n` |
| **REVERSE** | `for i in range(len-1, -1, -1)` | `for val in reversed(arr)` | `i = n-1; while i >= 0` |

---

### 3️⃣ Array Operations

#### [operations.py](operations.py)
**Purpose:** Reference guide for common insertion and deletion operations with complexity analysis.

**Insertion Operations:**
| Operation | Time Complexity | Space Complexity | Notes |
|-----------|-----------------|------------------|-------|
| At the end | O(1) amortized | O(1) | Fastest, leverages Python's dynamic resizing |
| At the beginning | O(n) | O(1) | Requires shifting all elements |
| At a given point | O(n) | O(1) | Worst case when inserting near start |

**Deletion Operations:**
| Operation | Time Complexity | Space Complexity | Notes |
|-----------|-----------------|------------------|-------|
| From the end | O(1) | O(1) | Fastest, no shifting needed |
| From the beginning | O(n) | O(1) | All elements must shift left |
| A specific occurrence | O(n) | O(1) | Requires finding and shifting |
| All duplicates | O(n) | O(1) | Must scan entire array |
| From a given point | O(n) | O(1) | Worst case if near start |

**Key Takeaway:** Always prefer operations at the end of an array for better performance.

---

### 4️⃣ Practical Applications

#### [modifying_application.py](modifying_application.py)
**Purpose:** Demonstrates how to modify array elements in-place.

**Key Details:**
- **Operation:** Increment each element by a fixed value
- **Time Complexity:** O(n)
- **Space Complexity:** O(1)
- **Example:**
  ```python
  arr = [10, 20, 30, 40, 50]
  for i in range(len(arr)):
      arr[i] += 5  # Increases each element by 5
  # Result: [15, 25, 35, 45, 55]
  ```

**Use Cases:** 
- Scaling values (e.g., converting units, applying tax)
- Data preprocessing and normalization
- In-place transformations to save memory

---

#### [search_application.py](search_application.py)
**Purpose:** Implements linear search to find an element in an array.

**Key Details:**
- **Algorithm:** Sequential comparison of each element until target is found
- **Time Complexity:** O(n) — worst case examines all elements
- **Space Complexity:** O(1) — only uses a single flag variable
- **Example:**
  ```python
  arr = [1, 2, 3, 4, 5]
  target = 3
  found = False
  
  for i in range(len(arr)):
      if arr[i] == target:
          found = True
          break
  
  print("Element Found!" if found else "Element not Found!")
  ```

**Use Cases:**
- Finding elements in unsorted arrays
- Checking if a value exists in a dataset
- Building blocks for more complex searches

**Note:** For sorted arrays, consider binary search (O(log n)) for better performance.

---

## 🎯 Learning Path

**Beginner:**
1. Start with [array_types.py](array_types.py) — understand array creation
2. Learn traversal fundamentals:
   - Study **Linear Traversal** with [Linear_traversal.py](Linear_traversal.py)
   - Study **Reverse Traversal** with [Reverse_traversal.py](Reverse_traversal.py)
3. Explore traversal methods:
   - Practice **Foreach Method** with [ForeachLoop_Traversal.py](ForeachLoop_Traversal.py) ⭐ Start here (most Pythonic)
   - Practice **For Method** with [ForLoop_Traversal.py](ForLoop_Traversal.py) (when you need index)
   - Practice **While Method** with [WhileLoop_Traversal.py](WhileLoop_Traversal.py) (for control)
4. Study [operations.py](operations.py) — memorize complexity tradeoffs

**Intermediate:**
1. Master all traversal types with different methods
2. Review [search_application.py](search_application.py) — implement and test variations
3. Work through [modifying_application.py](modifying_application.py) — practice in-place modifications
4. Implement hybrid operations combining traversal + search + modification

**Advanced:**
1. Choose the optimal traversal type + method combination for each problem
2. Solve LeetCode problems involving array manipulation
3. Implement advanced algorithms: two-pointer technique, sliding window, prefix sums

---

## ⏱️ Complex Analysis Summary

| Operation | Time | Space | Notes |
|-----------|------|-------|-------|
| Access element by index | O(1) | O(1) | Direct memory arithmetic |
| Linear search | O(n) | O(1) | Must check each element |
| Insert at end | O(1) amortized | O(1) | Leverages buffer |
| Insert at beginning | O(n) | O(1) | Requires shifting |
| Delete from end | O(1) | O(1) | No shifting needed |
| Delete from beginning | O(n) | O(1) | All elements shift |
| Traverse entire array | O(n) | O(1) | Visit each element once |
| Reverse traversal | O(n) | O(1) | Visit each element once backward |

---

## 💡 Quick Tips

1. **Amortized Complexity:** Appending to a Python list is O(1) *amortized*, not per-operation
2. **In-Place Modifications:** Modifying existing elements is always O(n) for n elements, but beats creating new arrays
3. **Index Bounds:** Python uses 0-based indexing; negative indices count from the end
4. **List vs Array:** Python's `list` is a dynamic array; the `array` module provides typed arrays
5. **Performance:** For frequently-appended data at the beginning, consider `collections.deque`

---

## 🔗 Related Topics

- **Binary Search:** O(log n) search for sorted arrays
- **Sorting Algorithms:** Preparation for advanced array problems
- **Two-Pointer Technique:** Efficient O(n) solutions for many array problems
- **Sliding Window:** Pattern for subarray problems
- **Prefix Sums:** Optimize range queries

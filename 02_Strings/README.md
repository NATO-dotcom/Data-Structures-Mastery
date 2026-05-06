# 🔤 02 · Strings — Immutable Character Arrays in Python

> **DSA-Leetcode-Journey** › `02_Strings`

---

## 📖 Concept Explanation (Plain English)

A **string** in Python is an **ordered, immutable sequence of Unicode characters**. Under the hood, it behaves much like an array — each character lives at a fixed index and can be accessed in constant time — but with one critical difference: **you cannot change it after it is created.**

### Strings are Arrays — but Frozen

Imagine a row of sealed glass display cases, each holding exactly one character. You can peer into any case in O(1) time, read the whole row from left to right, or photograph a section of it (slicing). What you **cannot** do is unlock a case and swap the character inside. That is Python string immutability in a nutshell.

```python
s = "hello"
print(s[1])  # ✅  'e'  — reading is fine
s[1] = 'a'  # ❌  TypeError: 'str' object does not support item assignment
```

### Why Does Immutability Matter for DSA?

| Consequence | Practical Impact |
|---|---|
| **Concatenation always creates a new object** | `s += "x"` is **O(n)** — it allocates fresh memory and copies every character. Inside a loop this quietly becomes O(n²). Use `"".join(parts)` instead. |
| **Safe as dict keys / set elements** | Immutable objects are hashable, so strings can be used directly as `dict` keys or `set` members — critical for frequency-map problems. |
| **No true in-place modification** | Palindrome / anagram checks must operate on indices or convert to a `list` first. |
| **Interning** | CPython may reuse the same memory object for identical short string literals — a useful micro-optimisation, but never rely on it in logic. |

### The "Convert to List" Escape Hatch

When a problem genuinely requires character-level mutation (e.g. reversing a string in-place), the idiomatic Python pattern is:

```python
chars = list(s)      # O(n) — make a mutable copy
# ... mutate chars ...
result = "".join(chars)  # O(n) — reassemble into a new string
```

Both steps are O(n), so the overall cost stays linear — and crucially, **the original string `s` is never touched**.

---

## ⏱️ Big O Complexity — Python String Operations

| Operation | Syntax | Time | Space | Notes |
|---|---|---|---|---|
| Access by index | `s[i]` | **O(1)** | O(1) | Direct memory-offset calculation into the buffer |
| Length | `len(s)` | **O(1)** | O(1) | Stored as a cached struct field; never recomputed |
| Search (substring) | `s.find(t)` / `t in s` | **O(n · m)** | O(1) | n = len(s), m = len(t); CPython uses optimised Boyer-Moore-Horspool variants |
| Concatenation | `s + t` | **O(n + m)** | O(n + m) | Always allocates a brand-new string object |
| Loop concatenation | `s += c` × k | **O(n · k)** ⚠️ | O(n · k) | Each iteration copies the entire string — a silent O(n²) trap |
| Join (preferred) | `"".join(lst)` | **O(n)** | O(n) | Single allocation for the whole result; always prefer this |
| Slicing | `s[i:j]` | **O(k)** | O(k) | k = j − i; copies the selected characters into a new string |
| Count occurrences | `s.count(t)` | **O(n · m)** | O(1) | Full scan of s for every candidate position |
| Replace | `s.replace(a, b)` | **O(n)** | O(n) | Returns a new string; original is unchanged |
| Split | `s.split(sep)` | **O(n)** | O(n) | Output list holds the resulting substrings |
| Strip whitespace | `s.strip()` | **O(n)** | O(n) | Scans both ends; returns a new string |
| Upper / Lower | `s.upper()` | **O(n)** | O(n) | Every character is re-mapped into a new string |

> ⚠️ **The loop-concatenation trap** is one of the most common hidden O(n²) bugs in string problems. Always collect characters or segments in a list and call `"".join()` exactly once at the end.

---

## 🌍 Real-World Applications

Strings are among the most processed data types in software engineering. Understanding their performance characteristics is not just academic — it directly affects the systems you build.

### Natural Language Processing (NLP)
Every NLP pipeline — from spam filters to large language models — begins with raw text. Tokenisation (splitting a document into words or subwords), stemming, lemmatisation, and vocabulary lookups are all string-intensive operations. Frequency maps (`collections.Counter`) and trie structures, both rooted in string fundamentals, power autocomplete engines and search-as-you-type features in products used by billions of people.

### Data Parsing & ETL
Log files, CSV records, JSON payloads, and HTML documents are all strings at rest. Data engineers write parsers that scan, slice, and pattern-match billions of characters daily. Choosing `str.split()` over a regex when the separator is fixed, or streaming a file line-by-line instead of loading it entirely into memory, are real-world decisions that hinge on the same Big O reasoning applied here.

### Bioinformatics & DNA Sequencing
A DNA strand is literally a string over the four-character alphabet `{A, C, G, T}`. Finding a gene motif inside a genome is a substring search problem (O(n · m) naïvely; O(n + m) with KMP or Rabin-Karp). Sequence alignment algorithms such as Smith-Waterman and Needleman-Wunsch are dynamic-programming solutions applied directly to strings.

### Cryptography & Security
Password hashing, JWT token parsing, Base64 encoding/decoding, and TLS certificate validation all operate on byte strings. String immutability is a security feature here: an authenticated token cannot be silently mutated in memory by another part of the program.

### Compilers & Interpreters
Every programming language starts as a string of source code. The lexer tokenises it, the parser builds an AST from those tokens, and the code generator emits a new string (assembly or bytecode). Pattern matching on strings is at the heart of every compiler front-end.

---

## 🐍 Python Code Snippet — Two-Pointer Palindrome Check

A **palindrome** reads identically forwards and backwards (`"racecar"`, `"madam"`). The two-pointer technique achieves this in **O(n) time and O(1) auxiliary space** — no reversed copy is built, no extra list is allocated.

```python
# ─────────────────────────────────────────────────────────────────
# Two-Pointer Palindrome Check
# Time:  O(n)  — each character is visited at most once
# Space: O(1)  — only two integer index variables; nothing extra
#
# Core insight: place one pointer at each end of the string and
# march them inward simultaneously. The instant a mismatch is
# detected, the string cannot be a palindrome — return early.
# ─────────────────────────────────────────────────────────────────

def is_palindrome(s: str) -> bool:
    """Pure palindrome check — no filtering."""
    left, right = 0, len(s) - 1

    while left < right:
        if s[left] != s[right]:
            return False        # mismatch → cannot be a palindrome
        left  += 1
        right -= 1

    return True                 # all symmetric pairs matched ✅


# ── LC 125 variant: skip non-alphanumeric, ignore case ────────────
def is_palindrome_lc125(s: str) -> bool:
    """
    LeetCode 125 — Valid Palindrome.
    Considers only alphanumeric characters; treats upper and lower
    case as equal. Achieves O(n) time and O(1) space by never
    constructing a filtered copy of the string.
    """
    left, right = 0, len(s) - 1

    while left < right:
        # skip non-alphanumeric characters from the left
        while left < right and not s[left].isalnum():
            left += 1
        # skip non-alphanumeric characters from the right
        while left < right and not s[right].isalnum():
            right -= 1

        if s[left].lower() != s[right].lower():
            return False        # case-insensitive mismatch

        left  += 1
        right -= 1

    return True


# ── Quick demo ────────────────────────────────────────────────────
if __name__ == "__main__":
    tests = [
        ("racecar",                        True),
        ("hello",                          False),
        ("A man, a plan, a canal: Panama",  True),
        ("Was it a car or a cat I saw?",    True),
        ("Not a palindrome",               False),
    ]

    print(f"{'Input':<45} {'Expected':<10} {'Result':<10} {'Pass?'}")
    print("─" * 75)
    for s, expected in tests:
        result = is_palindrome_lc125(s)
        icon   = "✅" if result == expected else "❌"
        print(f"{s!r:<45} {str(expected):<10} {str(result):<10} {icon}")
```

### Two-Pointer — Step-by-Step Visualisation

```
Input:  s = "r a c e c a r"
Index:       0 1 2 3 4 5 6

Step 1:  left=0, right=6  →  s[0]='r' == s[6]='r'  ✅  →  converge
Step 2:  left=1, right=5  →  s[1]='a' == s[5]='a'  ✅  →  converge
Step 3:  left=2, right=4  →  s[2]='c' == s[4]='c'  ✅  →  converge
Step 4:  left=3, right=3  →  left >= right           →  return True
```

The two pointers together visit every character **exactly once**, and no additional memory is allocated — this is the canonical O(n) / O(1) solution pattern you will reach for in many string problems.

---

## ✅ LeetCode Problem Tracker

| # | Problem | Difficulty | Core Pattern | Status |
|---|---|---|---|---|
| 125 | [Valid Palindrome](https://leetcode.com/problems/valid-palindrome/) | 🟢 Easy | Two Pointers + alphanumeric filter | - [ ] |
| 242 | [Valid Anagram](https://leetcode.com/problems/valid-anagram/) | 🟢 Easy | Character frequency map / sorted comparison | - [ ] |

### Checkbox version (for local tracking)

- [ ] **LC 125 — Valid Palindrome** · Use two pointers from both ends. At each step, call `.isalnum()` to skip non-alphanumeric characters, then compare `.lower()` versions. No cleaned string is ever built — space stays O(1).

- [ ] **LC 242 — Valid Anagram** · Two strings are anagrams iff their character frequencies are identical. Use `collections.Counter(s) == collections.Counter(t)` for an O(n) solution with at most 26 keys (O(1) space for lowercase-only input). Alternative: sort both strings and compare — O(n log n) time, but simpler to reason about.

---

## 💡 Common String Patterns — Quick Reference

```
Pattern                   When to reach for it
───────────────────────── ───────────────────────────────────────────────────
Two Pointers              Palindromes, in-place reversals, opposite-end checks
Sliding Window            Longest substring without repeats, min window substring
Character Frequency Map   Anagrams, permutation checks, most-frequent character
String Builder (join)     Any loop that assembles a result character by character
Trie                      Prefix search, autocomplete, word-dictionary problems
KMP / Rabin-Karp          Efficient substring search — O(n + m) instead of O(n·m)
```

---

## 🗂️ Folder Structure

```
02_Strings/
├── README.md                ← you are here
├── valid_palindrome.py
└── valid_anagram.py
```

---

## 🔗 Further Reading

- [Python `str` documentation](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)
- [CPython string interning internals](https://docs.python.org/3/library/sys.html#sys.intern)
- [Time Complexity — Python Wiki](https://wiki.python.org/moin/TimeComplexity)
- [NeetCode Strings Roadmap](https://neetcode.io/roadmap)

---

*Part of the [DSA-Leetcode-Journey](../../README.md) repository · Previous: [01\_Arrays](../01_Arrays/README.md)*
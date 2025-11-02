# 🐍 Python Coding Challenge: Log Summarizer

**Duration:** 30 minutes  
**Goal:** Demonstrate Python fluency and ability to write clean, correct, and readable code.
---
## 📋 Problem Description

You are asked to build a **log summarizer** that reads application logs from **standard input** and prints a concise summary to **standard output**.

Each log line is **tab-separated (TSV)** with exactly four fields:

<timestamp>\t<level>\t<module>\t<message>



Where:

| Field | Description | Example |
|--------|--------------|----------|
| `timestamp` | ISO-8601 format (no timezone) | `2025-10-14T11:22:33` |
| `level` | One of `DEBUG`, `INFO`, `WARN`, `ERROR` | `ERROR` |
| `module` | Module or subsystem name | `api.gateway` |
| `message` | Log message text | `Query failed: timeout reached` |

---

## ✅ Program Requirements

### Input
1. **First line:** integer `N` (number of log lines).
2. **Next N lines:** each is a log entry as described above.

### Output
Your program must print **four lines** of summary in this exact order:

---

### 1️⃣ LEVEL COUNTS

Counts of log levels in fixed order: `DEBUG`, `INFO`, `WARN`, `ERROR`.

LEVEL_COUNTS debug=<n> info=<n> warn=<n> error=<n>

---

### 2️⃣ TIME RANGE

Earliest and latest timestamps seen (inclusive).
TIME_RANGE first=<ISO> last=<ISO>

If there are no lines, print:
TIME_RANGE first=none last=none


---

### 3️⃣ NOISY MODULE

The module that produced the **most ERROR logs**.  
Break ties by choosing the **lexicographically smallest** module name.  
If there are no ERROR logs, print `none`.



---

### 4️⃣ TOP WORDS

Print the **top 5 most frequent words** from all `message` fields, excluding stopwords and words shorter than 3 characters.

**Rules:**
- Case-insensitive (`User` = `user`)
- Split on non-alphabetic characters  
  (`can't` → `can`, `t`)
- Keep only tokens of letters `a–z`
- Exclude common **stopwords** (listed below)
- Sort by:
  - Frequency (descending)
  - Alphabetically (ascending) for ties

Print in the following format:
TOP_WORDS word1=c1, word2=c2, word3=c3, word4=c4, word5=c5


If there are fewer than 5 valid words, print only the ones available.  
If no valid words exist, print:



---

## 🚫 Stopwords List

Ignore the following words (case-insensitive):

{"the","and","for","with","from","this","that","you","your","are","was","were",
"has","have","had","but","not","can","cannot","cant","will","would","should",
"could","into","over","under","out","in","on","to","of","by","at","is","it",
"its","as","be"}


---

## 🧮 Example

### Input
12
2025-10-14T11:00:00 INFO auth User login success for arthur
2025-10-14T11:00:03 WARN api.gateway Slow response from upstream
2025-10-14T11:00:04 ERROR api.gateway Upstream timeout after 30s
2025-10-14T11:01:00 DEBUG db Connection pool size=12
2025-10-14T11:01:05 INFO auth User logout arthur
2025-10-14T11:02:10 ERROR db Query failed: deadlock detected
2025-10-14T11:02:11 ERROR db Query failed: retry limit reached
2025-10-14T11:03:00 INFO api.gateway Request GET /health
2025-10-14T11:04:00 INFO api.gateway Request GET /orders
2025-10-14T11:05:00 WARN db Lock wait exceeded for trx
2025-10-14T11:06:00 DEBUG auth Auth cache refresh ok
2025-10-14T11:06:30 INFO db Maintenance window starts


### Output
LEVEL_COUNTS debug=2 info=6 warn=2 error=3
TIME_RANGE first=2025-10-14T11:00:00 last=2025-10-14T11:06:30
NOISY_MODULE db
TOP_WORDS query=2, failed=2, upstream=1, timeout=1, user=1


---

## 🧩 Edge Cases

| Situation | Expected Behavior |
|------------|-------------------|
| No input lines | Output all zeros or "none" as shown above |
| Invalid level or missing field | Safe to ignore or treat as non-matching |
| Tied error counts | Pick lexicographically smallest module |
| Fewer than 5 unique words | Print only available words |
| Words with punctuation/numbers | Strip and tokenize correctly |

---

## 🛠️ Implementation Notes

- You may use **any part of the Python standard library**.
- Recommended modules:  
  `collections.Counter`, `datetime`, `re`, `sys`
- Suggested helper functions:
  - `parse_line(line: str)`
  - `tokenize_message(msg: str)`
  - `update_counts(...)`
  - `solve(stdin, stdout)` for testing
- Keep your code **modular, clear, and readable**.
- Include short **docstrings** and type hints where appropriate.

---

## ⏱️ Constraints

| Resource | Limit |
|-----------|--------|
| **Time limit** | 5 seconds |
| **Memory limit** | 256 MB |
| **Source size** | 1024 KB |

---

## 🧠 Evaluation Criteria

| Category | Weight | What is assessed |
|-----------|---------|------------------|
| **Correctness** | 80% | Output matches spec, handles edge cases |
| **Python Fluency** | 15% | Use of idiomatic, clean Python |
| **Code Hygiene** | 5% | Readability, naming, comments, structure |

---

## 🌟 Bonus (Optional Stretch Goals)

If you finish early, try adding one of the following features:
- Add a CLI flag `--top K` to change number of top words (default 5)
- Support timestamps with timezones (`Z`, `+00:00`)
- Allow a `--stopwords path` argument to load stopwords from a file

---

## 🧪 Quick Test Checklist

Before submitting, verify that:
- ✅ The program handles zero or many log lines gracefully  
- ✅ Output matches the required format exactly  
- ✅ Tie-breaking rules are correct (lexicographic for modules, alphabetical for words)  
- ✅ The solution runs efficiently and cleanly with no extra dependencies  

---

### 🎯 Summary

Your task is to write a **single Python program** that:
1. Reads logs from stdin  
2. Summarizes counts, time range, noisy module, and common words  
3. Produces clean, correctly formatted output  
4. Uses clear and maintainable Pythonic code  

This exercise tests your ability to **write real-world production Python**, not to solve a math puzzle.

Good luck! 💪



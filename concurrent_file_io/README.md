# 🚀 Concurrent File Processor Challenge

**Duration:** 45-60 minutes  
**Level:** Beginner to Intermediate  
**Goal:** Build a practical file processing system that demonstrates real-world concurrency patterns using Python's `asyncio` and `threading` modules.

---

## 📋 Problem Description

You work for a data analytics company that receives large batches of CSV files from various clients. Your task is to build a **concurrent file processor** that can handle multiple files simultaneously while providing real-time progress feedback to users.

The system should process files containing customer transaction data, calculate statistics, and generate summary reports—all while keeping the user informed of progress through a visual spinner and status updates.

---

## 🎯 Requirements

### Core Functionality

Your program must implement **three concurrent components**:

1. **File Processor** - Processes CSV files and calculates statistics
2. **Progress Spinner** - Shows visual feedback during processing  
3. **Status Monitor** - Tracks and reports processing progress

### Input Data Format

Each CSV file contains transaction records with these columns:
- **transaction_id**: Unique identifier for each transaction
- **customer_id**: Customer identifier
- **amount**: Transaction amount (decimal)
- **date**: Transaction date (YYYY-MM-DD format)
- **category**: Transaction category (groceries, electronics, dining, etc.)

### Processing Requirements

For each file, calculate:
- **Total transactions:** Count of all records
- **Total amount:** Sum of all transaction amounts
- **Average transaction:** Mean transaction value
- **Top category:** Most frequent transaction category
- **Date range:** Earliest and latest transaction dates
- **Processing time:** How long the file took to process

---

## 🔧 Technical Specifications

### 1. File Processing (Async)
**Function:** `process_file(filename: str) -> dict`

**Purpose:** Process a single CSV file and return comprehensive statistics

**Implementation Requirements:**
- Read CSV file asynchronously
- Parse each row and extract transaction data
- Add artificial delays every 100 rows (`await asyncio.sleep(0.1)`) to simulate I/O operations
- Calculate all required statistics (count, sum, average, etc.)
- Handle file errors gracefully
- Return results as a dictionary with all calculated metrics

### 2. Progress Spinner (Async)
**Function:** `show_spinner(message: str) -> None`

**Purpose:** Display a rotating visual indicator to show processing is active

**Implementation Requirements:**
- Use `itertools.cycle()` to rotate through spinner characters: `\ | / -`
- Update display every 0.1 seconds
- Print spinner and message on same line (use `\r` for carriage return)
- Handle `asyncio.CancelledError` when task is cancelled
- Clear spinner display when finished (print blank spaces to overwrite)
- Ensure smooth animation without flickering

### 3. Status Monitor (Async)
**Function:** `monitor_progress(filenames: list, results: dict) -> None`

**Purpose:** Track and report processing progress in real-time

**Implementation Requirements:**
- Update progress display every 2 seconds
- Show format: "Processed X of Y files (Z%)"
- List names of completed files
- Calculate and display estimated time remaining
- Access shared results dictionary safely
- Continue monitoring until all files are processed
- Handle concurrent updates to results dictionary

### 4. Main Coordinator (Async)
**Function:** `process_batch(filenames: list) -> dict`

**Purpose:** Orchestrate concurrent processing of multiple files

**Implementation Requirements:**
- Create and start spinner task for visual feedback
- Create and start progress monitor task
- Limit concurrent file processing to maximum of 3 files
- Use `asyncio.Semaphore` for concurrency control
- Coordinate all async tasks properly
- Handle task cancellation and cleanup
- Collect and return consolidated results from all files
- Ensure all background tasks are properly terminated

---

## 📁 Sample Data Structure

Create test CSV files with this structure:

**transactions_001.csv format:**
- Header row: transaction_id,customer_id,amount,date,category
- Sample data rows with various transaction types
- Mix of different categories (groceries, electronics, dining, etc.)
- Date range spanning multiple days
- Varying transaction amounts for realistic statistics

**Expected Output Structure:**
The function should return a dictionary containing:
- **total_transactions**: Integer count of all records
- **total_amount**: Sum of all transaction amounts (float)
- **average_transaction**: Mean transaction value (float)
- **top_category**: Most frequently occurring category (string)
- **date_range**: Dictionary with 'earliest' and 'latest' dates
- **processing_time**: Time taken to process the file (float, seconds)
- **status**: Processing status ('completed', 'error', etc.)

---

## 🔄 Concurrency Patterns to Implement

### Pattern 1: Task Coordination
**Concept:** Create and manage multiple async tasks concurrently

**Implementation Guide:**
- Use `asyncio.create_task()` to start background tasks (spinner, monitor)
- Coordinate main processing work with background feedback tasks
- Use `await` to wait for main processing to complete
- Cancel background tasks when main work is done
- Handle task cleanup and resource management properly

### Pattern 2: Cooperative Yielding
**Concept:** Allow other tasks to run during CPU-intensive operations

**Implementation Guide:**
- Add `await asyncio.sleep(0)` periodically during long-running loops
- Yield control every 100 rows or similar reasonable interval
- This prevents blocking the event loop during intensive processing
- Allows spinner and monitor tasks to update while processing files
- Essential for responsive user interface in async applications

### Pattern 3: Bounded Concurrency
**Concept:** Limit the number of concurrent operations to prevent resource exhaustion

**Implementation Guide:**
- Use `asyncio.Semaphore(3)` to limit concurrent file processing
- Wrap file processing function to acquire/release semaphore
- Use `async with semaphore:` context manager for automatic cleanup
- Create tasks for all files but semaphore controls actual concurrency
- Use `asyncio.gather()` to wait for all tasks to complete
- This prevents overwhelming system resources with too many concurrent operations

---

## ✅ Success Criteria

Your solution should demonstrate:

1. **Visual Feedback:** Spinner rotates smoothly during processing
2. **Progress Updates:** Status monitor shows real-time progress every 2 seconds
3. **Concurrent Processing:** Multiple files processed simultaneously (max 3)
4. **Proper Cleanup:** All tasks cancelled gracefully when processing completes
5. **Error Handling:** Graceful handling of missing files or corrupted data
6. **Performance:** Processing 5 files (100 rows each) in under 10 seconds

### Sample Console Output:
The program should produce output similar to this format:
- Initial message indicating batch processing has started
- Rotating spinner characters with processing message
- Periodic progress updates showing completion percentage
- List of completed files as they finish processing
- Final completion message with checkmark or success indicator
- Summary statistics including total files, transactions, amounts, and timing

---

## 🧩 Extension Challenges (Optional)

1. **Threading Integration:** Add a background thread that saves results to a database
2. **Real-time Dashboard:** Use `curses` library to create a terminal-based dashboard
3. **Configuration:** Add command-line arguments for batch size and processing limits
4. **Retry Logic:** Implement retry mechanism for failed file processing
5. **Memory Management:** Process very large files in chunks to manage memory usage

---

## 🛠️ Implementation Tips

### Getting Started
1. Create sample CSV files with varying sizes (10, 50, 100 rows)
2. Implement the spinner first—it's satisfying and helps with debugging
3. Build file processing incrementally (read → parse → calculate → return)
4. Add concurrency last, starting with sequential processing

### Common Pitfalls
- **Don't forget `await`** - CPU-intensive loops need `await asyncio.sleep(0)`
- **Handle cancellation** - Always catch `asyncio.CancelledError` in long-running tasks
- **Resource cleanup** - Cancel all tasks in finally blocks
- **Shared state** - Use appropriate synchronization for shared data structures

### Testing Strategy
**Basic Test Implementation:**
- Create temporary CSV files with known data for testing
- Use `tempfile.NamedTemporaryFile()` for temporary test files
- Write test data with `csv.writer()` 
- Call your `process_file()` function with test file
- Assert that calculated results match expected values
- Test edge cases like empty files, single rows, missing data
- Verify that async behavior works correctly with multiple files

---

## 📚 Key Learning Outcomes

By completing this challenge, you'll understand:

- **Asyncio fundamentals:** Tasks, coroutines, and event loops
- **Cooperative concurrency:** When and how to yield control
- **Task management:** Creating, coordinating, and cancelling tasks
- **Real-world patterns:** Progress reporting, bounded concurrency, graceful shutdown
- **Performance considerations:** I/O vs CPU-bound operations in async code

---

## 🎯 Evaluation Criteria

| Criterion | Weight | Description |
|-----------|--------|-------------|
| **Correctness** | 40% | Calculations are accurate, files processed completely |
| **Concurrency** | 30% | Proper use of asyncio, tasks run concurrently |
| **User Experience** | 20% | Smooth spinner, clear progress updates |
| **Code Quality** | 10% | Clean, readable, well-structured code |

---

This challenge simulates real-world scenarios where you need to process multiple data sources concurrently while keeping users informed of progress. It's perfect for learning practical concurrency patterns that you'll use in production applications! 🚀
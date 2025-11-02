# GitHub Commit Analyzer Challenge

## 🎯 Challenge Overview

Build a Python script that fetches commit data from a GitHub repository, aggregates it by month, calculates statistics, and sends the results to a webhook endpoint.

This challenge tests your ability to:
- Work with REST APIs (GitHub API)
- Process and aggregate JSON data
- Handle datetime parsing and formatting
- Calculate statistical metrics
- Send HTTP requests (GET and POST)
- Structure data for external consumption

---

## 📋 Requirements

### Input Parameters
The script should work with these repository variables:
```python
repo_owner = "ahvar"
repo_name = "gene_annotator"  # or any valid GitHub repository
```


## API Endpoint
GitHub API: https://api.github.com/repos/{owner}/{repo}/commits?per_page=100
Method: GET
Response: JSON array of commit objects
Data Processing Steps
Fetch Commits: Retrieve up to 100 recent commits from the specified repository

### Extract Required Fields from each commit:

commit.author.date - ISO 8601 timestamp
commit.message - commit message text
commit.author.name - author name
Group by Month: Aggregate commits by month-year in format "MM-YYYY"

### Calculate Monthly Statistics:

Metric	Description
commit_count	Total number of commits in that month
average_message_length	Average character length of commit messages (rounded to nearest integer)
unique_authors	Number of distinct commit authors by name
Output Format
Generate a JSON array sorted by date (most recent first):

[
  {
    "date": "06-2025",
    "commit_count": 80,
    "average_message_length": 90,
    "unique_authors": 2
  },
  {
    "date": "05-2025", 
    "commit_count": 20,
    "average_message_length": 72,
    "unique_authors": 3
  }
]

### Webhook Delivery
Method: POST
Content-Type: application/json
Body: The complete JSON array
Endpoint: Use webhook.site to generate a test URL
Success: Print confirmation with HTTP status code

### Testing & Validation

Test Cases
Valid Repository: Use a repository with multiple months of commits
Single Author: Repository with commits from one author
Multiple Authors: Repository with diverse contributors
Varying Message Lengths: Mix of short and long commit messages
API Errors: Handle repository not found, rate limits, network issues

### Validation Checklist
 Fetches commits successfully from GitHub API
 Groups commits correctly by month-year
 Calculates accurate commit counts
 Computes correct average message lengths (rounded)
 Counts unique authors properly
 Formats dates as "MM-YYYY"
 Sorts output by date (newest first)
 Sends valid JSON to webhook
 Handles errors gracefully
 Prints success confirmation


# Extensions (Optional)
For additional practice, consider extending the solution with:

CLI Interface: Accept repository parameters as command-line arguments
Configuration: Support for GitHub API tokens
Pagination: Handle repositories with >100 commits
Multiple Repositories: Compare statistics across repositories
Data Export: Save results to CSV or database
Visualization: Generate charts of commit activity
Testing: Unit tests for core functions
Logging: Structured logging for debugging


This README provides a complete specification that covers all the requirements evident in your implementation, plus additional context for testing and extensions.This README provides a complete specification that covers all the requirements evident in your implementation, plus additional context for testing and extensions.
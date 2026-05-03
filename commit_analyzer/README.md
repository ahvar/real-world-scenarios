# GitHub Commits Aggregator

## 🧭 Overview
This project implements a Python script that retrieves recent commits from a GitHub repository, processes the data to generate monthly statistics, and sends the results to a webhook endpoint.

The script demonstrates the ability to:
- Work with external APIs (GitHub REST API)
- Parse and aggregate structured JSON data
- Handle dates and string processing
- Perform HTTP requests (GET and POST)
- Produce and send structured output

---

## 📥 Input

The script should accept two required variables:
```python
repo_owner = "ahvar"
repo_name = "data-structures-algorithms"
```
https://api.github.com/repos/{repo_owner}/{repo_name}/commits?per_page=100


## For each commit retrieved:

1. Extract the commit date (commit.author.date)

2. Extract the commit message text (commit.message)

3. Extract the commit author (name or email)

4. Then, group all commits by month and year in the format "MM-YYYY".

For each month group, calculate:

Metric	Description
commit_count	Total number of commits in that month
average_message_length	Average character length of commit messages
unique_authors	Number of distinct commit authors (by email or name)

```
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
```

After computing the aggregated data, send it as a JSON payload to the webhook URL below using a POST request.

## Solutions for This Exercise:
### Option 1: Create a New webhook.site URL

1. Go to https://webhook.site
2. You'll automatically get a new unique URL like: https://webhook.site/#!/12345678-abcd-1234-efgh-123456789abc/
3. Use that URL in your script



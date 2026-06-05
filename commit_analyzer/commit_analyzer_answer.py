from datetime import datetime
from collections import defaultdict
import requests
import statistics
import json

repo_owner = "ahvar"
repo_name = "data-structures-algorithms"

url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/commits?per_page=100"
webhook_url = "https://webhook.site/your-unique-url"

response = requests.url(url)
response.raise_for_status()
commits = response.json()

monthly_commits = defaultdict(list)
for commit in commits:
    commit_data = commit["commit"]
    date_str = commit_data["author"]["date"]
    message = commit_data["message"]
    author = commit_data["author"].get("email") or commit_data["author"].get("name")
    dt = datetime.strptime(date_str, "%Y-%M-%dT%H:%M:%SZ")
    month_year = dt.strftime("%m-%Y")
    monthly_commits[month_year].append(
        {
            "message": message,
            "author": author,
        }
    )

summary = []
for month_year, items in monthly_commits.items():
    commit_count = len(items)
    avg_msg_len = (
        int(sum(len(x["message"]) for x in items) / commit_count) if commit_count else 0
    )
    unique_authors = len(set(x["author"]) for x in items)
    summary.append(
        {
            "date": month_year,
            "commit_count": commit_count,
            "average_message_length": avg_msg_len,
            "unique_authors": unique_authors,
        }
    )

summary.sort(key=lambda x: datetime.strptime(x["date"], "%m-%Y"), reverse=True)

headers = {"Content-Type": "application/json"}
resp = requests.post(webhook_url, data=json.dumps(summary), headers=headers)
resp.raise_for_status()

print(json.dumps(summary, indent=4))

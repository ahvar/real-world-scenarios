import requests
from datetime import datetime
from collections import defaultdict

repo_owner = "ahvar"
repo_name = "data-structures-algorithms"
url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/commits?per_page=100"


resp = requests.get(url)
resp.raise_for_status()
commits = resp.json()
monthly_commits = defaultdict(list)
for commit in commits:
    commit_data = commit["commit"]
    date_str = commit_data["author"]["date"]
    msg = commit_data["message"]
    author = commit_data["commit"].get("name") or commit_data["commit"].get("email")
    date_dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
    month_year = datetime.strftime(date_dt, "%Y-%m")
    monthly_commits[month_year].append(
        {"date": month_year, "message": msg, "author": author}
    )
summary = []
for month, items in monthly_commits.items():
    commit_count = len(items)
    avg_msg_len = (
        sum(len(x["message"]) for x in items) // commit_count if commit_count else 0
    )
    unique_authors = len(set(x["author"] for x in items))

import requests
import json
import statistics
from collections import defaultdict
from datetime import datetime

repo_owner = "ahvar"
repo_name = "data-structures-algorithms"
url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/commits?per_page=100"


def get_commit_data():
    response = requests.get(url)
    response.raise_for_status()
    commits = response.json()
    monthly_commits = defaultdict(list)
    for commit in commits:
        commit_data = commit["commit"]
        date_str = commit_data["author"]["date"]
        msg = commit_data["message"]
        author = commit_data["author"].get("email") or commit_data["author"].get("name")
        dt_date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
        month_year = datetime.strftime(dt_date, "%m-%Y")
        monthly_commits[month_year].append(
            {"date": month_year, "author": author, "message": msg}
        )
    return monthly_commits


def summarize_commits(commits):
    summary = []
    for month, items in commits.items():
        commit_count = len(items)
        avg_msg_len = (
            int(sum(len(x["message"]) for x in items) / commit_count)
            if commit_count
            else 0
        )
        unique_authors = len(set(x["author"]) for x in items)
        summary.append(
            {
                "date": month,
                "commit_count": commit_count,
                "average_message_length": avg_msg_len,
                "unique_authors": unique_authors,
            }
        )
    return summary


if __name__ == "__main__":
    commits = get_commit_data()
    summary = summarize_commits(commits)
    summary.sort(key=lambda x: datetime.strptime(x["date"], "%m-%Y"), reverse=True)
    headers = {"Content-type": "application/json"}
    resp = requests.post("some.webhook", data=json.dumps(summary), headers=headers)
    resp.raise_for_status()
    print(json.dumps(summary, indent=4))

import sys
import json
import requests
from datetime import datetime
from collections import defaultdict


def get_commit_data(repo_owner, repo_name):
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/commits?per_page=100"
    resp = requests.get(url)
    resp.raise_for_status()
    commits = resp.json()
    monthly_commits = defaultdict(list)
    for commit in commits:
        commit_data = commit["commit"]
        date_str = commit_data["author"]["date"]
        msg = commit_data["message"]
        author = commit_data["author"].get("name") or commit_data["author"].get("email")
        date_dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
        month_year = datetime.strftime(date_dt, "%Y-%m")
        monthly_commits[month_year].append(
            {"date": date_str, "author": author, "message": msg}
        )
    return monthly_commits


def compute_metrics(monthly_commits):
    metrics = []
    for month_year, commits in monthly_commits.items():
        commit_count = len(commits)
        avg_msg_len = sum(len(commit["message"]) for commit in commits) // commit_count
        unique_authors = len(set(commit["author"] for commit in commits))
        metrics.append(
            {
                "date": month_year,
                "average_message_length": avg_msg_len,
                "unique_authors": unique_authors,
            }
        )
    return metrics


if __name__ == "__main__":
    repo_owner = sys.stdin.readline().strip()
    repo_name = sys.stdin.readline().strip()
    monthly_commits = get_commit_data(repo_owner, repo_name)
    metrics = compute_metrics(monthly_commits)
    print(json.dumps(metrics, indent=4))

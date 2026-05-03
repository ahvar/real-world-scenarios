from dotenv import load_dotenv
from config import Config
from collections import defaultdict
from datetime import datetime
import requests
import json

url = f"https://api.github.com/repos/{Config.REPO_OWNER}/{Config.REPO_NAME}/commits?per_page=100"


def retrieve_commit_data():
    monthly_commits = defaultdict(list)
    resp = requests.get(url)
    commit_json = resp.json()
    for commit_data in commit_json:
        commit = commit_data["commit"]
        author = commit.get("author", {})
        if not author:
            continue
        author_name_email = author.get("email") or author.get("name")
        msg = commit.get("message", "")
        date_str = author.get("date")
        date_dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
        month_year = datetime.strftime(date_dt, "%m-%Y")
        monthly_commits[month_year].append(
            {"author": author_name_email, "message": msg, "date": date_str}
        )

    return monthly_commits


def calculate_metrics(monthly_commits):
    metrics = []
    for month_year, commits in monthly_commits.items():
        metrics.append(
            {
                "date": month_year,
                "commit_count": len(commits),
                "average_message_length": sum([len(c["message"]) for c in commits])
                / len(commits),
                "unique_authors": len(set(c["author"] for c in commits)),
            }
        )
    return metrics


if __name__ == "__main__":
    monthly_commits = retrieve_commit_data()
    metrics = calculate_metrics(monthly_commits)
    print(json.dumps(metrics, indent=4))

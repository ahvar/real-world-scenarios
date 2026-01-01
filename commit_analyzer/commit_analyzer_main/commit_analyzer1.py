import requests
import json
from collections import defaultdict
from datetime import datetime

repo_owner = "ahvar"
repo_name = "data-structures-algorithms"
url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/commits?per_page=100"


def get_commits():
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def extract_metrics(commits):
    metrics = defaultdict(list)
    for commit in commits:
        commit_data = commit["commit"]
        date_str = commit_data["author"]["date"]
        msg = commit_data["message"]
        author = (
            commit_data["author"].get("name")
            or commit_data["author"].get("email")
            or "unknown"
        )
        date_dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
        month_year = datetime.strftime(date_dt, "%m-%Y")
        metrics[month_year].append({"date": date_str, "author": author, "message": msg})
    return metrics


def summarize_by_month(metrics):
    result = []
    for month_year, items in metrics.items():
        commit_count = len(items)
        avg_msg_len = (
            sum(len(item["message"]) for item in items) / commit_count
            if commit_count
            else 0
        )
        unique_authors = len(set(item["author"] for item in items))
        result.append(
            {
                "date": month_year,
                "commit_count": commit_count,
                "average_message_length": avg_msg_len,
                "unique_authors": unique_authors,
            }
        )
    return result


if __name__ == "__main__":
    commits = get_commits()
    metrics = extract_metrics(commits)
    summary = summarize_by_month(metrics)
    summary.sort(key=lambda x: datetime.strptime(x["date"], "%m-%Y"), reverse=True)
    headers = {"Content-Type": "application/json"}
    requests.post("some.url.net", data=json.dumps(summary), headers=headers)


class TestCommitAnalyzer:

    def test_get_commits(self):
        commits = get_commits()
        # print(json.dumps(commits, indent=4))

    def test_extract_metrics(self):
        commits = get_commits()
        metrics = extract_metrics(commits)
        # print(json.dumps(metrics, indent=4))

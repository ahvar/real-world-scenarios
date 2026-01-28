import requests
import json
from collections import defaultdict
from datetime import datetime

repo_owner = "ahvar"
repo_name = "data-structures-algorithms"

url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/commits?per_page=100"


def get_commit_data():
    try:
        resp = requests.get(url)
        resp.raise_for_status()
        commits = resp.json()
    except Exception as ex:
        print(ex)
    return commits


def extract_date_msg_author(commits):
    commit_data_by_month = defaultdict(list)
    for commit in commits:
        commit_data = commit["commit"]
        date_str = commit_data["author"]["date"]
        msg = commit_data["message"]
        author = commit_data["author"].get("name", None) or commit_data["author"].get(
            "email", None
        )
        date_dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
        month_year = datetime.strftime(date_dt, "%Y-%m")
        commit_data_by_month[month_year].append(
            {"date": date_str, "message": msg, "author": author}
        )
    return commit_data_by_month


def summarize(commit_data_by_month):
    summary = []
    for month_year, items in commit_data_by_month.items():
        commit_count = len(items)
        avg_msg_len = (
            int(sum(len(x["message"]) for x in items)) // commit_count
            if commit_count
            else 0
        )
        unique_authors = len(set(x["author"] for x in items))
        summary.append(
            {
                "date": month_year,
                "commit_count": commit_count,
                "average_message_length": avg_msg_len,
                "unique_authors": unique_authors,
            }
        )
    return summary


if __name__ == "__main__":
    commit_data = get_commit_data()


class TestCommitAnalyzer:
    def test_get_commit_data(self):
        commits = get_commit_data()
        assert commits != None
        print(json.dumps(commits[0], indent=4))

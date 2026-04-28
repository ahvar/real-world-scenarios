import requests
import json
from collections import defaultdict
from datetime import datetime


class CommitAnalyzer:

    def __init__(self):
        self._repo_owner = "ahvar"
        self._repo_name = "ahvar.github.io"
        self._commits = {}
        self._commits_by_month = defaultdict(list)

    def load_commits(self):
        url = f"https://api.github.com/repos/{self._repo_owner}/{self._repo_name}/commits?per_page=100"
        resp = requests.get(url)
        resp.raise_for_status()
        self._commits = resp.json()

    def load_date_msg_author_from_commits(self):
        if not self._commits:
            return
        for commit in self._commits:
            commit_data = commit["commit"]
            date_str = commit_data["author"]["date"]
            msg = commit_data["message"]
            author = commit_data["author"]["name"] or commit_data["author"]["email"]
            date_dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
            month_year = datetime.strftime(date_dt, "%Y-%m")
            self._commits_by_month[month_year].append(
                {"date": date_str, "msg": msg, "author": author}
            )

    @property
    def commits(self):
        return self._commits

    @property
    def commits_by_month(self):
        return self._commits_by_month


class TestAnalyzer:
    def setup_method(self):
        self.commit_analyzer = CommitAnalyzer()

    def test_load_commits(self):
        self.commit_analyzer.load_commits()
        assert self.commit_analyzer.commits != None

    def test_load_month_year(self):
        self.commit_analyzer.load_commits()
        self.commit_analyzer.load_date_msg_author_from_commits()
        print(json.dumps(self.commit_analyzer.commits_by_month, indent=4))

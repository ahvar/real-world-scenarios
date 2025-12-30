import pytest
from commit_analyzer1 import get_commit_data


class TestCommitAnalyzer:

    def test_get_commits(self):
        monthly_commits = get_commit_data()
        assert monthly_commits != None

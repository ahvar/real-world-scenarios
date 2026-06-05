import requests
import json
from datetime import datetime
from collections import defaultdict
from flask import render_template, Blueprint, request

bp = Blueprint("routes", __name__)

repo_owner = "ahvar"
repo_name = "data-structures-algorithms"
url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/commits?per_page=100"


def get_monthly_commits():

    resp = requests.get(url)
    respj = resp.json()
    monthly_commits = defaultdict(list)
    for obj in respj:
        commit_data = obj["commit"]
        author_data = commit_data.get("author", {})
        date_str = author_data.get("date", "")
        name_or_email = author_data.get("name", "") or author_data.get("email", "")
        msg = commit_data.get("message", "")
        date_dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
        month_year = datetime.strftime(date_dt, "%m-%Y")
        monthly_commits[month_year].append(
            {"date": date_str, "author": name_or_email, "msg": msg}
        )
    return monthly_commits


def get_commit_summary():
    monthly_commits = get_monthly_commits()
    output = []
    for month, commits in monthly_commits.items():
        commit_count = len(commits)
        avg_msg_len = sum(len(c["msg"]) for c in commits) // commit_count
        author_count = len(set(c["author"] for c in commits))
        output.append(
            {
                "date": month,
                "commit_count": commit_count,
                "average_message_length": avg_msg_len,
                "unique_authors": author_count,
            }
        )
    return output


@bp.route("/")
@bp.route("/index", methods=["GET"])
def index():
    user_agent = request.headers.get("User-Agent")
    render_template("index.html")


@bp.route("/commits/<month>", methods=["GET"])
def monthly_commits(month):
    monthly_commits = get_monthly_commits()


@bp.route("/commits/summary", methods=["GET"])
def commits_summary():
    summary = get_commit_summary()

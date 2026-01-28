from . import app
from collections import defaultdict
from datetime import datetime
from flask import current_app, render_template, jsonify
import requests


def retrieve_monthly_commit_data() -> defaultdict:
    repo_owner = current_app.config["REPO_OWNER"]
    repo_name = current_app.config["REPO_NAME"]
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/commits?per_page=100"
    resp = requests.get(url)
    resp.raise_for_status()
    commits = resp.json()
    monthly_commits = defaultdict(list)
    for commit in commits:
        commit_data = commit["commit"]
        date_str = commit_data["author"]["date"]
        msg = commit_data["message"]
        author = commit_data["author"].get("name", None) or commit_data["author"].get(
            "email", None
        )
        date_dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
        month_year = datetime.strftime(date_dt, "%Y-%m")
        monthly_commits[month_year].append(
            {"date": month_year, "message": msg, "author": author}
        )
    return monthly_commits


def summarize_commit_metrics():
    monthly_commits = retrieve_monthly_commit_data()
    metrics = []
    for month, items in monthly_commits.items():
        commit_count = len(items)
        avg_msg_len = sum(len(x["message"]) for x in items) // commit_count
        unique_authors = len(set(x["author"] for x in items))
        metrics.append(
            {
                "date": month,
                "commit_count": commit_count,
                "average_message_length": avg_msg_len,
                "unique_authors": unique_authors,
            }
        )
    return sorted(metrics, key=lambda x: ["date"], reverse=True)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/commit-data")
def display_monthly_commit_data():
    monthly_commits = retrieve_monthly_commit_data()
    return render_template("monthly_commits.html", monthly_commits=monthly_commits)


@app.route("/metrics")
def display_metrics():
    metrics = summarize_commit_metrics()
    return render_template("metrics.html", metrics=metrics)

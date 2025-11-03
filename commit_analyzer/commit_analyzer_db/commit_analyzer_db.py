""" """

import requests
import statistics
import json
import sqlite3
from datetime import datetime
from pprint import PrettyPrinter

pp = PrettyPrinter(indent=4)
commit_db_path = "commits.db"
conn = sqlite3.connect(commit_db_path)
cursor = conn.cursor()


def init_db_create_tables():
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS Authors(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255),
        UNIQUE(name, email)
    )
    """
    )
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS Commits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sha VARCHAR(40) UNIQUE NOT NULL,
        date DATETIME NOT NULL,
        message TEXT NOT NULL,
        author_id INTEGER NOT NULL,
        repo_owner VARCHAR(100) NOT NULL,
        repo_name VARCHAR(100) NOT NULL,
        FOREIGN KEY (author_id) REFERENCES Authors(id) ON DELETE CASCADE
    )
    """
    )
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS MonthlySummary(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        month INTEGER NOT NULL CHECK (month BETWEEN 1 AND 12),
        year INTEGER NOT NULL CHECK (year > 1900),
        repo_owner VARCHAR(100) NOT NULL,
        repo_name VARCHAR(100) NOT NULL,
        commit_count INTEGER DEFAULT 0,
        unique_authors INTEGER DEFAULT 0,
        average_message_length REAL DEFAULT 0,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(month, year, repo_owner, repo_name)
    )
    """
    )
    conn.commit()


def get_commit_data(repo_owner, repo_name):
    github_url = (
        f"https://api.github.com/repos/{repo_owner}/{repo_name}/commits?per_page=100"
    )
    response = requests.get(github_url).json()
    return json.dumps(response, indent=4)


def get_monthly_summary(repo_owner, repo_name):
    github_url = (
        f"https://api.github.com/repos/{repo_owner}/{repo_name}/commits?per_page=100"
    )
    response = requests.get(github_url).json()
    monthly_commits = {}
    for each in response:
        commit_date = datetime.strptime(
            each["commit"]["author"]["date"], "%Y-%m-%dT%H:%M:%SZ"
        )
        month_year = f"{commit_date.month:02d}-{commit_date.year}"
        if month_year in monthly_commits:
            monthly_commits[month_year]["messages"].append(each["commit"]["message"])
            monthly_commits[month_year]["authors"].append(
                each["commit"]["author"]["name"]
            )
        else:
            monthly_commits[month_year] = {
                "messages": [each["commit"]["message"]],
                "authors": [each["commit"]["author"]["name"]],
            }
    month_summary = []
    for month_year, data in monthly_commits.items():
        month_summary.append(
            {
                "date": month_year,
                "commit_count": len(data["messages"]),
                "average_message_length": round(
                    statistics.mean([len(msg) for msg in data["messages"]])
                ),
                "unique_authors": len(set(data["authors"])),
            }
        )
    month_summary.sort(
        key=lambda x: datetime.strptime(x["date"], "%m-%Y"), reverse=True
    )
    return month_summary


def load_commit_data(repo_owner, repo_name):
    github_url = (
        f"https://api.github.com/repos/{repo_owner}/{repo_name}/commits?per_page=100"
    )
    response = requests.get(github_url).json()
    for each in response:
        commit_date = datetime.strptime(
            each["commit"]["author"]["date"], "%Y-%m-%dT%H:%M:%SZ"
        )
        # month_year = f"{commit_date.month:02d}-{commit_date.year}"
        name = each["commit"]["author"]["name"]
        email = each["commit"]["author"]["email"]
        msg = each["commit"]["message"]
        sha = each["sha"]
        insert_commit(
            sha,
            datetime.strftime(commit_date, "%Y-%m-%dT%H:%M:%SZ"),
            msg,
            name,
            email,
            repo_owner,
            repo_name,
        )
    conn.commit()


def insert_author(name, email=None):
    cursor.execute(
        """INSERT OR IGNORE INTO Authors (name, email) VALUES (?, ?)
""",
        (name, email),
    )
    cursor.execute(
        """
        SELECT id FROM Authors WHERE name = ? AND (email = ? OR (email IS NULL AND ? IS NULL)) 
""",
        (name, email, email),
    )
    return cursor.fetchone()[0]


def insert_commit(sha, date, message, author_name, author_email, repo_owner, repo_name):
    author_id = insert_author(author_name, author_email)
    cursor.execute(
        """INSERT OR REPLACE INTO COMMITS
                   (sha,date,message,author_id,repo_owner,repo_name)
                   VALUES (?,?,?,?,?,?)
""",
        (sha, date, message, author_id, repo_owner, repo_name),
    )
    return cursor.lastrowid


def post_to_webhook(data):
    response = requests.post(
        "https://webhook.site/4823ab23-3b35-4d63-ac29-27a6996c7f1f", json=data
    )
    response.raise_for_status()


if __name__ == "__main__":
    repo_owner = "ahvar"
    repo_name = "gene_annotator"
    print(get_commit_data(repo_owner, repo_name))
    init_db_create_tables()
    # print(json.dumps(get_monthly_summary(repo_owner, repo_name), indent=4))
    load_commit_data(repo_owner, repo_name)

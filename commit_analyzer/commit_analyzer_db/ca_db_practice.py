import sqlite3
import requests
from datetime import datetime


def fetch_commits(repo_owner, repo_name, per_page):
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/commits?per_page={per_page}"
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "codesignal-backend-practice-script",
    }

    resp = requests.get(url, headers=headers, timeout=20)
    resp.raise_for_status()
    commits = resp.json()
    return commits


def init_db(conn: sqlite3.Connection):
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS commits(
            sha TEXT PRIMARY KEY,
            author_id INTEGER NOT NULL,
            message TEXT NOT NULL,
            committed_at TEXT NOT NULL,
            month_key TEXT NOT NULL,
            month_label TEXT NOT NULL,
            FOREIGN KEY(author_id) REFERENCES authors(id)
        )
        """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS authors(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            author_key TEXT NOT NULL UNIQUE
        )
        """
    )

    cursor.execute(
        "CREATE INDEX IF NOT EXISTS idx_commits_author_id ON commits(author_id)"
    )
    cursor.execute(
        "CREATE INDEX IF NOT EXISTS idx_commits_month_key ON commits(month_key)"
    )
    cursor.execute(
        "CREATE INDEX IF NOT EXISTS idx_commits_committed_at ON commits(committed_at)"
    )

    conn.commit()
    return cursor


def parse_github_dt(date_str):
    """
    GitHub provides ISO 8601 like: '2025-06-10T12:34:56Z'
    Return:
      committed_at:  'YYYY-MM-DD HH:MM:SS'
      month_key:     'YYYY-MM'
      month_label:   'MM-YYYY'
    """
    date_dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
    committed_at = date_dt.strftime("%Y-%m-%d %H:%M:%SZ")
    month_key = date_dt.strftime("%Y-%m")
    month_label = date_dt.strftime("%m-%Y")
    return committed_at, month_key, month_label


def extract_author_key(item):
    """
    Prefer commit.author.email; fallback to commit.author.name; else 'unknown'.
    Note: GitHub top-level item["author"] may be null for unlinked emails.
    """
    commit_obj = item.get("commit", {}) or {}
    author_obj = commit_obj.get("author", {}) or {}
    email = author_obj.get("email")
    name = author_obj.get("name")
    return email or name or "unknown"


def extract_commit_fields(item):
    """
    Return (sha, message, date_str) or None if unusable.
    """
    sha = item.get("sha")
    commit_obj = item.get("commit", {}) or {}
    message = item.get("message", "") or ""

    author_obj = commit_obj["author"] or {}
    committer_obj = commit_obj.get("committer", {}) or {}
    date_str = author_obj.get("date") or committer_obj.get("date")

    if not sha or not date_str:
        return None
    return sha, message, date_str


def load_commits(conn: sqlite3.Connection, commits):
    cursor = conn.cursor()
    author_id_cache = {}
    for item in commits:
        fields = extract_commit_fields(item)
        if fields is None:
            continue

        sha, message, date_str = fields
        author_key = extract_author_key(item)
        committed_at, month_key, month_label = parse_github_dt(date_str)

        if author_key not in author_id_cache:
            cursor.execute(
                "INSERT OR IGNORE INTO authors(author_key) VALUES (?)",
                (author_key,),
            )
            cursor.execute(
                "SELECT id FROM authors WHERE author_key = ?",
                (author_key,),
            )
            row = cursor.fetchone()
            if row is None:
                continue
            author_id_cache[author_key] = int(row[0])
        author_id = author_id_cache[author_key]

        cursor.execute(
            """
            INSERT OR REPLACE INTO commits(sha, author_id, message, committed_at, month_key, month_label)
            VALUES (?,?,?,?,?,?)
            """,
            (sha, author_id, message, committed_at, month_key, month_label),
        )
    conn.commit()


def query_all(conn: sqlite3.Connection, sql: str):
    pass


def main():
    repos = [
        {"repo_owner": "ahvar", "repo_name": "data-structures-algorithms"},
        {"repo_owner": "ahvar", "repo_name": "real-world-scenarios"},
    ]
    all_commits = []
    for repo in repos:
        for k, v in repo.items():
            commits = fetch_commits(repo_owner=k, repo_name=v, per_page=100)
            all_commits.extend(commits)

    conn = sqlite3.connect("commits.db")
    init_db(conn)

    load_commits(conn, all_commits)

    monthly_summary_sql = """
        SELECT month_label AS date,
        COUNT(*) AS commit_count,
        CAST(AVG(LENGTH(message)) AS INT) AS average_message_length,
        COUNT(DISTINCT author_id) AS unique_authors
        FROM commits
        GROUP BY month_key, month_label
        ORDER BY month_key DESC
        """
    results = query_all(conn, monthly_summary_sql)
    conn.close()


if __name__ == "__main__":
    main()

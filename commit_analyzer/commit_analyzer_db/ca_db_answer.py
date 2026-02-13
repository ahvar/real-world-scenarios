from __future__ import annotations

import json
import os
import sqlite3
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

import requests


# ----------------------------
# Layer B: tiny harness + ingest
# ----------------------------


def fetch_commits(
    repo_owner: str, repo_name: str, per_page: int = 100
) -> List[Dict[str, Any]]:
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/commits?per_page={per_page}"

    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "codesignal-backend-practice-script",
    }

    # Optional: if you hit GitHub rate limits, set GITHUB_TOKEN in your env.
    token = os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    resp = requests.get(url, headers=headers, timeout=20)
    resp.raise_for_status()
    return resp.json()


def init_db(conn: sqlite3.Connection) -> None:
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS authors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            author_key TEXT NOT NULL UNIQUE
        );

        CREATE TABLE IF NOT EXISTS commits (
            sha TEXT PRIMARY KEY,
            author_id INTEGER NOT NULL,
            message TEXT NOT NULL,
            committed_at TEXT NOT NULL,     -- 'YYYY-MM-DD HH:MM:SS'
            month_key TEXT NOT NULL,        -- 'YYYY-MM' (sortable)
            month_label TEXT NOT NULL,      -- 'MM-YYYY' (display)
            FOREIGN KEY(author_id) REFERENCES authors(id)
        );

        CREATE INDEX IF NOT EXISTS idx_commits_author_id ON commits(author_id);
        CREATE INDEX IF NOT EXISTS idx_commits_month_key ON commits(month_key);
        CREATE INDEX IF NOT EXISTS idx_commits_committed_at ON commits(committed_at);
        """
    )


def parse_github_dt(date_str: str) -> Tuple[str, str, str]:
    """
    GitHub provides ISO 8601 like: '2025-06-10T12:34:56Z'
    Return:
      committed_at:  'YYYY-MM-DD HH:MM:SS'
      month_key:     'YYYY-MM'
      month_label:   'MM-YYYY'
    """
    dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
    committed_at = dt.strftime("%Y-%m-%d %H:%M:%S")
    month_key = dt.strftime("%Y-%m")
    month_label = dt.strftime("%m-%Y")
    return committed_at, month_key, month_label


def extract_author_key(item: Dict[str, Any]) -> str:
    """
    Prefer commit.author.email; fallback to commit.author.name; else 'unknown'.
    Note: GitHub top-level item["author"] may be null for unlinked emails.
    """
    commit_obj = item.get("commit", {}) or {}
    author_obj = commit_obj.get("author", {}) or {}
    email = author_obj.get("email")
    name = author_obj.get("name")
    return email or name or "unknown"


def extract_commit_fields(item: Dict[str, Any]) -> Optional[Tuple[str, str, str]]:
    """
    Return (sha, message, date_str) or None if unusable.
    """
    sha = item.get("sha")
    commit_obj = item.get("commit", {}) or {}
    message = commit_obj.get("message") or ""

    # Prefer author date; fallback to committer date
    author_obj = commit_obj.get("author", {}) or {}
    committer_obj = commit_obj.get("committer", {}) or {}
    date_str = author_obj.get("date") or committer_obj.get("date")

    if not sha or not date_str:
        return None
    return sha, message, date_str


def load_commits(conn: sqlite3.Connection, commits: List[Dict[str, Any]]) -> None:
    cur = conn.cursor()

    # Cache author_key -> author_id to reduce SELECTs
    author_id_cache: Dict[str, int] = {}

    for item in commits:
        fields = extract_commit_fields(item)
        if fields is None:
            continue

        sha, message, date_str = fields
        author_key = extract_author_key(item)
        committed_at, month_key, month_label = parse_github_dt(date_str)

        # Upsert author
        if author_key not in author_id_cache:
            cur.execute(
                "INSERT OR IGNORE INTO authors(author_key) VALUES (?)",
                (author_key,),
            )
            cur.execute(
                "SELECT id FROM authors WHERE author_key = ?",
                (author_key,),
            )
            row = cur.fetchone()
            if row is None:
                # Should not happen, but keep it safe.
                continue
            author_id_cache[author_key] = int(row[0])

        author_id = author_id_cache[author_key]

        # Upsert commit
        cur.execute(
            """
            INSERT OR REPLACE INTO commits(sha, author_id, message, committed_at, month_key, month_label)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (sha, author_id, message, committed_at, month_key, month_label),
        )

    conn.commit()


# ----------------------------
# Layer A: SQL queries (practice pack)
# ----------------------------


def query_all(conn: sqlite3.Connection, sql: str) -> List[Dict[str, Any]]:
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(sql)
    return [dict(r) for r in cur.fetchall()]


def main() -> None:
    repo_owner = "ahvar"
    repo_name = "data-structures-algorithms"

    commits = fetch_commits(repo_owner, repo_name, per_page=100)

    # Use ":memory:" for fast iteration, or "commits.db" to inspect later
    with sqlite3.connect(":memory:") as conn:
        init_db(conn)
        load_commits(conn, commits)

        # Q0: sanity check
        print("Rows:")
        print(
            query_all(
                conn,
                "SELECT (SELECT COUNT(*) FROM authors) AS authors, (SELECT COUNT(*) FROM commits) AS commits;",
            )
        )

        # Q1: Monthly summary (your original output, but in SQL)
        monthly_summary_sql = """
        SELECT
            month_label AS date,
            COUNT(*) AS commit_count,
            CAST(AVG(LENGTH(message)) AS INT) AS average_message_length,
            COUNT(DISTINCT author_id) AS unique_authors
        FROM commits
        GROUP BY month_key, month_label
        ORDER BY month_key DESC;
        """
        summary = query_all(conn, monthly_summary_sql)
        print(json.dumps(summary, indent=2))

        # Optional: if you still want to send to a webhook, keep this pattern:
        # webhook_url = "https://webhook.site/your-unique-url"
        # requests.post(webhook_url, json=summary, timeout=20).raise_for_status()


if __name__ == "__main__":
    main()

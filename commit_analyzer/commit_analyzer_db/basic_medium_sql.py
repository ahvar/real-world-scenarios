# 10 most recent commits with author and preview message
recent_commits_sql = """
    SELECT c.committed_at,
    a.author_key AS author,
    SUBSTR(c.message, 1, 80) AS message_preview,
    c.sha
    FROM commits c
    JOIN authors a
    ON a.id = c.author_id
    ORDER BY c.committed_at DESC
    LIMIT 10;
    """

# Commits per author (descending)
commits_per_author = """
    SELECT a.author_key AS author,
    COUNT(*) AS commit_count
    FROM commits c
    JOIN authors a ON a.id = c.author_id
    GROUP BY a.author_key
    ORDER BY commit_count DESC, author ASC;
"""

# first commit date + last commit date per author

first_and_last = """
    SELECT a.author_key as author,
    MIN(c.committed_at) AS first_commit,
    MAX(c.committed_at) AS last_commit,
    COUNT(*) AS total_commits
    FROM commits c
    JOIN authors a ON a.id = c.author_id
    GROUP BY a.author_key
    ORDER BY total_commits DESC, author ASC
"""

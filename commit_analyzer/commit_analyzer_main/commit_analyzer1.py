""" """

import requests
import json
import statistics
from datetime import datetime
from pathlib import Path

repo_owner = "ahvar"
repo_name = "data-structures-algorithms"
url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/commits?per_page=100"

response = requests.get(url).json()
# Path("commits_data.json").write_text(json.dumps(response, indent=4))
monthly_commits = {}
for obj in response:

    date, message, author = (
        obj["commit"]["author"]["date"],
        obj["commit"]["message"],
        obj["commit"]["author"]["name"],
    )
    dt = datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")
    month, year = dt.month, dt.year
    if f"{month}-{year}" not in monthly_commits:
        monthly_commits[f"{month:02d}-{year}"] = {
            "commit_count": 1,
            "messages": [len(message)],
            "authors": [author],
        }
    else:
        monthly_commits[f"{month}-{year}"]["commit_count"] += 1
        monthly_commits[f"{month}-{year}"]["message_lengths"].append(len(message))
        monthly_commits[f"{month}-{year}"]["authors"].append(author)
output = []
for month, data in monthly_commits.items():
    output.append(
        {
            "commit_count": data["commit_count"],
            "date": month,
            "average_message_length": statistics.mean(data["messages"]),
            "unique_authors": len(set(data["authors"])),
        }
    )

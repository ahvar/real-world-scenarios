from datetime import datetime
from collections import defaultdict
import requests
import statistics
import json

repo_owner = "ahvar"
repo_name = "data-structures-algorithms"

url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/commits?per_page=100"
commit_raw = requests.get(url).json()
monthly_commits = defaultdict(list)
for com_obj in commit_raw:
    date_str, message, author = (
        com_obj["commit"]["author"]["date"],
        com_obj["commit"]["message"],
        com_obj["commit"]["author"]["name"],
    )

    dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
    month_year = f"{dt.month}-{dt.year}"
    monthly_commits[month_year].append(
        {"date": date_str, "message": message, "author": author}
    )

output = []
for month, commits in monthly_commits:
    commit_count = len(commits)
    avg_msg_len = statistics.mean([len(c["message"]) for c in commits])
    unique_authors = [len(set(c["author"])) for c in commits]
    output.append(
        {
            "date": month,
            "commit_count": commit_count,
            "average_message_length": avg_msg_len,
            "unique_authors": unique_authors,
        }
    )

print(json.dumps(commit_raw, indent=4))

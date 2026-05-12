import requests
import json
from collections import defaultdict
from datetime import datetime
from commit_analyzer_app import app

repo_owner = "ahvar"
repo_name = "data-structures-algorithms"
url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/commits?per_page=100"


resp = requests.get(url)
print(resp.status_code)
resp_json = resp.json()
print(json.dumps(resp_json[0], indent=4))
monthly_commits = defaultdict(list)
for obj in resp_json:
    commit = obj["commit"]
    author = commit["author"].get("name") or commit["author"].get("email")
    date_str = commit["author"].get("date")
    date_dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
    month_year = datetime.strftime(date_dt, "%Y-%m")
    msg = commit["message"]
    monthly_commits[month_year].append(
        {"author": author, "message": msg, "date": date_str}
    )
output = []
for month, items in monthly_commits.items():

    avg_msg_len = sum(len(c["msg"]) for c in items) // len(items)
    unique_authors = set(len(c["author"]) for c in items)
    output.append(
        {
            "date": month,
            "commit_count": len(items),
            "average_message_length": avg_msg_len,
            "unique_authors": unique_authors,
        }
    )

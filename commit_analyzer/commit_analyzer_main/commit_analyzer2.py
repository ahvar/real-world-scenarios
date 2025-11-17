import requests
import json
import statistics
from datetime import datetime

repo_owner = "ahvar"
repo_name = "data-structures-algorithms"
url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/commits?per_page=100"

response = requests.get(url).json()
# print(json.dumps(response, indent=4))
monthly_commits = {}
for commit_obj in response:
    cdate, cauthor, cmsg = (
        commit_obj["commit"]["author"]["date"],
        commit_obj["commit"]["author"]["name"],
        commit_obj["commit"]["message"],
    )

    dt = datetime.strptime(cdate, "%Y-%m-%dT%H:%M:%SZ")
    month, year = dt.month, dt.year
    month_key = f"{month:02d}-{year}"
    if month_key not in monthly_commits:

        monthly_commits[month_key] = [
            {"date": cdate, "author": cauthor, "msg_len": len(cmsg)}
        ]
    else:
        monthly_commits[month_key].append(
            {"date": cdate, "author": cauthor, "msg_len": len(cmsg)}
        )
result = []
for month_year, cdata in monthly_commits.items():
    total = len(cdata)
    msg_lens = [obj["msg_len"] for obj in cdata]
    avg_msg_len = statistics.mean(msg_lens)
    unique_author = len(set([obj["author"] for obj in cdata]))
    result.append(
        {
            "commit_count": total,
            "average_message_length": avg_msg_len,
            "unique_author": unique_author,
            "date": month_year,
        }
    )


print(json.dumps(result, indent=4))

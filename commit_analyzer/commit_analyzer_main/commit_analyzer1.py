""" """

import requests
import statistics
import json
from datetime import datetime
from pprint import PrettyPrinter

pp = PrettyPrinter(indent=4)

repo_owner = "ahvar"
repo_name = "gene_annotator"
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
        monthly_commits[month_year]["authors"].append(each["commit"]["author"]["name"])
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
month_summary.sort(key=lambda x: datetime.strptime(x["date"], "%m-%Y"), reverse=True)
response = requests.post(
    "https://webhook.site/4823ab23-3b35-4d63-ac29-27a6996c7f1f", json=month_summary
)
response.raise_for_status()
print(f"Data sent successfully: {response.status_code}")

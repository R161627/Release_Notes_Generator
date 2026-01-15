import requests
import re
import json
import os
from urllib.parse import urlencode
from dotenv import load_dotenv
from Data.jira_client import fetch_jira_details

load_dotenv()

GITLAB_BASE_URL = f"{os.getenv('GITLAB_URL')}/api/v4"
PROJECT_ID = os.getenv("GITLAB_PROJECT_ID")
PRIVATE_TOKEN = os.getenv("GITLAB_TOKEN")
HEADERS = {
    "PRIVATE-TOKEN": PRIVATE_TOKEN
}
JIRA_REGEX = r"[A-Z]+-\d+"
def extract_jira_id(text: str):
    if not text:
        return None
    match = re.search(JIRA_REGEX, text)
    return match.group(0) if match else None

def fetch_merge_requests(start_date: str, end_date: str, include_diff=False):
    """
    Collects merge requests merged in a given date range.
    start_date, end_date in format: YYYY-MM-DD
    """

    page = 1
    per_page = 50
    results = []

    query = {
        "state": "merged",
        "updated_after": start_date,
        "updated_before": end_date,
        "per_page": per_page,
    }

    while True:
        url = f"{GITLAB_BASE_URL}/projects/{PROJECT_ID}/merge_requests?{urlencode(query)}&page={page}"
        print(f"Fetching page {page}: {url}")
        res = requests.get(url, headers=HEADERS,verify='./Current-IT-Root-CAs.pem')

        if res.status_code != 200:
            raise RuntimeError(f"GitLab API error {res.status_code}: {res.text}")

        mrs = res.json()
        if not mrs:
            break
        for mr in mrs:
            mr_data = {
                "iid": mr["iid"],
                "title": mr["title"],
                "description": mr.get("description", ""),
                "merged_at": mr["merged_at"],
                "web_url": mr["web_url"],
                "jira_id": extract_jira_id(mr["title"] + " " + mr.get("description", "")),
            }
            # Optional: Fetch changes (diff)
            if include_diff:
                diff_url = f"{GITLAB_BASE_URL}/projects/{PROJECT_ID}/merge_requests/{mr['iid']}/changes"
                diff_res = requests.get(diff_url, headers=HEADERS,verify='./Current-IT-Root-CAs.pem')
                if diff_res.status_code == 200:
                    changes = diff_res.json().get("changes", [])
                    files_changed = [c["new_path"] for c in changes]
                    mr_data["files_changed"] = files_changed
                    mr_data["diff_stats"] = {
                        "files": len(files_changed),
                        "additions": sum(c["additions"] for c in changes if "additions" in c),
                        "deletions": sum(c["deletions"] for c in changes if "deletions" in c),
                    }
            if mr_data["jira_id"]:
                mr_data["jira_details"]=fetch_jira_details(mr_data["jira_id"])
            results.append(mr_data)
        page += 1
    return results

def save_to_file(data, filename="gitlab_prs.json"):
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Saved {len(data)} PRs to {filename}")
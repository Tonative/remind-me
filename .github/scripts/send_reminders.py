import os
import re
import requests
from datetime import datetime

# GitHub API base and repo info
GITHUB_API = "https://api.github.com"
REPO = os.environ["GITHUB_REPO"]
HEADERS = {
    "Authorization": f"Bearer {os.environ['GH_TOKEN']}",
    "Accept": "application/vnd.github.v3+json"
}

# Function to fetch issues
def get_issues():
    url = f"{GITHUB_API}/repos/{REPO}/issues"
    res = requests.get(url, headers=HEADERS)
    res.raise_for_status()
    return res.json()

# Function to extract Start/End dates from issue body
def extract_dates(body):
    start = re.search(r"Start Date:\s*(\d{4}-\d{2}-\d{2})", body)
    end = re.search(r"End Date:\s*(\d{4}-\d{2}-\d{2})", body)
    return (
        datetime.strptime(start.group(1), "%Y-%m-%d").date() if start else None,
        datetime.strptime(end.group(1), "%Y-%m-%d").date() if end else None,
    )

# Function to post a comment to an issue
def post_comment(issue_number, message):
    url = f"{GITHUB_API}/repos/{REPO}/issues/{issue_number}/comments"
    res = requests.post(url, headers=HEADERS, json={"body": message})
    res.raise_for_status()
    print(f"Posted comment on issue #{issue_number}")

# Main function: send test comments to all issues
def send_reminders():
    issues = get_issues()

    for issue in issues:
        # Skip pull requests
        if "pull_request" in issue:
            continue

        number = issue["number"]
        body = issue.get("body", "")
        assignee = issue.get("assignee", {}).get("login", "team")

        start, end = extract_dates(body)

        # Build and send the test comment
        comment = f"Test: @{assignee}, this issue #{number} starts on **{start}** and ends on **{end}**."
        post_comment(number, comment)

if __name__ == "__main__":
    send_reminders()

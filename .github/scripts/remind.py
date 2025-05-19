#!/usr/bin/env python3
import os
import re
from datetime import datetime, timedelta
from dateutil import parser
import pytz
from github import Github

def main():
    token = os.getenv('GITHUB_TOKEN')
    if not token:
        raise RuntimeError("GITHUB_TOKEN is not set")

    # Authenticate with GitHub token
    gh = Github(token)
    repo = gh.get_repo(f"{os.getenv('GITHUB_REPOSITORY')}")

    # Time setup
    tz = pytz.timezone(os.getenv('TZ', 'UTC'))
    now = datetime.now(tz).replace(hour=0, minute=0, second=0, microsecond=0)

    # Fetch open issues
    issues = repo.get_issues(state='open')
    for issue in issues:
        body = issue.body or ""
        
        # Extract YYYY-MM-DD after "Start Date:" / "End Date:"
        start_match = re.search(r"Start\s*Date:\s*(\d{4}-\d{2}-\d{2})", body, re.IGNORECASE)
        end_match   = re.search(r"End\s*Date:\s*(\d{4}-\d{2}-\d{2})",   body, re.IGNORECASE)
        if not (start_match and end_match):
            print(f"Issue #{issue.number}: no dates found, skipping")
            continue

        start = tz.localize(parser.isoparse(start_match.group(1)))
        end   = tz.localize(parser.isoparse(end_match.group(1)))

        delta_start = (start - now).days
        delta_end   = (end - now).days

        comment = None
        if delta_start == 1:
            comment = f"⏰ Reminder: this project starts tomorrow ({start.date()})."
        elif delta_start == 0:
            comment = f"🚀 Today is the start date ({start.date()})—let’s get going!"
        elif delta_end == 1:
            comment = f"⚠️ Heads-up: project ends tomorrow ({end.date()})."
        elif delta_end == 0:
            comment = f"🏁 Today is the end date ({end.date()}). Please wrap up any remaining tasks."

        if comment:
            print(f"Posting to issue #{issue.number}: {comment}")
            issue.create_comment(comment)
        else:
            print(f"Issue #{issue.number}: no reminders due today.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
        exit(1)

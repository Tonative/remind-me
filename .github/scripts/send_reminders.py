import os
import requests
from datetime import datetime, timedelta

GITHUB_API = "https://api.github.com/graphql"
REPO = os.environ["GITHUB_REPO"]  
ORG = os.environ["GITHUB_ORG"]    
PROJECT_NUMBER = int(os.environ["GITHUB_PROJECT_NUMBER"]) 
TOKEN = os.environ["GITHUB_TOKEN"]

HEADERS = {
    "Authorization": f"Bearer {TOKEN}"
}

def run_graphql(query, variables):
    res = requests.post(GITHUB_API, json={"query": query, "variables": variables}, headers=HEADERS)
    res.raise_for_status()
    resp_json = res.json()
    if "errors" in resp_json:
        raise Exception(f"GraphQL errors: {resp_json['errors']}")
    return resp_json["data"]

def get_open_issues():
    query = """
    query($owner: String!, $repo: String!, $after: String) {
  repository(owner: $owner, name: $repo) {
    issues(first: 100, after: $after, states: OPEN) {
      nodes {
        number
        assignees(first: 1) {
          nodes {
            login
          }
        }
        projectItems(first: 10) {
          nodes {
            id
          }
        }
      }
      pageInfo {
        endCursor
        hasNextPage
      }
    }
  }
}
"""
    owner, repo = REPO.split("/")
    issues = []
    after = None
    while True:
        data = run_graphql(query, {"owner": owner, "repo": repo, "after": after})
        issues_batch = data["repository"]["issues"]["nodes"]
        issues.extend(issues_batch)
        page_info = data["repository"]["issues"]["pageInfo"]
        if not page_info["hasNextPage"]:
            break
        after = page_info["endCursor"]
    return issues


def get_project_item_dates(project_item_id):
    query = """
    query($id: ID!) {
      node(id: $id) {
        ... on ProjectV2Item {
          fieldValues(first: 20) {
            nodes {
              ... on ProjectV2ItemFieldDateValue {
                date
                field {
                  ... on ProjectV2FieldCommon {
                    name
                  }
                }
              }
            }
          }
        }
      }
    }
    """

    data = run_graphql(query, {"id": project_item_id})
    field_values = data["node"]["fieldValues"]["nodes"]

    start_date = None
    end_date = None

    for fv in field_values:
        # Safely access field name
        field = fv.get("field")
        if not field:
            continue  # Skip if field is missing

        field_name = field.get("name", "").lower()
        if "start" in field_name:
            start_date = fv.get("date")
        elif "end" in field_name:
            end_date = fv.get("date")

    return start_date, end_date


def post_comment(issue_number, message):
    print(f"running post comment method for issue: #{issue_number}")
    url = f"https://api.github.com/repos/{REPO}/issues/{issue_number}/comments"
    res = requests.post(url, headers={
        "Authorization": f"Bearer {TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }, json={"body": message})
    res.raise_for_status()
    print(f"Posted comment on issue #{issue_number}")

def send_reminders():
    from datetime import datetime, timezone

    today = datetime.now(timezone.utc).date()

    issues = get_open_issues()

    for issue in issues:
        issue_number = issue["number"]
        assignees = issue.get("assignees", {}).get("nodes", [])
        assignee_mention = ""
        if assignees:
            # Mention the first assignee (you can modify if multiple)
            assignee_mention = f"@{assignees[0]['login']} "
    project_items = issue["projectItems"]["nodes"]

    for item in project_items:
        project_item_id = item.get("id")
        if not project_item_id:
            print("Warning: Skipping item with missing ID")
            continue

        try:
            start_str, end_str = get_project_item_dates(project_item_id)
        except Exception as e:
            print(f"Failed to fetch dates for item {project_item_id}: {e}")
            continue

        start_date = datetime.fromisoformat(start_str).date() if start_str else None
        end_date = datetime.fromisoformat(end_str).date() if end_str else None

        remind = False
        comment_parts = []
        if start_date:
            print(f"Start date for issue #{issue_number}: {start_date}")
            print(f"Today: {today}")
            if today == start_date - timedelta(days=2):
                remind = True
                comment_parts.append(f"Project starts in 2 days on **{start_date}**.")
            elif today == start_date - timedelta(days=1):
                remind = True
                comment_parts.append(f"Project starts tomorrow (**{start_date}**).")
        if end_date:
            print(f"End date for issue #{issue_number}: {end_date}")
            if today == end_date - timedelta(days=1):
                remind = True
                comment_parts.append(f"Project ends tomorrow (**{end_date}**).")
            elif today == end_date:
                remind = True
                comment_parts.append(f"Project ends today (**{end_date}**).")

        if remind:
            comment = f"{assignee_mention} ⏰ Reminder for issue #{issue_number}:\n" + "\n".join(comment_parts)
            post_comment(issue_number, comment)


if __name__ == "__main__":
    send_reminders()

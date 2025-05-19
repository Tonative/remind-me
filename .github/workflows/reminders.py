import requests
import os
import datetime
import re


#repo info
GITHUB_API = "https://api.github.com"
GITHUB_REPO = os.environ["GITHUB_REPOSITORY"]
TOKEN = os.environ["GITHUB_TOKEN"]
HEADERS = {"Authorization": f"token {TOKEN}"}

#fetch issues from github
def get_issues():
    url = f"{GITHUB_API}/repos/{GITHUB_REPO}/issues"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()

#extract start and end dates
def extract_dates(body):
    date_pattern =  r"(start|end)\s*date\s*:\s*(\d{4}-\d{2}-\d{2})"
    dates = dict(re.findall(date_pattern, body, re.IGNORECASE))
    return dates.get("start"), dates.get("end")

#Post comment to the github issue
def post_comment(issue_number, message):
    url = f"https://api.github.com/repos/{GITHUB_REPO}/issues/{issue_number}/comments"
    response = requests.post(url, headers=HEADERS, json={"body": message})
    response.raise_for_status()
    
#main logic    
def main():
    today = datetime.date.today().isoformat()
    issues = get_issues()
    
    for issue in issues:
        number = issue["number"]
        body = issue.get("body", "")
        start, end = extract_dates(body)
        
        if not start or not end:
            continue #skip if date info is missing
        
        if today == start:
            post_comment(number, f"Today is the **start date** of this task")
        elif today == end:
            post_comment(number, f"Today is the **end date** of this task. Make sure it is completed")
            
            
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
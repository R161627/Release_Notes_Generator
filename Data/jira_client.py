from jira import JIRA
from dotenv import load_dotenv
import os

load_dotenv()
jira_server=os.getenv("JIRA_SERVER")
jira_token=os.getenv("JIRA_TOKEN")

def fetch_jira_details(jira_id):
    jira_obj = JIRA(server=jira_server, token_auth=jira_token)
    issues = jira_obj.issue(jira_id,fields="*all")
    jira_details = {
        "key": issues.key,
        "summary": issues.fields.summary,
        "description": issues.fields.description,
        "issue_type": issues.fields.issuetype.name,
        "status": issues.fields.status.name,
        "comments": [
            {
                "body": c.body,
            }
            for c in issues.fields.comment.comments
        ],
        "latest_sprint": None,
    }
    return jira_details
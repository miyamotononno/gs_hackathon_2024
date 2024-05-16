from . import settings
from fastapi import FastAPI, Request
import requests
from requests.auth import HTTPBasicAuth
import json
from github import Github


app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "YOUNG TOKYO"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):

    return {"item_id": item_id, "q": q}

@app.post("/info/")
async def create_info(info: Request):
    jsondata = await info.json()
    owner = jsondata["owner"]
    repo = jsondata["repo"]
    pr_id = int(jsondata["pr"])
    issue_key = jsondata["jira"]
    response = {}
    response["jira"] = get_jira(issue_key)
    response["pr"] = get_pr(owner, repo, pr_id)
    return response

def get_jira(issue_key: str):
    url = "https://teki0928.atlassian.net/rest/api/2/issue/" + issue_key
    auth = HTTPBasicAuth(settings.JIRA_USER_NAME, settings.JIRA_API_KEY)
    headers = {
        "Accept": "application/json"
    }

    response = requests.request(
        "GET",
        url,
        headers=headers,
        auth=auth
    )
    result = {}
    res = json.loads(response.text)
    result["name"] = res["fields"]["summary"]
    result["description"] = res["fields"]["description"]
    result["labels"] = res["fields"]["labels"]
    result["proj_name"] = res["fields"]["project"]["name"]
    result["comments"] = res["fields"]["comment"]["comments"]
    return result

def get_pr(owner: str, repo: str, pr_id: int):
    g = Github()
    repo = g.get_repo(f"{owner}/{repo}")
    pr = repo.get_pull(pr_id)
    result = {}
    result["title"] = pr.title
    result["number"] = pr.number
    result["changes"] = []
    print(f"Checking Pull Request #{pr.number} - {pr.title}")
    files = pr.get_files()
    for file in files:
        file_attr = {}
        file_attr["file_name"] = file.filename
        patch_content = file.patch
        patch_lines = patch_content.split('\n')
        added_lines = [line[1:].replace('"','').replace("'","").strip() for line in patch_lines if len(line[1:].replace('"','').replace("'","")) > 0 and line.startswith('+') and not line.startswith('+++')]
        deleted_lines = [line[1:].replace('"','').replace("'","").strip() for line in patch_lines if len(line[1:].replace('"','').replace("'","")) > 0 and line.startswith('-')]
        file_attr["added_line_num"] = len(added_lines)
        file_attr["deleted_line_num"] = len(deleted_lines)
        file_attr["added_lines"] = added_lines
        file_attr["deleted_lines"] = deleted_lines
        result["changes"].append(file_attr)
    return result




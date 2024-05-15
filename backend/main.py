from fastapi import FastAPI
import uvicorn
import requests
from requests.auth import HTTPBasicAuth
import json
from github import Github
import settings
import service


app = FastAPI()

@app.get("/")
def read_root():
    return {"message": service.result.content}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):

    return {"item_id": item_id, "q": q}

@app.get("/jira/{issue_key}")
def get_jira(issue_key: str):
    url = "https://teki0928.atlassian.net/rest/api/2/issue/" + issue_key
    # use comment one for local debugging
    auth = HTTPBasicAuth(settings.JIRA_USER_NAME, settings.JIRA_API_KEY)
    # auth = HTTPBasicAuth("w2495969292@gmail.com", "jira_api_key")
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

@app.get("/github/{repo_owner}/{repo_name}/{pr_id}")
def get_code_changes(repo_owner:str, repo_name:str, pr_id: int):
    g = Github()
    repo = g.get_repo(f"{repo_owner}/{repo_name}")
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
        added_lines = [line[2:] for line in patch_lines if line.startswith('+ ') and not line.startswith('+++')]
        deleted_lines = [line[2:] for line in patch_lines if line.startswith('- ')]
        file_attr["added_line_num"] = len(added_lines)
        file_attr["deleted_line_num"] = len(deleted_lines)
        file_attr["added_lines"] = added_lines
        file_attr["deleted_lines"] = deleted_lines
        result["changes"].append(file_attr)
    return result



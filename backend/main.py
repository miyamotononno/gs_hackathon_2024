import settings
from fastapi import FastAPI, Request
import requests
from requests.auth import HTTPBasicAuth
import json
from github import Github
from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    HarmBlockThreshold,
    HarmCategory,
)
from langchain.prompts.chat import ChatPromptTemplate


app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "YOUNG TOKYO"}

@app.post("/info/")
async def create_info(info: Request):
    jsondata = await info.json()
    owner = jsondata["owner"]
    repo = jsondata["repo"]
    pr_id = int(jsondata["pr"])
    issue_key = jsondata["jira"]
    jira = get_jira(issue_key)
    pr = get_pr(owner, repo, pr_id)
    response = get_llm_response(jira, pr).content
    print(f"jira info: {jira}")
    print(f"pr info: {pr}")
    print(f"llm: {response}")
    return response

def get_jira(issue_key: str):
    url = "https://teki0928.atlassian.net/rest/api/2/issue/" + issue_key
    auth = HTTPBasicAuth(settings.JIRA_USER_NAME, settings.JIRA_API_KEY)
    headers = {
        "Accept": "application/json"
    }
    print(f"Checking Jira issue #{issue_key}...")
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
    print(f"Checking Pull Request #{pr.number} - {pr.title}...")
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

def get_llm_response(jira, pr):
    llm = ChatGoogleGenerativeAI(model="gemini-pro",
                                safety_settings={
                                                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                                                 },
                                google_api_key=settings.GOOGLE_API_KEY 
            )
    print(f"Getting summary from Gemini...")
    result = llm.invoke(f"You are a software engineer. You are working on a project along with {jira}. You made pull request in project GitHub repository like {pr}. Please explain in brief and concise language what change you made, why and how you did that and testing, if done, alongside updates to your code. Use the format ## What, ## Why, ## How, ## Testing. Don't add anything that you are not sure of and don't make up false information.")
    return result
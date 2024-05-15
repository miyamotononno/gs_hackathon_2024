# GS EngCon Hackathon 2024 for YOUNG TOKYO

## Prerequisite
- copy `.env.sample` to `.env` (need to share the secret key/pass privately)

## How to install libraries
```
pip install -r requirements.txt
```

## How to run the server
```
cd ./backend/
uvicorn main:app --reload
```
Then go to `http://127.0.0.1:8000/`

`http://127.0.0.1:8000/docs` shows API doc as swagger-ui.

Please see [FastAPI doc](https://fastapi.tiangolo.com/ja/).

## How to run the UI
**The above server needs to be up on the background.**

```
cd ./fronend/
streamlit run main.py
```
Then go to `http://localhost:8501/`

Please see [Streamlit doc](https://docs.streamlit.io/).

## How to deploy to GCP
TBD
useful link to deploy: [here](https://laid-back-scientist.com/cloud-run-python)

# API Docs
### get Jira ticket by id
```
http://localhost:8000/jira/{jira_ticket_id}
```
response:
```
{
  "name": "issue title",
  "description": "This is the great description of issue 0001.",
  "labels": [
    "feat"
  ],
  "proj_name": "GS_Hackson",
  "comments": []
}
```

### get Github PR info
```
http://localhost:8000/github/{repo_owner}/{repo_name}/{pull_request_id}

example:
http://localhost:8000/github/tensorflow/tensorflow/67560
```
response:
```
{
  "title": "PR #12433: [GPU] Make cuDNN fusion test run on H100.",
  "number": 67560,
  "changes": [
    {
      "file_name": "third_party/xla/xla/service/gpu/fusions/BUILD",
      "added_line_num": 1,
      "deleted_line_num": 1,
      "added_lines": [
        "       \"requires-gpu-sm90\","
      ],
      "deleted_lines": [
        "       \"requires-gpu-sm80\","
      ]
    }
  ]
}
```
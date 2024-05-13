# GS EngCon Hackathon 2024 for YOUNG TOKYO

## Prerequisite
- copy `.env.sample` to `.env` (need to share the secret key/pass privately)

## How to install libraries
```
pip install -r requirements.txt
```

## How to run the server
```
uvicorn main:app --reload
```
Then go to `http://127.0.0.1:8000/`

`http://127.0.0.1:8000/docs` shows API doc as swagger-ui.

Please see [FastAPI doc](https://fastapi.tiangolo.com/ja/).

## How to run the UI
**The above server needs to be up on the background.**

```
streamlit run ui.py
```
Then go to `http://localhost:8501/`

Please see [Streamlit doc](https://docs.streamlit.io/).

## How to deploy to GCP
TBD
useful link to deploy: [here](https://laid-back-scientist.com/cloud-run-python)

# coding: UTF-8
import os
from dotenv import load_dotenv

load_dotenv(verbose=True)

JIRA_USER_NAME = os.getenv("JIRA_USER_NAME")
JIRA_API_KEY = os.getenv("JIRA_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GITHUB_ACCESS_TOKEN = os.getenv("GITHUB_ACCESS_TOKEN")

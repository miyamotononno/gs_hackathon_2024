# coding: UTF-8
import os
from dotenv import load_dotenv

load_dotenv(verbose=True)

URL = os.getenv("BACKEND_URL")

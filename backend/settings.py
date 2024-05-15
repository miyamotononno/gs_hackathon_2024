# coding: UTF-8
import os
from dotenv import load_dotenv

load_dotenv(verbose=True)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

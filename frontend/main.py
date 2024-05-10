# coding: UTF-8
import settings
import requests
import streamlit as st

st.set_page_config(layout="wide")

def main():
    response = requests.get(settings.URL)
    jsondata = response.json()
    msg = jsondata['message']
    st.title(msg)

if __name__ == '__main__':
    main()

import streamlit as st
import requests

st.set_page_config(layout="wide")
URL = 'http://localhost:8000'

def main():
    response = requests.get(URL)
    jsondata = response.json()
    msg = jsondata['message']
    st.title(msg)

if __name__ == '__main__':
    main()
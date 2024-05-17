# coding: UTF-8
import settings
import requests
import streamlit as st
import json

st.set_page_config(layout="wide")

def main():
    response = requests.get(settings.URL)
    jsondata = response.json()
    msg = jsondata['message']
    st.title(msg)
    with st.form("inputs form", clear_on_submit=False):
        pr_link = st.text_input("Pull Request URL")
        jira_link = st.text_input("JIRA Issue ticket")
        submitted = st.form_submit_button("Submit")
        if submitted:
            pr_link_split = pr_link.split("/")
            jira_link_split = jira_link.split("/")
            
            if pr_link.startswith("https"):
                owner, repo, pr_number = pr_link_split[3], pr_link_split[4], pr_link_split[-1]
            else:
                owner, repo, pr_number = pr_link_split[1], pr_link_split[2], pr_link_split[-1]
            
            jira_number = jira_link_split[-1]

            post_url = f"{settings.URL}/info/"

            post_data = json.dumps({"owner": owner, "repo": repo, "pr": pr_number, "jira": jira_number})

            post_response = requests.post(post_url, data=post_data)

            st.write(post_response.json())


if __name__ == '__main__':
    main()

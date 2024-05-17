from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    HarmBlockThreshold,
    HarmCategory,
)
from langchain.prompts.chat import ChatPromptTemplate

JIRA_ticket = {
  "name": "issue title",
  "description": "Terminal: inline chat widget is not consistently hidden",
  "labels": [
    "feat"
  ],
  "proj_name": "vscode",
  "comments": []
}

PR_ = {
  "title": "PR #12433: on blur of terminal chat widget, if terminal is not visible, hide it",
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

# prompt_template = ChatPromptTemplate.from_messages(
#     [
#         (
#             "system",
#             "You are a software engineer. You are working on a project along with {JIRA}. You made pull request in project GitHub repository like {PR}",
#         ),
#         ("human", "Please explain what change you made, why and how you did that and testing alongside updates to your code."),
#     ]
# ).format_messages(JIRA=str(JIRA_ticket),PR=str(PR_))

llm = ChatGoogleGenerativeAI(model="gemini-pro",
safety_settings={
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    },
   google_api_key='AIzaSyD_f0uRQtaJGNsXTAQlMPMov3I8yXQ2HE0' 
)
result = llm.invoke(f"You are a software engineer. You are working on a project along with {JIRA_ticket}. You made pull request in project GitHub repository like {PR_}. Please explain what change you made, why and how you did that and testing alongside updates to your code.")
print(result)



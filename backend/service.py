from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    HarmBlockThreshold,
    HarmCategory,
)
from langchain.prompts.chat import ChatPromptTemplate

JIRA_ticket = {
  "name": "issue title",
  "description": "This is the great description of issue 0001.",
  "labels": [
    "feat"
  ],
  "proj_name": "GS_Hackson",
  "comments": []
}

PR = {
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

prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a software engineer. You are working on a project along with {JIRA_ticket}. "
            +"You made pull request in project GitHub repository like {PR}",
        ),
        ("human", "Please explain what change you made, why and how you did that and testing alongside updates to your code."),
    ]
).format_messages(JIRA_ticket=JIRA_ticket,PR=PR)
# prompt_template.format(JIRA_ticket=JIRA_ticket,PR=PR)

llm = ChatGoogleGenerativeAI(model="gemini-pro",
safety_settings={
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    },
)
result = llm.invoke(prompt_template)



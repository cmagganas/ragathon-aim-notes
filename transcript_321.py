# pip install -U langchain langchainhub
# export LANGCHAIN_HUB_API_KEY="ls_..."
# LANGCHAIN_HUB_API_KEY_RAGATHON="ls_..."

# from google.colab import userdata
from langchain import hub
from langchain_openai import ChatOpenAI
import openai
import os
from dotenv import load_dotenv
load_dotenv()

# openai.api_key = userdata.get('OPENAI_API_KEY')
# os.environ["OPENAI_API_KEY"] = userdata.get('OPENAI_API_KEY')
openai.api_key = os.environ['OPENAI_API_KEY']

model = ChatOpenAI()

# pull a chat prompt
# prompt = hub.pull("aim-notes/sum-n-act-eval")
summary_prompt = hub.pull("aim-notes/summary")
todo_prompt = hub.pull("aim-notes/todo")
tasks_prompt = hub.pull("aim-notes/tasks")
report_prompt = hub.pull("aim-notes/meeting-report")


# load transcript from a file
with open("samples/transcript-with-diarization-sample.txt", "r", encoding="utf-8") as file:
    transcript = file.read()

# use it in a runnable
summary_runnable = summary_prompt | model
todo_runnable = todo_prompt | model
tasks_runnable = tasks_prompt | model
report_runnable = report_prompt | model
summary_response = summary_runnable.invoke({"transcript_text": transcript})
todo_response = todo_runnable.invoke({"transcript_text": transcript})
tasks_response = tasks_runnable.invoke({"transcript_text": transcript})
report_response = report_runnable.invoke({
    "summary": summary_response.content,
    "todo": todo_response.content,
    "tasks": tasks_response.content
    })

print(report_response.content)

# https://docs.smith.langchain.com/hub/dev-setup
# from langchain import hub
# from langchain.prompts.chat import ChatPromptTemplate

# prompt = ChatPromptTemplate.from_template("tell me a joke about {topic}")

# hub.push("<handle>/topic-joke-generator", prompt)
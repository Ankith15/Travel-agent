import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.tools import tool
from langchain_cohere import ChatCohere
from langchain_community.tools import DuckDuckGoSearchRun
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time
from utils.tools import scrape_train,check_train_station
from utils.tools_caller import invoke_tools

# Load environment variables
load_dotenv()


# Initialize tools and LLM
search = DuckDuckGoSearchRun()
llm = ChatCohere()







# Bind tools to LLM


# Initial Message
def train_agent(text:str)->str:
    llm_with_tools = llm.bind_tools([check_train_station, scrape_train])

    messages = [HumanMessage(content=text)]

    res = llm_with_tools.invoke(messages)


    # Invoke LLM
    while res.tool_calls:
        messages.append(res)
        messages = invoke_tools(res.tool_calls, messages)
        try:
            res = llm_with_tools.invoke(messages)
        except Exception as e:
            print("An error occurred during LLM invocation:", str(e))

    return res.content
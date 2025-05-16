from dotenv import load_dotenv
import os
import uuid

# Load environment variables from .env file
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent

class Agent:
    def __init__(self):
        self.memory = MemorySaver()
        self.model = ChatOpenAI(model_name=os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview"))
        self.search = TavilySearchResults(max_results=2)
        self.tools = [self.search]
        self.agent_executor = create_react_agent(self.model, self.tools, checkpointer=self.memory)
        self.thread_id = str(uuid.uuid4())
        self.config = {"configurable": {"thread_id": self.thread_id}}

    def process_message(self, message: str):
        response = None
        for step in self.agent_executor.stream(
            {"messages": [HumanMessage(content=message)]},
            self.config,
            stream_mode="values",
        ):
            response = step["messages"][-1]
        return response
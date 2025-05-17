from dotenv import load_dotenv
import os
import uuid

load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent

class WebSearchAgent:
    def __init__(self):
        self.conversation_memory = MemorySaver()
        self.language_model = ChatOpenAI(model_name=os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview"))
        self.web_search_tool = TavilySearchResults(max_results=3)
        self.available_tools = [self.web_search_tool]
        
        system_prompt = """You are a helpful web search assistant. 
        Your primary function is to search the web and provide accurate, up-to-date information.
        When searching:
        1. Use specific search terms to get relevant results
        2. Consider multiple sources for comprehensive information
        3. Cite your sources when providing information
        4. If you're unsure about something, say so and search for clarification
        Always maintain a helpful and informative tone."""
        
        self.agent_executor = create_react_agent(
            self.language_model, 
            self.available_tools, 
            checkpointer=self.conversation_memory,
            prompt=SystemMessage(content=system_prompt),
        )
        self.conversation_id = str(uuid.uuid4())
        self.execution_config = {"configurable": {"thread_id": self.conversation_id}}

    def process_message(self, user_message: str):
        search_response = None
        for step in self.agent_executor.stream(
            {"messages": [HumanMessage(content=user_message)]},
            self.execution_config,
            stream_mode="values",
        ):
            search_response = step["messages"][-1]
        return search_response
from dotenv import load_dotenv
import os

load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent

memory = MemorySaver()
model = ChatOpenAI(model_name="gpt-4-turbo-preview")
search = TavilySearchResults(max_results=2)
tools = [search]
agent_executor = create_react_agent(model, tools, checkpointer=memory)

config = {"configurable": {"thread_id": "abc123"}}

print("Chat initialized! Type 'quit' to exit.")
while True:
    user_input = input("\nYou: ").strip()
    if user_input.lower() == 'quit':
        break
        
    for step in agent_executor.stream(
        {"messages": [HumanMessage(content=user_input)]},
        config,
        stream_mode="values",
    ):
        print("\nAssistant:", end=" ")
        step["messages"][-1].pretty_print()
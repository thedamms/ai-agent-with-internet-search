from agent import WebSearchAgent

def run_web_search_cli():
    web_search_agent = WebSearchAgent()
    print("Web Search Agent initialized! Type 'quit' to exit.")
    print("Ask me anything, and I'll search the web for accurate information.")
    
    while True:
        user_query = input("\nYou: ").strip()
        if user_query.lower() == 'quit':
            break
            
        search_result = web_search_agent.process_message(user_query)
        print("\nAssistant:", end=" ")
        search_result.pretty_print()

if __name__ == "__main__":
    run_web_search_cli() 
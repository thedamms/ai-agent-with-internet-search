from agent import Agent

def main():
    """Run the agent in command-line interface mode"""
    agent = Agent()
    print("Chat initialized! Type 'quit' to exit.")
    
    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() == 'quit':
            break
            
        response = agent.process_message(user_input)
        print("\nAssistant:", end=" ")
        response.pretty_print()

if __name__ == "__main__":
    main() 
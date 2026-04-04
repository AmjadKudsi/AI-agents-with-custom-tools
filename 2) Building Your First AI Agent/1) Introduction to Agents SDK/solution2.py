# Add the new input and ensure that the agent can process it correctly.

from agents import Agent, Runner

def main():
    # Create an agent with instructions
    agent = Agent(
        name="Science Guide",
        instructions=(
            "You are a knowledgeable science guide. "
            "Explain scientific concepts in a simple and engaging way. "
            "Encourage curiosity and exploration."
        )
    )

    # Example input for the agent
    user_input = "What is photosynthesis?"

    # Run the agent synchronously
    result = Runner.run_sync(agent, user_input)
    print(result.final_output)

    # TODO: Add a new input example and run the agent with it
    new_input = "How does photosynthesis compare with how humans get and use energy?"    
    
    result = Runner.run_sync(agent, new_input)
    print(result.final_output)    

if __name__ == "__main__":
    main()
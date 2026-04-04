# change the agent's role to a "Science Guide" who explains scientific concepts simply and engagingly

from agents import Agent, Runner

def main():
    # Create an agent with instructions
    agent = Agent(
        name="Science Guide",
        instructions=(
            "You are a helpful knowledgeable guide designed to help students understand complex topics in scientific field. "
            "Provide clear, educational responses that break down concepts step by step. "
            "Make your explanations interesting by using innovative and engaging examples."
        )
    )

    # Example input for the agent
    user_input = "Explain how neural networks learn."

    # Run the agent synchronously
    result = Runner.run_sync(agent, user_input)
    print(result.final_output)

if __name__ == "__main__":
    main()
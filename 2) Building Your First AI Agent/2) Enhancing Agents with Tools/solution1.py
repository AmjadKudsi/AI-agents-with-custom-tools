# Update the agent's instructions and user input to search for the latest news about a specific celebrity, such as "Beyoncé"

from agents import Agent, Runner, WebSearchTool


def main():
    # Create an agent with instructions
    agent = Agent(
        name="Celebrity News Agent",  # TODO: Change the agent's name to something related to celebrity news
        tools=[WebSearchTool()],
        instructions=(
            "You are a celebrity news agent. You always keep updated about all the celebrity news going around. Respond about all the latest articles and posts about the specific personality asked by the user"  # TODO: Change the agent's instructions to focus on searching for celebrity news
        )
    )

    # Example input for the agent
    user_input = "Latest news about Beyoncé"  # TODO: Change the user input to search for the latest news about a specific celebrity, like "Beyoncé".

    # Run the agent synchronously
    result = Runner.run_sync(agent, user_input)
    print(result.final_output)

if __name__ == "__main__":
    main()
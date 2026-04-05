# complete the code

# TODO: Import the necessary classes from the agents module
from agents import Agent, Runner, WebSearchTool

# TODO: Define the main function
def main():

    # TODO: Create an agent with the name "Web Search Agent"
    # TODO: Add the WebSearchTool to the agent's tools
    # TODO: Provide instructions for the agent to use the web search tool
    agent = Agent(
        name="Web Search Agent",
        tools=[WebSearchTool()],
        instructions=(
            "You are a web search agent. You can use the web search tool to find information on the web."
        )
    )    

    # TODO: Set the user input to search for the latest news about a specific topic
    user_input = "Latest news about AI"

    # TODO: Run the agent synchronously and print the result
    result = Runner.run_sync(agent, user_input)
    print(result.final_output)

# TODO: Ensure the main function is called when the script is executed
if __name__ == "__main__":
    main()
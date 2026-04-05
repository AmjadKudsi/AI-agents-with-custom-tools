# add a conditional logic to ensure the agent responds only to queries about celebrities. If the user input is not related to a celebrity, the agent should not provide an answer

from agents import Agent, Runner, WebSearchTool


def main():
    # Create an agent with instructions
    # TODO: Add instructions to the agent to ensure it only responds to queries about celebrities, and does not provide answers for other queries.
    agent = Agent(
        name="Celebrity News Agent",
        tools=[WebSearchTool()],
        instructions=(
            "You are a celebrity news agent. You can use the web search tool to find the latest news about celebrities." 
            "- The agent must ONLY respond if the query is about a celebrity (person in entertainment, sports, politics, etc.)"
            "- If the query is NOT about a celebrity, the agent must respond with a refusal message such as: 'I can only answer questions related to celebrities.'"
            "- The agent should NOT attempt to answer or use tools for non-celebrity queries"
            "- The agent should determine whether a query is celebrity-related before taking any action (including tool usage)"
        )
    )

    user_input = "Latest news about Beyoncé"

    result = Runner.run_sync(agent, user_input)
    print(result.final_output)

    print("======================")

    user_input = "Latest AI news"

    result = Runner.run_sync(agent, user_input)
    print(result.final_output)

if __name__ == "__main__":
    main()
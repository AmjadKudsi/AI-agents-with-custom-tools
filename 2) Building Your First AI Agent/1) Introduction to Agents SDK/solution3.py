# Create a new agent named "History Guide" who explains historical events simply and engagingly

from agents import Agent, Runner

def main():
    # TODO: Create a history guide agent with instructions
    my_agent = Agent(
        name="History Guide",
        instructions="You are a friendly assistant. Answer questions clearly and politely."
    )

    # TODO: Add example input for the history agent
    history_input = "Who won the First and Second World War"

    # TODO: Run the history agent synchronously
    result = Runner.run_sync(my_agent, history_input)
    print(result.final_output)

if __name__ == "__main__":
    main()
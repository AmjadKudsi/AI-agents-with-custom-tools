# Implement the conversationloop for the manager agent

from todo_agent import TODO_AGENT
from rag_agent import RAG_AGENT
from agents import Runner, Agent
from rag_builder import build_rag

MANAGER_AGENT = Agent(
    name="Manager Agent",
    instructions=(
        "You are a manager agent that orchestrates multiple agents. "
        "You can delegate tasks to the Todo Agent and the Learn Agent. "
        "Use the Todo Agent for task management and the Learn Agent for retrieving learning items and returning it to the user."
    ),
    tools=[TODO_AGENT.as_tool(
            tool_name="todo_agent",
            tool_description="A tool for managing tasks using the Todo API"
        ),
        RAG_AGENT.as_tool(
            tool_name="rag_agent",
            tool_description="A tool for providing answers regarding user's learning items"
        )
    ]
)


def run_manager_agent(requests):
    build_rag()

    input_index = 0
    # TODO: Implement the conversation loop. The loop should run until the user inputs "exit" or "quit".
    # For each iteration, the loop should:
    # 1. Get the user input from the requests list
    # 2. Increment the input_index
    # 3. Check if the user input is "exit" or "quit"
    # 4. If it is, break the loop
    # 5. Otherwise, run the manager agent with the user input and print the result
    while True:
        if input_index >= len(requests):
            print("No more user requests. Exiting the manager agent.")
            break

        user_input = requests[input_index]
        input_index += 1
        if user_input.lower() in ["exit", "quit"]:
            print("Exiting the manager agent.")
            break

        result = Runner.run_sync(MANAGER_AGENT, user_input)
        print(f"Manager Agent: {result.final_output}")    
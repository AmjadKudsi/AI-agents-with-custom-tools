# tackle the implementation of the manager agent. Fill in the missing parts in the code

from todo_agent import TODO_AGENT
from rag_agent import RAG_AGENT
from agents import Runner, Agent
from rag_builder import build_rag

MANAGER_AGENT = Agent(
    # TODO: Specify the name of the agent
    
    # TODO: Specify the instructions of the agent. Here is and example:
    # "You are a manager agent that orchestrates multiple agents. "
    # "You can delegate tasks to the Todo Agent and the Learn Agent. "
    # "Use the Todo Agent for task management and the Learn Agent for retrieving learning items and returning it to the user."

    # TODO: Specify the tools of the agent. Remember, we need to use the as_tool method to convert the agents to tools.
    name="Manager Agent",
    instructions=(
        "You are a manager agent that orchestrates multiple agents. "
        "You can delegate tasks to the Todo Agent and the Learn Agent. "
        "Use the Todo Agent for task management and the Learn Agent for retrieving learning items and returning it to the user."
    ),
    tools=[
        TODO_AGENT.as_tool(
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
    while True:
        user_input = requests[input_index]
        input_index += 1
        if user_input.lower() in ["exit", "quit"]:
            print("Exiting the manager agent.")
            break

        result = Runner.run_sync(MANAGER_AGENT, user_input)
        print(f"Manager Agent: {result.final_output}")
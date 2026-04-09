# Complete the code

from agents import Agent, Runner, WebSearchTool, RunContextWrapper, FunctionTool
from pydantic import BaseModel
from typing import Any

# TODO: Define a function read_file that reads the content of a file and handles exceptions
def read_file(data):
    """Custom tool function that can be called by the agent."""
    try:
        with open(data, "r") as file:
            return file.read()
    except Exception as e:
        return f"Error reading file: {e}"


# TODO: Create a FunctionArgs class using BaseModel to define the file_path argument
class FunctionArgs(BaseModel):
    file_path: str


# TODO: Implement an async function run_function to parse arguments and call read_file
async def run_function(ctx: RunContextWrapper[Any], args: str) -> str:
    parsed = FunctionArgs.model_validate_json(args)
    return read_file(parsed.file_path)


# TODO: Set up a FunctionTool named file_read_tool with a description and JSON schema
file_read_tool = FunctionTool(
    name="file_read_tool",
    description="A tool to read the content of a file.",
    params_json_schema={
        "type": "object",
        "properties": {
            "file_path": {"type": "string"},
        },
        "required": ["file_path"],
        "additionalProperties": False
    },
    on_invoke_tool=run_function
)

# TODO: Create a Web Search Agent with the WebSearchTool and appropriate instructions
agent1 = Agent(
    name="Web Search Agent",
    tools=[WebSearchTool()],
    instructions=(
        "You are a web search agent. You can use the web search tool to find information on the web."
    )
)

# TODO: Create a Filesystem Agent with the file_read_tool and appropriate instructions
agent2 = Agent(
    name="Filesystem Agent",
    tools=[file_read_tool],
    instructions=(
        "You are a filesystem agent. You can use the file read tool to read the content of a file."
    )
)

# TODO: Set up an Orchestrator Agent that uses both the web search and file read tools
orchestrator = Agent(
    name="Orchestrator",
    tools=[
        agent1.as_tool(
            tool_name="web_search",
            tool_description="A tool to search the web for information."
        ),
        agent2.as_tool(
            tool_name="file_read",
            tool_description="A tool to read the content of a file."
        )
    ],
    instructions=(
        # TODO: Enhance the instructions to let the orchestrator provide learning goals based on the file content at /usercode/FILESYSTEM/data.txt
        "You are an orchestrator agent. You can use the web search tool to find information on the web and the file read tool to read the content of a file. "
        "If the user asks for learning goals or educational objectives, you should read the file at /usercode/FILESYSTEM/data.txt using the file_read tool, "
        "analyze its content, and generate appropriate learning goals based on that content."
    )
)

# TODO: Implement the main function to run the orchestrator with different queries
def main():
    result = Runner.run_sync(orchestrator, "What is the content of the file /usercode/FILESYSTEM/other.txt")
    print(result.final_output)

    # TODO: Add a call to the orchestrator to provide learning goals without mentioning the file name explicitely
    result = Runner.run_sync(orchestrator, "Provide learning goals based on the available study material.")
    print(result.final_output)

# TODO: Ensure the script runs the main function when executed
if __name__ == "__main__":
    main()
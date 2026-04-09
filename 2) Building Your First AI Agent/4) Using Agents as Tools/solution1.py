# modify the orchestrator's instructions to include the ability to provide learning goals based on the content of a file at /usercode/FILESYSTEM/data.txt
# Update the orchestrator's instructions to include this new feature

from agents import Agent, Runner, WebSearchTool, RunContextWrapper, FunctionTool
from pydantic import BaseModel
from typing import Any

def read_file(data):
    """Custom tool function that can be called by the agent."""
    try:
        with open(data, "r") as file:
            return file.read()
    except Exception as e:
        return f"Error reading file: {e}"

class FunctionArgs(BaseModel):
    file_path: str


async def run_function(ctx: RunContextWrapper[Any], args: str) -> str:
    parsed = FunctionArgs.model_validate_json(args)
    return read_file(parsed.file_path)

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

agent1 = Agent(
    name="Web Search Agent",
    tools=[WebSearchTool()],
    instructions=(
        "You are a web search agent. You can use the web search tool to find information on the web."
    )
)

agent2 = Agent(
    name="Filesystem Agent",
    tools=[file_read_tool],
    instructions=(
        "You are a filesystem agent. You can use the file read tool to read the content of a file."
    )
)

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


def main():
    result = Runner.run_sync(orchestrator, "What is the content of the file /usercode/FILESYSTEM/other.txt")
    print(result.final_output)

    # TODO: Add a call to the orchestrator to provide learning goals without mentioning the file name explicitely
    result = Runner.run_sync(orchestrator, "Provide learning goals based on the available study material.")
    print(result.final_output)

if __name__ == "__main__":
    main()
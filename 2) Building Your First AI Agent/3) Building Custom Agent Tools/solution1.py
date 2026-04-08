# change the code so that the agent reads a file and returns the number of lines in the file instead of its contents

from agents import Agent, Runner, RunContextWrapper, FunctionTool
from pydantic import BaseModel
from typing import Any

def file_read_tool(data):
    """Custom tool function that can be called by the agent."""
    with open(data, "r") as file:
        # TODO: Modify this function to return the number of lines in the file. Hint: Use readlines() to read all the lines into a list.
        return len(file.readlines())

class FunctionArgs(BaseModel):
    file_path: str


async def run_function(ctx: RunContextWrapper[Any], args: str) -> str:
    parsed = FunctionArgs.model_validate_json(args)
    return str(file_read_tool(parsed.file_path))

custom_tool = FunctionTool(
    name="custom_tool",
    description="A custom tool that can be called by the agent.",
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

def main():
    # Create an agent with instructions
    agent = Agent(
        name="File Read Agent",
        tools=[custom_tool],
    )

    # TODO: Update the user input to ask for the number of lines in the file
    user_input = "How many lines are in the file /usercode/FILESYSTEM/data.txt?"

    # Run the agent synchronously
    result = Runner.run_sync(agent, user_input)
    print(result.final_output)

if __name__ == "__main__":
    main()
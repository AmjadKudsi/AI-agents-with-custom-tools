# add the missing parts to complete the implementation

from agents import Agent, Runner, RunContextWrapper, FunctionTool
from pydantic import BaseModel
from typing import Any

def file_read_tool(data):
    """Custom tool function that can be called by the agent."""
    with open(data, "r") as file:
        return file.read()

class FunctionArgs(BaseModel):
    file_path: str

# TODO:
# Implement the async function 'run_function' below.
# - It should take two arguments: a context (ctx) and a string of arguments (args).
# - Parse the arguments using FunctionArgs.model_validate_json(args).
# - Call file_read_tool with the parsed file_path and return the result.
async def run_function(ctx, args: str):
    parsed_args = FunctionArgs.model_validate_json(args)
    return file_read_tool(parsed_args.file_path)

# TODO:
# Create a FunctionTool instance named 'custom_tool'.
# - Set the name to "custom_tool".
# - Provide a description explaining that it reads the contents of a file.
# - Define the params_json_schema to require a "file_path" string.
# - Set on_invoke_tool to the run_function you implemented above.
custom_tool = FunctionTool(
    name="custom_tool",
    description="Reads the contents of a file.",
    params_json_schema={
        "type": "object",
        "properties": {
            "file_path": {"type": "string"},
        },
        "required": ["file_path"],
        "additionalProperties": False,
    },
    on_invoke_tool=run_function,
)

def main():
    # Create an agent with instructions
    agent = Agent(
        name="File Read Agent",
        tools=[custom_tool],
    )

    # Example input for the agent
    user_input = "Read the file /usercode/FILESYSTEM/data.txt"

    # Run the agent synchronously
    result = Runner.run_sync(agent, user_input)
    print(result.final_output)

if __name__ == "__main__":
    main()
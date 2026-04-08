# Modify the code so that if the file path provided does not exist, the agent returns a friendly message indicating that the file was not found

from agents import Agent, Runner, RunContextWrapper, FunctionTool
from pydantic import BaseModel
from typing import Any

# TODO: Update the file reading logic to handle the case where the file does not exist, and return "ERROR: File not found." if the file is not found.
def file_read_tool(data):
    """Custom tool function that can be called by the agent."""
    try:
        with open(data, "r") as file:
            return file.read()
    except FileNotFoundError:
        return "ERROR: File not found."

class FunctionArgs(BaseModel):
    file_path: str


async def run_function(ctx: RunContextWrapper[Any], args: str) -> str:
    parsed = FunctionArgs.model_validate_json(args)
    return file_read_tool(parsed.file_path)

custom_tool = FunctionTool(
    name="custom_tool",
    description="A tool that reads a file and returns its contents, or 'ERROR: File not found.' if the file does not exist.", # TODO: Update the description to reflect that an error message is returned if the file does not exist.
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

    # Example input for the agent with a non-existing file path
    user_input = "Read the file /usercode/FILESYSTEM/non_existing_file.txt"

    # Run the agent synchronously
    result = Runner.run_sync(agent, user_input)
    print(result.final_output)

if __name__ == "__main__":
    main()
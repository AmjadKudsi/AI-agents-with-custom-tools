# complete the code

from agents import Agent, Runner, RunContextWrapper, FunctionTool
from pydantic import BaseModel
from typing import Any

# TODO: Define a function named file_read_tool that takes a file path as input and returns the file's contents
def file_read_tool(file_path):
    """Reads a file and returns its contents."""
    try:
        with open(file_path, "r") as file:
            return file.read()
    except FileNotFoundError:
        return "File not found."

# TODO: Create a Pydantic BaseModel class named FunctionArgs with a single field file_path of type str
class FunctionArgs(BaseModel):
    file_path: str

# TODO: Define an async function named run_function that takes a context and arguments as input, parses the arguments using FunctionArgs, and returns the result of file_read_tool
async def run_function(ctx: RunContextWrapper[Any], args: str) -> str:
    parsed = FunctionArgs.model_validate_json(args)
    return file_read_tool(parsed.file_path)

# TODO: Create a FunctionTool instance named custom_tool with the appropriate name, description, parameter schema, and on_invoke_tool function
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

# TODO: Define a main function that creates an Agent with the custom_tool and runs it with a user input to read a file
def main():
    agent = Agent(
        name="File Read Agent",
        tools=[custom_tool],
    )

    user_input = "Read the file /usercode/FILESYSTEM/data.txt"

# TODO: Use Runner.run_sync to execute the agent and print the final output
    result = Runner.run_sync(agent, user_input)
    print(result.final_output)

# TODO: Ensure the script runs the main function when executed
if __name__ == "__main__":
    main()
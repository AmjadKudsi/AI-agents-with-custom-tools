# complete the word_count_tool function to return the number of words instead. 

from agents import Agent, Runner, RunContextWrapper, FunctionTool
from pydantic import BaseModel
from typing import Any

def word_count_tool(data):
    """Custom tool function that can be called by the agent."""
    # TODO: Implement the function to count words in a file. Hint: use `file.read().split()` to get a list of words.
    with open(data, "r") as file:
        return len(file.read().split())

class FunctionArgs(BaseModel):
    file_path: str


async def run_function(ctx: RunContextWrapper[Any], args: str) -> str:
    parsed = FunctionArgs.model_validate_json(args)
    # TODO: Call the function to count words in the file. Pass the file path from parsed arguments - parsed.file_path
    return str(word_count_tool(parsed.file_path))

custom_tool = FunctionTool(
    name="word_count_tool", # TODO: Fill in the name of the tool
    description="Counts the number of words in a given file", # TODO: Fill in the description of the tool to reflect its functionality
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

    # TODO: Create an input for the agent that instructs it to read a file and count the words for the file /usercode/FILESYSTEM/data.txt
    user_input = "How many words are there in the file /usercode/FILESYSTEM/data.txt?"

    # Run the agent synchronously
    result = Runner.run_sync(agent, user_input)
    print(result.final_output)

if __name__ == "__main__":
    main()
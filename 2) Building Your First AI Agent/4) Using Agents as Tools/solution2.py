# create an orchestrator agent that can use both the web search tool and the file read tool

from agents import Agent, Runner, WebSearchTool, RunContextWrapper, FunctionTool
from pydantic import BaseModel
from typing import Any

def read_file(data):
    """Custom tool function that can be called by the agent."""
    with open(data, "r") as file:
        return file.read()

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

# TODO: Implement the orchestrator agent below as described in the task
# Provide the name "Orchestrator" and include both tools
# Hint: Wrap your specialized agents with `.as_tool()` before adding them to the orchestrator’s tools
# orchestrator = Agent(
#     ...
# )
orchestrator = Agent(
    name="Orchestrator",
    tools=[
        agent1.as_tool(
            tool_name="web_search_agent",
            tool_description="Search the web for up to date information."
        ),
        agent2.as_tool(
            tool_name="filesystem_agent",
            tool_description="Read the contents of a local file."
        ),
    ],
    instructions=(
        "You are an orchestrator agent. Decide whether to use the web search agent, "
        "the filesystem agent, or both. When a request needs both, read the file first "
        "when helpful, use the web tool to gather or verify external information, and "
        "then combine the results into one clear answer."
    )
)

def main():
    # TODO: Run the orchestrator with different queries to test its functionality

    with open("sample_notes.txt", "w") as file:
        file.write(
            "OpenAI was founded in 2015.\n"
            "GPT stands for Generative Pre-trained Transformer.\n"
        )

    queries = [
        "Read the file sample_notes.txt and summarize its contents.",
        "Use the web to tell me who is the current CEO of OpenAI.",
        (
            "Read the file sample_notes.txt, then use the web to verify whether "
            "OpenAI was founded in 2015, and report both the file content and the verification."
        ),
    ]

    for i, query in enumerate(queries, start=1):
        result = Runner.run_sync(orchestrator, query)
        print(f"\n--- Query {i} ---")
        print(f"Request: {query}")
        print(f"Response: {result.final_output}")

if __name__ == "__main__":
    main()
# implement a custom tool for RAG retrieval from scratch
# this tool will enable an agent to fetch the most relevant knowledge chunks based on a user query

from typing import Any
from pydantic import BaseModel
from agents import Agent, Runner, FunctionTool
from rag_builder import load_collection

def retrieve_top_chunks(user_query, top_k=1):
    # TODO: Load the collection using the load_collection function
    collection = load_collection()
    results = collection.query(
        query_texts=[user_query],
        n_results=top_k
    )
    retrieved_chunks = []
    for i in range(len(results['documents'][0])):
        retrieved_chunks.append({
            "chunk": results['documents'][0][i],
            "id": results['metadatas'][0][i]['id'],
            "distance": results['distances'][0][i]
        })
    return retrieved_chunks

# TODO: Define a Pydantic model for input validation with user query as a string
class FunctionArgs(BaseModel):
    user_query: str
    
# TODO: Implement the run_function to use the retrieval function and return results
# - This function should accept a context and args, parse the args, and return the retrieved chunks as a string.
async def run_function(ctx, args: str) -> str:
    parsed = FunctionArgs.model_validate_json(args)
    chunks = retrieve_top_chunks(parsed.user_query)
    return "\n".join([c["chunk"] for c in chunks])

# TODO: Create a FunctionTool to wrap the retrieval logic
# - The tool should have a name, description, params_json_schema, and on_invoke_tool function.
# - The params_json_schema should define the expected input structure:
#   - with type "object", properties "user_query" of type "string", and required "user_query"
# - The on_invoke_tool should call the run function with the provided context and args.

rag_retrieval_tool = FunctionTool(
    name="rag_retrieval_tool",
    description="A tool to retrieve context from RAG based on user query",
    params_json_schema={
        "type": "object",
        "properties": {
            "user_query": {"type": "string"},
        },
        "required": ["user_query"],
        "additionalProperties": False
    },
    on_invoke_tool=run_function
)

# TODO: Create an Agent and integrate the FunctionTool
# - The agent should have a name, e.g. "Learning Assistant",
# - instructions that describe its role, e.g. "You are a personal learning assistant with access to rag tool. Whenever asked a question about learning plans, use the RAG retrieval tool to get context from the DB and answer user questions.",
# - and the tools list containing the rag_retrieval_tool.

AGENT = Agent(
    name="Learning Assistant",
    instructions=(
        "You are a personal learning assistant with access to rag tool. "
        "Whenever asked a question about learning plans, use the RAG retrieval tool to get context from the DB and answer user questions."
    ),
    tools=[rag_retrieval_tool]
)

def ask_agent(prompt):
    result = Runner.run_sync(AGENT, prompt)
    return result.final_output
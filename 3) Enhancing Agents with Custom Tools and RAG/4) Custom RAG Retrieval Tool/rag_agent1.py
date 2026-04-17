# implement the function tool for retrieving context from the RAG collection, add the missing parts in the provided starter code

from typing import Any
from pydantic import BaseModel
from agents import Agent, Runner, FunctionTool
from rag_builder import load_collection

def retrieve_top_chunks(user_query, top_k=3):
    collection = load_collection()
    # TODO: Call the collection's query method to retrieve top_k chunks based on user_query
    results = collection.query(query_texts=[user_query], n_results=top_k)
    retrieved_chunks = []
    for i in range(len(results['documents'][0])):
        retrieved_chunks.append({
            "chunk": results['documents'][0][i],
            "id": results['metadatas'][0][i]['id'],
            "distance": results['distances'][0][i]
        })
    return retrieved_chunks

class FunctionArgs(BaseModel):
    # TODO: Define the function arguments schema for user query as a string
    user_query: str
    

async def run_function(ctx: Any, args: str) -> str:
    parsed = FunctionArgs.model_validate_json(args)
    # TODO: Retrieve top chunks based on user query
    chunks = retrieve_top_chunks(parsed.user_query)
    return "\n".join([f"{c['chunk']} (Score: {c['distance']})" for c in chunks])

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
    on_invoke_tool=run_function  # TODO: Add the function to be invoked here
)

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
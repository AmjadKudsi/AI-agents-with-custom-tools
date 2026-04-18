# write a complete implementation of a Todo API agent from scratch

from agents import Agent, FunctionTool, Runner, RunContextWrapper
from agents import Agent, FunctionTool, Runner, RunContextWrapper
from pydantic import BaseModel
import requests
from enum import Enum
from typing import Any
import json

# TODO: Define the Action enum with a GET action.
#       This enum will represent the possible actions the agent can perform.
#       For now, only support fetching all tasks (GET).
class Action(Enum):
    GET = "get"

# TODO: Define the TodoItem class using Pydantic's BaseModel.
#       This class should have fields: id (int), title (str), done (bool), description (str).
#       It will represent a single todo item returned by the API.
class TodoItem(BaseModel):
    id: int
    title: str
    done: bool
    description: str

# TODO: Define the TodoItemArgs class for input validation.
#       This class should have a single field: action (of type Action).
#       It will be used to validate and parse the arguments passed to the tool.
class TodoItemArgs(BaseModel):
    action: Action

# TODO: Implement the TodoAPI class with methods to get tasks and handle requests.
#       - Add a BASE_URL class variable pointing to "http://127.0.0.1:8000/todos".
#       - Implement a get_tasks class method that fetches tasks from the API and returns a list of TodoItem objects.
#       - Implement a handle_request class method that takes an action and returns the appropriate result (for now, just GET).
class TodoAPI:
    BASE_URL = "http://127.0.0.1:8000/todos"
    
    @classmethod
    def get_tasks(cls):
        response = requests.get(cls.BASE_URL)
        response.raise_for_status()
        return [TodoItem(**item) for item in response.json()]
        
    @classmethod
    def handle_request(cls, action):
        if action == Action.GET:
            tasks = cls.get_tasks()
            tasks_dicts = [task.dict() for task in tasks]
            return tasks_dicts
            
        else:
            raise ValueError(f"Unknown action: {action}")

# TODO: Implement the run_function to process agent requests.
#       - This should be an async function that takes a context and a JSON string of arguments.
#       - Parse the arguments using TodoItemArgs.
#       - Call TodoAPI.handle_request with the parsed action.
#       - Return the result as a JSON string.
async def run_function(ctx: RunContextWrapper[Any], args: str) -> str:
    parsed = TodoItemArgs.model_validate_json(args)
    return json.dumps({"tasks": TodoAPI.handle_request(parsed.action)})

# TODO: Create a FunctionTool for interacting with the Todo API.
#       - Name it "todos_api".
#       - Add a description.
#       - Use TodoItemArgs.model_json_schema() for params_json_schema.
#       - Set on_invoke_tool to run_function.
todos_api_tool = FunctionTool(
    name="todos_api",
    description="A tool for interacting with the Todo API",
    params_json_schema = {
        **TodoItemArgs.model_json_schema(),
        "additionalProperties": False
    },
    on_invoke_tool=run_function
)

# TODO: Assemble the TODO_AGENT with the appropriate instructions and tools.
#       - Name the agent "Todo Manager".
#       - Add instructions describing its purpose and how to use the todos_api tool.
#       - Add the todos_api_tool to the agent's tools list.
TODO_AGENT = Agent(
    name="Todo Manager",
    instructions=(
        "You are a Todo API agent."
        "You can read tasks using the Todo API."
        "Use the todos_api tool to interact with the API."
    ),
    tools=[todos_api_tool]
)

# TODO: Implement the ask_agent function to interact with the agent.
#       - This function should take a prompt string.
#       - Use Runner.run_sync to run the agent with the prompt.
#       - Return the agent's final_output.
def ask_agent(prompt):
    result = Runner.run_sync(TODO_AGENT, prompt)
    return result.final_output
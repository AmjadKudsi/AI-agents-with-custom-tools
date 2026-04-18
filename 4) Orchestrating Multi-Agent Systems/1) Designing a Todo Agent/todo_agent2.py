# Follow the TODOs in the code to complete the task

from agents import Agent, FunctionTool, Runner, RunContextWrapper
from pydantic import BaseModel
import requests
from enum import Enum
from typing import Any
import json

class Action(Enum):
    GET = "get"

class TodoItem(BaseModel):
    id: int
    title: str
    done: bool
    description: str

class TodoItemArgs(BaseModel):
    action: Action

class TodoAPI:
    BASE_URL = "http://127.0.0.1:8000/todos"

    @classmethod
    def get_tasks(cls):
        # TODO: Get all tasks from the Todo API and return them as a list of TodoItem objects
        response = requests.get(cls.BASE_URL)
        response.raise_for_status()
        return [TodoItem(**item) for item in response.json()]


    @classmethod
    def handle_request(cls, action):
        # TODO: If the action is GET, then get all tasks using the get_tasks method and return them as a list of dictionaries
        # TODO: If the action is not GET, then raise a ValueError with the message "Unknown action: {action}"
        if action == Action.GET:
            tasks = cls.get_tasks()
            tasks_dicts = [task.dict() for task in tasks]
            return tasks_dicts
        else:
            raise ValueError(f"Unknown action: {action}")

async def run_function(ctx: RunContextWrapper[Any], args: str) -> str:
    parsed = TodoItemArgs.model_validate_json(args)
    return json.dumps({"result": TodoAPI.handle_request(parsed.action)})

todos_api_tool = FunctionTool(
    name="todos_api",
    description="A tool for interacting with the Todo API",
    params_json_schema={
        **TodoItemArgs.model_json_schema(),
        "additionalProperties": False
    },
    on_invoke_tool=run_function
)

TODO_AGENT = Agent(
    name="Todo Manager",
    instructions=(
        "You are a Todo API agent. "
        "You can read tasks using the Todo API."
        "Use the todos_api tool to interact with the API."
    ),
    tools=[todos_api_tool]
)

def ask_agent(prompt):
    result = Runner.run_sync(TODO_AGENT, prompt)
    return result.final_output
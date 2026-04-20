# Update the TodoAPI class and the handle_request method to support the PUT and DELETE actions

from agents import Agent, FunctionTool, Runner, RunContextWrapper
from pydantic import BaseModel
from enum import Enum
from typing import Any
import json
import requests

class Action(str, Enum):
    GET = "get"
    POST = "post"
    PUT = "put"
    DELETE = "delete"

class TodoItem(BaseModel):
    id: int
    title: str
    done: bool
    description: str

class TodoItemArgs(BaseModel):
    action: Action
    task: TodoItem

class TodoAPI:
    BASE_URL = "http://127.0.0.1:8000/todos"

    @classmethod
    def get_tasks(cls):
        response = requests.get(cls.BASE_URL)
        response.raise_for_status()
        return [TodoItem(**item) for item in response.json()]

    @classmethod
    def create_task(cls, task: TodoItem):
        response = requests.post(cls.BASE_URL, json=task.dict())
        response.raise_for_status()
        return TodoItem(**response.json())

    @classmethod
    def update_task(cls, task: TodoItem):
        # TODO: Implement the update_task method that will update a task using the Todo API at the /todos/{id} endpoint using the PUT method
        # Return the updated task as a TodoItem object
        response = requests.put(f"{cls.BASE_URL}/{task.id}", json=task.dict())
        response.raise_for_status() 
        return TodoItem(**response.json())

    @classmethod
    def delete_task(cls, task: TodoItem):
        # TODO: Implement the delete_task method that will delete a task using the Todo API at the /todos/{id} endpoint using the DELETE method
        # Return a message indicating that the task was deleted successfully
        response = requests.delete(f"{cls.BASE_URL}/{task.id}")
        response.raise_for_status() 
        return {"message": "Task deleted successfully"}

    @classmethod
    def handle_request(cls, action, task):
        if action == Action.GET:
            tasks = cls.get_tasks()
            return [t.dict() for t in tasks]
        elif action == Action.POST:
            return cls.create_task(task).dict()
        # TODO: Implement the PUT and DELETE cases to call the update_task and delete_task methods respectively
        elif action == Action.PUT:
            return cls.update_task(task).dict() 
        elif action == Action.DELETE:
            return cls.delete_task(task)                 
        else:
            raise ValueError(f"Unknown action: {action}")

async def run_function(ctx: RunContextWrapper[Any], args: str) -> str:
    parsed = TodoItemArgs.model_validate_json(args)
    result = TodoAPI.handle_request(parsed.action, parsed.task)
    return json.dumps({"result": result})

model_json_schema = TodoItemArgs.model_json_schema()
model_json_schema["additionalProperties"] = False
model_json_schema["$defs"]["TodoItem"]["additionalProperties"] = False

todos_api_tool = FunctionTool(
    name="todos_api",
    description="A tool for interacting with the Todo API",
    params_json_schema=model_json_schema,
    on_invoke_tool=run_function
)

TODO_AGENT = Agent(
    name="Todo Manager",
    instructions=(
        "You are a Todo API agent. "
        "You can create, read, update, delete, and partially update tasks using the Todo API. "
        "Use the todos_api tool to interact with the API. "
        "For GET and PUT actions: always first list all tasks (use GET), then proceed with the requested operation (for PUT, update the task after listing). "
        "For DELETE action: you must first list all the tasks, identify the ID of the task you need to remove and then use the tool to delete the task."
    ),
    tools=[todos_api_tool]
)

def ask_agent(prompt):
    result = Runner.run_sync(TODO_AGENT, prompt)
    return result.final_output
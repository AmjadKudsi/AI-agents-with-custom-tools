# add a small testing script that will call the API directly to confirm id the agent did the right thing

from todo_agent import ask_agent
import requests

# TODO: Add a function that will directly call the Todo API to get all tasks.
# The API is running on http://127.0.0.1:8000 and the endpoint is /todos.
def get_tasks():
    response = requests.get("http://127.0.0.1:8000/todos")
    response.raise_for_status()
    return response.json()

def main():
    # Example usage of the Todo API agent
    query = "Hey list all my tasks"
    response = ask_agent(query)
    print(response)

    query = "Hey update the task with the title 'Buy groceries' to mark it as done"
    response = ask_agent(query)
    print(response)

    # TODO: Call the get_tasks function and print the result – observe if the Buy groceries task is indeed marked as done
    tasks = get_tasks()
    print(tasks)    

if __name__ == '__main__':
    main()
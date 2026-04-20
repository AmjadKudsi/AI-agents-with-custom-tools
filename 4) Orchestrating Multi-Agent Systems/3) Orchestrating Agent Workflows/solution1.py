# Update the user inputs to include a request to "What are my learning plans for React" and observe how the system responds differently using the appropriate agent.

from manager import run_manager_agent

if __name__ == '__main__':
    user_inputs = [
        "List all my tasks",
        # TODO: Add a new request "What are my learning plans for React"
        "What are my learning plans for React",
        "exit"
    ]

    run_manager_agent(user_inputs)
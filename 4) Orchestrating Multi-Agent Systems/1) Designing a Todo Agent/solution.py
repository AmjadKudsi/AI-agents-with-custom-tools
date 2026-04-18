from todo_agent import ask_agent

def main():
    # Example usage of the Todo API agent
    query = "Hey list all my tasks"
    response = ask_agent(query)
    print(response)

if __name__ == '__main__':
    main()
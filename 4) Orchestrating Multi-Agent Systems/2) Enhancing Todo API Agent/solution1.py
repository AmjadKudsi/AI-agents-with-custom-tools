# add a new prompt that will update the task with the title "Buy groceries" to mark it as done

from todo_agent import ask_agent

def main():
    query = "Hey list all my tasks"
    response = ask_agent(query)

    print(response)

    # TODO: Create a new prompt that will update the task with the title "Buy groceries"
    query =  "Mark the task with the title 'Buy groceries' as done"
    
    # TODO: Call the ask_agent function with the new prompt and print the response
    response = ask_agent(query)
    print(response)    

if __name__ == '__main__':
    main()
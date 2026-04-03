# focus on creating a simple chat loop that continues to prompt the user for input until they type exit

def main():
    print("Welcome to the Superhero Chat Assistant!")
    while True:
        user_input = input("Hero: ").strip()
        print(f"User: {user_input}")
        # TODO: Add a condition to break the loop when user_input is "exit"
        if user_input.lower() == "exit":
            print("Assistant: Goodbye, hero!")
            break

if __name__ == "__main__":
    main()
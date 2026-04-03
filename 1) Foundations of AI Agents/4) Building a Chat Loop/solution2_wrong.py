# make your assistant more user-friendly by handling empty or whitespace-only input
# If the user presses Enter without typing anything (or only types spaces), the assistant should print "Please provide a valid input."

def main():
    print("Welcome to the Superhero Chat Assistant!")
    while True:
        user_input = input("Hero: ").strip()
        # TODO: If the input is empty after stripping whitespace, prompt for valid input and continue
        print(f"User: {user_input}")
        
        if not user_input:
            print("Please provide a valid input.")
            
        if user_input.lower() == "exit":
            print("Assistant: Goodbye, hero!")
            break

if __name__ == "__main__":
    main()
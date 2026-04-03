# You're correctly checking for empty input, but the code still prints User: even when the input is blank
# How can you skip the rest of the code in the loop and jump straight back to the start when the input is invalid?

def main():
    print("Welcome to the Superhero Chat Assistant!")
    while True:
        user_input = input("Hero: ").strip()
        # TODO: If the input is empty after stripping whitespace, prompt for valid input and continue        
        if not user_input:
            print("Please provide a valid input.")
            continue

        print(f"User: {user_input}")
        if user_input.lower() == "exit":
            print("Assistant: Goodbye, hero!")
            break

if __name__ == "__main__":
    main()
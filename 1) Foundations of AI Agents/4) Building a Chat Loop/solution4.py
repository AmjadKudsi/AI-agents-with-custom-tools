# build a chat loop that allows a user to interact with an AI assistant, which provides helpful and knowledgeable responses
# New requirement: The system instructions should be read from a file (e.g., system_instruction.txt) instead of being hardcoded in the script.

from openai import OpenAI
import os

def load_system_instruction(filename="system_instruction.txt"):
    # TODO: Read and return the contents of the system instruction file
    with open(filename, "r", encoding="utf-8") as f:
        return f.read().strip()

def build_messages(user_input, history=None, system_instruction=None):
    # TODO: Use the system_instruction argument (or load from file if None)
    # TODO: Initialize the messages list with the system instruction
    # TODO: Append user and assistant messages from history to the messages list
    # TODO: Append the current user input to the messages list
    if system_instruction is None:
        system_instruction = load_system_instruction()
        
    messages = [{"role": "system", "content": system_instruction}]
    
    if history:
        for user_msg, assistant_msg in history[-5:]:
            messages.append({"role": "user", "content": user_msg})
            messages.append({"role": "assitant", "content": assistant_msg})
            
    messages.append({"role": "user", "content": user_input})
    return messages

def get_completion(messages, model="gpt-4o", max_tokens=50, temperature=0.7):
    try:
        # TODO: Initialize the OpenAI client
        # TODO: Create a chat completion with the given parameters
        # TODO: Return the assistant's response
        client = OpenAI()
        
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature
        )
        return response.choices[0].message.content
        
    except Exception as e:
        # TODO: Return an error message if an exception occurs
        return f"Error: {e}"

def main():
    try:
        print("OpenAI Chat Completions API - Basic Assistant Demo")
        print("=" * 40)

        # TODO: Load the system instruction from file
        # TODO: Initialize the history list
        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError("OPENAI_API_KEY environment variable is not set.")
            
        system_instruction = load_system_instruction()
        history = []
        

        while True:
            # TODO: Get user input and strip any leading/trailing whitespace
            # TODO: Check if the user wants to exit the chat
            # TODO: Handle empty user input
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() in {"exit", "quit", "bye"}:
                print("Goodbye!")
                break
                
            if not user_input:
                print("Please enter a valid message.")
                continue

            # TODO: Build the messages list with the current user input and recent history
            # TODO: Get the assistant's response using the OpenAI API
            # TODO: Print the user input and assistant's response
            # TODO: Append the user input and assistant's response to the history
            messages = build_messages(user_input, history=history, system_instruction=system_instruction)
            assistant_response = get_completion(messages)
            
            print(f"You: {user_input}")
            print(f"Assistant: {assistant_response}")
            
            history.append((user_input, assistant_response))

    except ValueError as ve:
        # TODO: Handle configuration errors (e.g., missing API key)
        print(f"Configuration error: {ve}")
    except Exception as e:
        # TODO: Handle unexpected errors
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()


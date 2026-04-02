# Complete the script and ask "What is the capital of Japan?"

# TODO: Import necessary modules: sys, OpenAI, and OpenAIError
from openai import OpenAI, OpenAIError


# TODO: Define the main function
def main():
    """Send a simple prompt to the OpenAI Chat Completions API."""
    try:
        # TODO: Initialize the OpenAI client
        client = OpenAI()

        # TODO: Create a message list with a prompt asking "What is the capital of Japan?"
        messages = [
            {"role": "user", "content": "What is the capital of Japan?"}
        ]

        # TODO: Use the client to create a chat completion with the specified model and max_tokens
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            max_tokens=50
        )

        # TODO: Print the prompt
        print("Prompt:", messages[0]["content"])

        # TODO: Check if the completion has choices and print the first choice's content
        if completion and hasattr(completion, "choices") and len(completion.choices) > 0:
            print("Completion:", completion.choices[0].message.content.strip())
        else:
            print("No completion returned.")

    except OpenAIError as oe:
        # TODO: Handle OpenAI API errors and exit with status code 2
        print(f"OpenAI API Error: {oe}", file=sys.stderr)
        sys.exit(2)

    except Exception as e:
        # TODO: Handle any other exceptions and exit with status code 3
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(3)

# TODO: Call the main function if this script is executed
if __name__ == "__main__":
    main()
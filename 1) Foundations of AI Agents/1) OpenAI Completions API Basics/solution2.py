# specify the model to use for the API request (configure the model parameter in an OpenAI API request)

import os
import sys
from openai import OpenAI
from openai import OpenAIError

def main():
    """Send a simple prompt to the OpenAI Chat Completions API."""
    try:
        client = OpenAI()
        messages = [
            {"role": "user", "content": "What is the capital of Italy?"}
        ]
        completion = client.chat.completions.create(
            model="gpt-4o",  # TODO: Add the model name here
            messages=messages,
            max_tokens=50
        )
        print("Prompt:", messages[0]["content"])
        if completion and hasattr(completion, "choices") and len(completion.choices) > 0:
            print("Completion:", completion.choices[0].message.content.strip())
        else:
            print("No completion returned.")
    except OpenAIError as oe:
        print(f"OpenAI API Error: {oe}", file=sys.stderr)
        sys.exit(2)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(3)

if __name__ == "__main__":
    main()
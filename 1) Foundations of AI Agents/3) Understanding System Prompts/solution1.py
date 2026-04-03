# Update the build_messages function to include this new style, and test it in the main function

import os
from openai import OpenAI

def build_messages(user_input, style="friendly"):
    if style == "friendly":
        system_instruction = (
            "You are a helpful and friendly assistant. "
            "Answer clearly and politely."
        )
    elif style == "formal":
        system_instruction = (
            "You are a formal and professional assistant. "
            "Provide concise and accurate responses."
        )
    # TODO: Add a new 'enthusiastic' style here
    elif style == "enthusiastic":
        system_instruction = (
            "You are a highly energetic and enthusiastic assistant."
            "Provide a clear response with great excitement."
        )
    else:
        system_instruction = ""
    return [
        {"role": "system", "content": system_instruction},
        {"role": "user", "content": user_input}
    ]

def main():
    try:
        client = OpenAI()
        user_input = "How do I bake a chocolate cake?"
        for style in ["friendly", "formal", "enthusiastic"]:
            # TODO: Add "enthusiastic" to the list of styles
            messages = build_messages(user_input, style)
            print(f"\n--- Style: {style} ---")
            completion = client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                max_tokens=80,
                temperature=0.7
            )
            print(completion.choices[0].message.content.strip())
    except ValueError as ve:
        print(f"Configuration Error: {ve}")
        print("Please set your OPENAI_API_KEY environment variable.")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()
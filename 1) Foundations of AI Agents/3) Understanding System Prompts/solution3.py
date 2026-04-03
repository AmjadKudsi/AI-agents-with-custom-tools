# Create the system instructions in the file named system_prompt.txt and read its content to set the system instruction for the LLM

import os
from openai import OpenAI

def build_messages(user_input):
    # Read the system instruction from 'system_prompt.txt'
    # TODO: Read the content of the system_prompt.txt into the variable system_instruction
    with open("system_prompt.txt", "r", encoding="utf-8") as file:
        system_instruction = file.read().strip()

    return [
        {"role": "system", "content": system_instruction},
        {"role": "user", "content": user_input}
    ]

def main():
    try:
        client = OpenAI()
        user_input = "How do I bake a chocolate cake?"
        messages = build_messages(user_input)
        print("\n--- AI Assistant ---")
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            max_tokens=80,
            temperature=0.7
        )
        print(completion.choices[0].message.content.strip())
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
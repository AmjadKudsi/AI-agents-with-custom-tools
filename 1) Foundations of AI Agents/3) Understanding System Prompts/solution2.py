# further enhance it by introducing a calm style

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
    elif style == "enthusiastic":
        system_instruction = (
            "You are an enthusiastic and energetic assistant. "
            "Respond with excitement and positivity."
        )
    # TODO: Add a new style 'calm' with appropriate system instruction
    elif style == "calm":
        system_instruction = (
            "You are an assistant with a calm personality. "
            "Respond with soothness, in a composed manner."
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
        for style in ["friendly", "formal", "enthusiastic", "calm"]:  # TODO: Add 'calm' to the list of styles
            messages = build_messages(user_input, style)
            print(f"\n--- Style: {style} ---")
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
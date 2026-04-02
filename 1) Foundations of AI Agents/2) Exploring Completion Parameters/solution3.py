# add the missing parts to complete the code that experiments with different max_tokens values

import os
from openai import OpenAI
from openai import OpenAIError

def main():
    """Experiment with different completion parameters."""
    try:
        client = OpenAI()
        prompt = "Write a short story about a robot learning to paint."
        print("Prompt:", prompt)

        for max_tokens in [20, 40, 60]:
            print(f"\n--- Max Tokens: {max_tokens} ---")
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,  # TODO: Add the max_tokens variable here
                temperature=0.5
            )
            # Ensure the response has choices and content
            if response and hasattr(response, "choices") and len(response.choices) > 0:
                print(response.choices[0].message.content.strip())
            else:
                print("No completion returned.")
    except ValueError as ve:
        print(f"Configuration Error: {ve}")
        print("Please set your OPENAI_API_KEY environment variable.")
    except OpenAIError as oe:
        print(f"OpenAI API Error: {oe}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()
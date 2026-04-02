# add the missing parts to complete the code that experiments with different temperature values

import os
from openai import OpenAI
from openai import OpenAIError

def main():
    """Experiment with different completion parameters."""
    try:
        client = OpenAI()
        prompt = "Write a short story about a robot learning to paint."
        print("Prompt:", prompt)

        for temp in [0.2, 0.7, 1.0]:
            print(f"\n--- Temperature: {temp} ---")
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=30,
                temperature=temp  # TODO: Add the temperature variable here
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
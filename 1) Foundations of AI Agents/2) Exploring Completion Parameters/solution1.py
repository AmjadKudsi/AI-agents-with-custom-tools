# Change the code to generate responses with a maximum of 30 tokens instead

import os
import sys
from openai import OpenAI, OpenAIError

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
                temperature=temp
            )
            # Ensure the response has choices and content
            if response and hasattr(response, "choices") and len(response.choices) > 0:
                print(response.choices[0].message.content.strip())
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
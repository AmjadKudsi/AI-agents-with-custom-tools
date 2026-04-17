from rag_builder import build_rag
from rag_agent import ask_agent

def main():
    build_rag()
    # TODO: Define a prompt and call the ask_agent function. At the end, print the response.
    prompt = "Create a learning plan for me."
    response = ask_agent(prompt)
    print(response)

if __name__ == '__main__':
    main()
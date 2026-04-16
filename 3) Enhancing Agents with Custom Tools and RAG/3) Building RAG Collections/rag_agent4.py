from agents import Agent, Runner

# TODO: Define an agent that processes prompts and returns responses with the following properties
# - Name: "Learning Assistant"
# - Instructions: "You are a personal learning assistant. Whenever asked a question about learning plans, use the context provided to answer questions."

# TODO: Implement the ask_agent function to process prompts using the Runner and return the final output
# rag_agent.py
learning_assistant = Agent(
    name="Learning Assistant",
    instructions=(
        "You are a personal learning assistant. Whenever asked a question "
        "about learning plans, use the context provided to answer questions."
    ),
)

def ask_agent(prompt):
    result = Runner.run_sync(learning_assistant, prompt)
    return result.final_output
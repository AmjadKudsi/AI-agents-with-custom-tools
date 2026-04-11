# Complete the code

# TODO: Import needed modules:
# - os and json for reading the JSON file
# - re for simple punctuation removal
# - ask_agent from rag_agent to run the agent with a prompt
import os
import json
import re
from rag_agent import ask_agent

# TODO: Implement load_data(file_name):
# - Build the path to data/<file_name> using os.path
# - Open and load JSON content
# - Return the loaded list of note dicts
def load_data(file_name):
    file_path = os.path.join("data", file_name)
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

# TODO: Implement tokenize(text):
# - Lowercase the text
# - Remove punctuation using a regex (replace non-word, non-space with a space)
# - Split into words and return a set of unique tokens
def tokenize(text):
    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text)
    return set(text.split())

# TODO: Implement rag_retrieval(query, knowledge_base):
# - Tokenize the query
# - For each document in the knowledge base:
#   - Tokenize doc["content"]
#   - Compute overlap size between query tokens and doc tokens
# - Track the best document by highest overlap score
# - Tie-break: if scores are equal and positive, choose the doc with smaller id
# - Return the best document, or None if there is no overlap
def rag_retrieval(query, knowledge_base):
    query_tokens = tokenize(query)
    best_doc = None
    best_score = 0
    for doc in knowledge_base:
        doc_tokens = tokenize(doc["content"])
        score = len(query_tokens & doc_tokens)
        
        if score > best_score:
            best_score = score
            best_doc = doc
        elif score == best_score and score > 0 and best_doc is not None:
            if doc["id"] < best_doc["id"]:
                best_doc = doc
    return best_doc if best_score > 0 else None

# TODO: Implement build_prompt(user_prompt, rag_document=None):
# - If rag_document is provided, return:
#   "Question: <user_prompt>\nContext: <rag_document['content']>\nAnswer:"
# - Otherwise, return the original user_prompt
def build_prompt(user_prompt, rag_document=None):
    if rag_document is not None:
        return f"Question: {user_prompt}\nContext: {rag_document['content']}\nAnswer:"
    return user_prompt

# TODO: Implement main():
# - Load data from "data.json"
# - Define a user query like: "What should I focus on for SQL joins?"
# - Run rag_retrieval to get the best document
# - Build the prompt with build_prompt
# - Call ask_agent(prompt) and print the response
def main():
    knowledge_base = load_data("data.json")
    user_query = "What should I focus on for SQL joins?"
    best_doc = rag_retrieval(user_query, knowledge_base)
    prompt = build_prompt(user_query, best_doc)
    response = ask_agent(prompt)
    print(response)

# TODO: Add the standard Python entry point guard to call main():
# if __name__ == '__main__':
#     main()
if __name__ == "__main__":
    main()
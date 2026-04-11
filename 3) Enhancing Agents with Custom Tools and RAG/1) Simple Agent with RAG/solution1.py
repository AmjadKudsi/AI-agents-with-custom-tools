# it returns only the document with the highest word overlap
# Modify it to return a list of all documents that share at least one word with the query, sorted by the number of overlapping words in descending order

import os
import json
from rag_agent import ask_agent
from agents import Runner

def load_data(file_name):
    """Load sample knowledge base content from JSON file."""
    current_dir = os.path.dirname(__file__)
    dataset_file = os.path.join(current_dir, "data", file_name)
    with open(dataset_file, 'r') as file:
        return json.load(file)
        
def rag_retrieval(query, knowledge_base):
    query_words = set(query.lower().split())
    matched_docs = []

    for doc in knowledge_base:
        doc_words = set(doc["content"].lower().split())
        overlap = len(query_words.intersection(doc_words))
        if overlap > 0:
            matched_docs.append((overlap, doc))

    matched_docs.sort(key=lambda x: x[0], reverse=True)
    return [doc for overlap, doc in matched_docs]

def build_prompt(user_prompt, rag_documents=None):
    if rag_documents:
        docs_text = " ".join(doc["content"] for doc in rag_documents)
        return f"Based on the following documents: {docs_text}, {user_prompt}"
    return user_prompt


def main():
    data = load_data("data.json")

    query = "How should I start tackling React useContext"

    rag_documents = rag_retrieval(query, data)

    query = build_prompt(query, rag_documents)

    response = ask_agent(query)

    print(response)

if __name__ == '__main__':
    main()
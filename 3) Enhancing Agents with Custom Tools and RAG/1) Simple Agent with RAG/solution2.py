# Add a top_k parameter to limit results to the most relevant notes by word overlap
# list those notes as a bulleted Context in the prompt. If nothing matches, send the original question as is

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

def rag_retrieval(query, knowledge_base, top_k=3):
    """
    Return up to top_k most relevant documents by word overlap.
    """
    # TODO: Convert the query to lowercase words and store in a set
    query_words = set(query.lower().split())

    # Collect (doc, overlap_score) for docs with at least one overlapping word
    scored = []

    # TODO: Iterate through the knowledge base and compute overlap
    for doc in knowledge_base:
        # TODO: Lowercase and split document content into words
        doc_words = set(doc["content"].lower().split())

        # TODO: Compute overlap score between query_words and doc_words
        overlap = len(query_words.intersection(doc_words))

        # TODO: Keep only documents with positive overlap
        if overlap > 0:
            scored.append((doc, overlap))

    # TODO: Sort by overlap descending
    scored.sort(key=lambda x: x[1], reverse=True)

    # TODO: Return only the top_k documents (no scores)
    return [d for d, _ in scored[:top_k]]

def build_prompt(user_prompt, rag_documents=None):
    """
    Build a prompt that lists retrieved notes under a Context section.
    If no documents are provided, return the original question.
    """
    if rag_documents:
        # TODO: Create a bullet list string from rag_documents' content lines
        context_lines = "\n".join(f"- {doc['content']}" for doc in rag_documents)
        # TODO: Compose the final prompt with question, context, and answer cue
        return f"Question: {user_prompt}\nContext:\n{context_lines}\nAnswer:"
    return user_prompt

def main():
    data = load_data("data.json")

    query = "How should I start tackling React useContext"
    top_k = 3

    rag_documents = rag_retrieval(query, data, top_k=top_k)

    prompt = build_prompt(query, rag_documents)

    response = ask_agent(prompt)

    print(response)

if __name__ == '__main__':
    main()
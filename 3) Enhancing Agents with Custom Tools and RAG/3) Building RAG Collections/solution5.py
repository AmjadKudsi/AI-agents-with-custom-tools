# complete the code

from agents import Agent, Runner
import os
import json
from chromadb import Client
from chromadb.config import Settings
from chromadb.utils import embedding_functions
from rag_agent import ask_agent

def load_data(file_name):
    current_dir = os.path.dirname(__file__)
    dataset_file = os.path.join(current_dir, "data", file_name)
    with open(dataset_file, 'r') as file:
        return json.load(file)

def chunk_text(text, chunk_size=30):
    chunks = []
    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i + chunk_size])
    return chunks

def chunk_dataset(data, chunk_size=30):
    all_chunks = []
    for doc_id, doc in enumerate(data):
        doc_text = doc["content"]
        doc_chunks = chunk_text(doc_text, chunk_size)
        for chunk_id, chunk_str in enumerate(doc_chunks):
            all_chunks.append({
                "id": doc_id,
                "chunk_id": chunk_id,
                "text": chunk_str,
            })
    return all_chunks


def build_chroma_collection(chunks, collection_name="rag_collection"):
    # TODO: Create an embedding function and collection, then add all chunks to the collection
    embedding_fn = embedding_functions.DefaultEmbeddingFunction()

    client = Client(Settings())
    collection = client.get_or_create_collection(
        name=collection_name,
        embedding_function=embedding_fn
    )

    collection.add(
        ids=[f'{chunk["id"]}_{chunk["chunk_id"]}' for chunk in chunks],
        documents=[chunk["text"] for chunk in chunks],
        metadatas=[
            {"id": chunk["id"], "chunk_id": chunk["chunk_id"]}
            for chunk in chunks
        ],
    )

    return collection

def retrieve_top_chunks(query, collection, top_k=1):
    # TODO: Query the collection for top-k relevant chunks and return them
    results = collection.query(
        query_texts=[query],
        n_results=top_k
    )
    return results["documents"][0]

def build_prompt(user_prompt, retrieved_chunks=[]):
    # TODO: Build a prompt with the user question and retrieved context
    context = "\n".join(retrieved_chunks)
    return f"Context:\n{context}\n\nQuestion: {user_prompt}"

def main():
    # TODO: Load data, chunk it, build the collection, retrieve chunks, build the prompt, and ask the agent
    data = load_data("data.json")
    chunks = chunk_dataset(data)
    collection = build_chroma_collection(chunks)

    user_prompt = input("Enter your question: ")
    retrieved_chunks = retrieve_top_chunks(user_prompt, collection, top_k=3)
    prompt = build_prompt(user_prompt, retrieved_chunks)

    response = ask_agent(prompt)
    print(response)

if __name__ == "__main__":
    main()
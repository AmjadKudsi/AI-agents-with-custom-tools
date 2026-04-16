# retrieve_top_chunks function is set to retrieve only one top chunk. Modify the main function to change the top_k parameter from 1 to 2

import os
import json
from chromadb import Client
from chromadb.config import Settings
from chromadb.utils import embedding_functions

def load_data(file_name):
    current_dir = os.path.dirname(__file__)
    dataset_file = os.path.join(current_dir, "data", file_name)
    with open(dataset_file, 'r') as file:
        return json.load(file)

def chunk_text(text, chunk_size=60):
    chunks = []
    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i + chunk_size])
    return chunks

def chunk_dataset(data, chunk_size=60):
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
    model_name = 'sentence-transformers/all-MiniLM-L6-v2'
    embed_func = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=model_name)
    client = Client(Settings())
    collection = client.get_or_create_collection(name=collection_name, embedding_function=embed_func)

    texts = [c["text"] for c in chunks]
    ids = [f"chunk_{c['id']}_{c['chunk_id']}" for c in chunks]
    metadatas = [{"id": c["id"], "chunk_id": c["chunk_id"]} for c in chunks]

    collection.add(documents=texts, metadatas=metadatas, ids=ids)

    return collection

def retrieve_top_chunks(query, collection, top_k=2):
    results = collection.query(
        query_texts=[query],
        n_results=top_k
    )
    retrieved_chunks = []
    for i in range(len(results['documents'][0])):
        retrieved_chunks.append({
            "chunk": results['documents'][0][i],
            "id": results['metadatas'][0][i]['id'],
            "distance": results['distances'][0][i]
        })
    return retrieved_chunks

def main():
    data = load_data("data.json")
    chunked_data = chunk_dataset(data)

    rag_collection = build_chroma_collection(chunked_data)

    query = "What are my learning plans for React"
    # TODO: Change the top_k parameter from 1 to 2
    retrieved_chunks = retrieve_top_chunks(query, rag_collection, top_k=1)

    print(retrieved_chunks)

if __name__ == "__main__":
    main()
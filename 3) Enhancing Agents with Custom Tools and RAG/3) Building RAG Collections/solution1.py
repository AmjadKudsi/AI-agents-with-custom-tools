# Create an embedding function, Initialize a ChromaDB client, Add all the provided chunks to the collection

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
    # TODO: Implement this function:
    # 1. Create an embedding function using 'sentence-transformers/all-MiniLM-L6-v2'
    # 2. Initialize a ChromaDB client and get or create a collection with the given name and embedding function
    # 3. Add all chunks to the collection with their text, unique IDs, and metadata
    # 4. Return the collection
    model_name = 'sentence-transformers/all-MiniLM-L6-v2'
    embed_func = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=model_name)
    
    client = Client(Settings())
    collection = client.get_or_create_collection(
        name=collection_name,
        embedding_function=embed_func
    )
    
    texts = [c["text"] for c in chunks]
    ids = [f"chunk_{c['id']}_{c['chunk_id']}" for c in chunks] 
    metadatas = [{"id": c["id"], "chunk_id": c["chunk_id"]} for c in chunks]
    
    collection.add(documents=texts, metadatas=metadatas, ids=ids)
    return collection

def retrieve_top_chunks(query, collection, top_k=1):
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

def build_prompt(user_prompt, retrieved_chunks=[]):
    prompt = f"Question: {user_prompt}\nContext:\n"
    for rc in retrieved_chunks:
        prompt += f"- {rc['chunk']}\n"
    prompt += "Answer:"
    return prompt

def main():
    data = load_data("data.json")
    chunked_data = chunk_dataset(data)

    rag_collection = build_chroma_collection(chunked_data)

    print(rag_collection)

if __name__ == "__main__":
    main()
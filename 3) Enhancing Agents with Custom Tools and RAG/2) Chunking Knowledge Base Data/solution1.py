# the code chunks the text by a fixed number of characters
# change the chunk_text function to chunk the text by a fixed number of words instead

import os
import json

def load_data(file_name):
    """Load sample knowledge base content from JSON file."""
    current_dir = os.path.dirname(__file__)
    dataset_file = os.path.join(current_dir, "data", file_name)
    with open(dataset_file, 'r') as file:
        return json.load(file)

def chunk_text(text, chunk_size=30):
    """Chunk text into smaller pieces based on a fixed number of words."""
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
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

def main():
    data = load_data("data.json")
    chunked_data = chunk_dataset(data)

    print("Loaded and chunked", len(chunked_data), "chunks from dataset.")
    for c in chunked_data:
        print(c)

if __name__ == "__main__":
    main()
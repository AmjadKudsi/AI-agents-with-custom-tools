# enhance the chunk_dataset function by completing the missing parts in the starter code

import os
import json

def load_data(file_name):
    """Load sample knowledge base content from JSON file."""
    current_dir = os.path.dirname(__file__)
    dataset_file = os.path.join(current_dir, "data", file_name)
    with open(dataset_file, 'r') as file:
        return json.load(file)

def chunk_text(text, chunk_size=5):
    """Chunk text into smaller pieces by word count for better processing."""
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunks.append(' '.join(words[i:i + chunk_size]))
    return chunks

def chunk_dataset(data, chunk_size=5):
    all_chunks = []
    for doc_id, doc in enumerate(data):
        # TODO: Retrieve the content of the document
        doc_text = doc["content"]
        # TODO: Chunk the document text into smaller pieces with the specified chunk size
        doc_chunks = chunk_text(doc_text, chunk_size)
        for chunk_id, chunk_str in enumerate(doc_chunks):
            # TODO: Append each chunk with its metadata to the all_chunks list
            all_chunks.append({
                "id": doc_id,
                "chunk_id": chunk_id,
                "text": chunk_str,
                "length": len(chunk_str.split())
            })
    return all_chunks

def main():
    """Main function to create and simple knowledge base."""
    data = load_data("data.json")
    chunked_data = chunk_dataset(data)

    print("Loaded and chunked", len(chunked_data), "chunks from dataset.")
    for c in chunked_data:
        print(c)

if __name__ == "__main__":
    main()
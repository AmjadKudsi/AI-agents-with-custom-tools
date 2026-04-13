# complete the code

import os
import json

# TODO: Define a function `load_data` that loads JSON data from a file.
# The function should take a file name as an argument and return the loaded data.
def load_data(file_name):
    """Load JSON data from a file and return the parsed object."""
    if not os.path.exists(file_name):
        raise FileNotFoundError(f"File not found: {file_name}")

    with open(file_name, "r", encoding="utf-8") as f:
        return json.load(f)


# TODO: Define a function `chunk_text` that splits text into smaller chunks.
# The function should take a text and a chunk size as arguments and return a list of text chunks.
def chunk_text(text, chunk_size):
    """Split text into smaller fixed-size chunks."""
    if not isinstance(text, str):
        text = str(text)

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")

    text = text.strip()
    if not text:
        return []

    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]


# TODO: Define a function `chunk_dataset` that processes a dataset to create chunks.
# The function should take the dataset and a chunk size as arguments and return a list of chunks with metadata.
def chunk_dataset(dataset, chunk_size):
    """
    Process a dataset and return chunked text with metadata.

    Expected dataset format:
    [
        {
            "id": ...,
            "title": ...,
            "text": ...
        },
        ...
    ]
    """
    if not isinstance(dataset, list):
        raise TypeError("dataset must be a list of documents")

    chunked_data = []

    for doc_index, document in enumerate(dataset):
        if not isinstance(document, dict):
            continue

        doc_id = document.get("id", doc_index)
        title = document.get("title", "")
        text = document.get("text", "")

        chunks = chunk_text(text, chunk_size)

        for chunk_index, chunk in enumerate(chunks):
            chunked_data.append({
                "doc_id": doc_id,
                "title": title,
                "chunk_index": chunk_index,
                "chunk_text": chunk
            })

    return chunked_data


# TODO: Implement the `main` function to load data, chunk it, and print the results.
def main():
    file_name = "dataset.json"
    chunk_size = 100

    try:
        dataset = load_data(file_name)
        chunked_data = chunk_dataset(dataset, chunk_size)

        print("Chunked Data:")
        print(json.dumps(chunked_data, indent=2, ensure_ascii=False))

    except Exception as e:
        print(f"Error: {e}")


# TODO: Call the `main` function when the script is executed.
if __name__ == "__main__":
    main()
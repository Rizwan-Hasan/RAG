# RAG

RAG is a Python-based project that uses the FastAPI framework. It is designed to work with ChromaDB and uses HuggingFace's BgeEmbeddings for text embeddings and SemanticChunker for text splitting.

## Installation

You can install the required packages using pip:

```bash
pip install -r requirements.txt
```

## Usage

### Upload File

You can upload a file to the server using the following curl command:

```bash
curl --location 'http://localhost:8001/upload-file' \
--form 'pdf_files=@"/path/to/your/file.pdf"' \
--form 'collection_name="your_collection_name"'
```

Replace `"/path/to/your/file.pdf"` with the path to your file and `"your_collection_name"` with the name of your collection.

### Delete Collection

You can delete a collection using the following curl command:

```bash
curl --location --request DELETE 'http://localhost:8001/delete' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'collection_name=your_collection_name'
```

Replace `your_collection_name` with the name of the collection you want to delete.

### Query

You can make a query to the server using the following curl command:

```bash
curl --location 'http://localhost:8001/query' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--form 'question="your_question"' \
--form 'collection_name="your_collection_name"'
```

Replace `"your_question"` with your question and `"your_collection_name"` with the name of your collection.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](LICENSE)
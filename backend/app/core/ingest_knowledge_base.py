import os
import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv

# Force load variables
load_dotenv(override=True)

persist_dir = os.getenv("CHROMA_PERSIST_DIRECTORY", "./chroma_db")
collection_name = os.getenv("CHROMA_COLLECTION_NAME", "one_knowledge_base")

# Path to knowledge_base — it lives at backend/knowledge_base/,
# and this script is at backend/app/core/, so go up two levels.
KNOWLEDGE_BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../knowledge_base"))

def ingest_directory():
    print(f"Looking for markdown files in: {KNOWLEDGE_BASE_DIR}")
    
    if not os.path.exists(KNOWLEDGE_BASE_DIR):
        print("Error: Could not find the knowledge_base directory. Please check the path.")
        return

    # Initialize Chroma client
    client = chromadb.PersistentClient(path=persist_dir)
    sentence_transformer_ef = embedding_functions.DefaultEmbeddingFunction()
    collection = client.get_or_create_collection(
        name=collection_name,
        embedding_function=sentence_transformer_ef
    )

    documents = []
    metadatas = []
    ids = []

    # Walk through the directory and read all .md files
    for root, dirs, files in os.walk(KNOWLEDGE_BASE_DIR):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                category = os.path.basename(root) # e.g., 'compliance', 'engineering'
                
                # Read the file content
                with open(file_path, "r", encoding="utf-8") as f:
                    text_content = f.read()

                # Generate a clean title from the filename
                title = file.replace("-", " ").replace(".md", "").title()
                doc_id = f"{category}_{file}"

                documents.append(text_content)
                metadatas.append({
                    "category": category, 
                    "title": title, 
                    "source_file": file
                })
                ids.append(doc_id)

    if not documents:
        print("No .md files found to ingest.")
        return

    print(f"Found {len(documents)} files. Embedding and inserting into ChromaDB...")
    
    # Upsert into database
    collection.upsert(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )
    
    print(f"Successfully ingested {len(documents)} real documents into '{collection_name}'!")

if __name__ == "__main__":
    ingest_directory()

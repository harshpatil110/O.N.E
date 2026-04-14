import asyncio
import logging
import time
from dotenv import load_dotenv

load_dotenv()

from app.rag.rag_service import RAGService

# Set up basic logging for the script
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

async def test_retrieval():
    logger.info("Starting standalone RAG retrieval test...")
    try:
        # 1. Initialize the RAG service
        rag_service = RAGService()
        logger.info("Successfully connected to ChromaDB and initialized RAGService.")
        
        # 2. Define the test query
        query = "what node version do we use?"
        logger.info(f"Querying vector database with: '{query}'")
        
        # 3. Perform retrieval (bypassing the LLM entirely)
        start_time = time.time()
        results = await rag_service.retrieve(query=query, top_k=3)
        elapsed_time = time.time() - start_time
        
        logger.info(f"Retrieved {len(results)} chunks in {elapsed_time:.3f} seconds.\n")
        
        # 4. Iterate and print out the formatted matches
        if not results:
            logger.warning("No results found. The ChromaDB collection might be empty or threshold is too high.")
            return

        for i, chunk in enumerate(results, 1):
            score = chunk.get("similarity_score", 0.0)
            source = chunk.get("source", "Unknown Source")
            content = chunk.get("content", "").strip()
            title = chunk.get("title", "No Title")
            
            print(f"--- MATCH {i} ---")
            print(f"Title:  {title}")
            print(f"Source: {source}")
            print(f"Score:  {score:.4f} (Higher is better)")
            print(f"Content:\n{content}")
            print("-" * 50 + "\n")
            
    except Exception as e:
        logger.error(f"Failed to execute RAG retrieval: {e}", exc_info=True)

if __name__ == "__main__":
    # Execute the async workflow
    asyncio.run(test_retrieval())

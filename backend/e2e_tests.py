import asyncio
import os
import sys
from dotenv import load_dotenv

# Ensure app imports work
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(override=True)

async def test_phase_1():
    print("\n--- PHASE 1: RAG Engine & Data Integrity ---")
    from app.core.rag_tool import _build_hybrid_retriever, search_company_knowledge_base
    from langchain_chroma import Chroma
    from langchain_huggingface import HuggingFaceEmbeddings

    print("Test 1.1: Dense Search (ChromaDB direct)")
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )
    db = Chroma(collection_name="one_knowledge_base", persist_directory="./chroma_db", embedding_function=embeddings)
    results = db.similarity_search("PTO Policy", k=2)
    assert any("pto" in r.metadata.get("source", "").lower() for r in results) or any("PTO" in r.page_content for r in results), "Dense search failed to find PTO policy."
    print("Test 1.1 Passed!")

    print("Test 1.2: Sparse Search (BM25)")
    retriever = _build_hybrid_retriever() # Builds and returns ensemble. We can just test ensemble for the exact match.
    ensemble_results = retriever.invoke("docker-compose up -d")
    assert any("docker" in r.page_content.lower() for r in ensemble_results), "BM25 failed to find docker-compose snippet."
    print("Test 1.2 Passed!")

    print("Test 1.3: Tool Execution")
    res1 = search_company_knowledge_base.invoke("What is the PTO policy?")
    assert isinstance(res1, str), "Tool should return a formatted string"
    assert "--- Source" in res1, "Tool formatting is incorrect"
    
    # Empty query test (should handle gracefully)
    res_empty = search_company_knowledge_base.invoke("")
    assert isinstance(res_empty, str)
    print("Test 1.3 Passed!")

async def test_phase_2():
    print("\n--- PHASE 2: Hermes Agent & Backend Logic ---")
    from app.core.database import SessionLocal
    from app.models.onboarding_session import OnboardingSession
    from app.models.conversation_log import ConversationLog
    from app.core.security import create_access_token
    import requests
    
    db = SessionLocal()
    session = db.query(OnboardingSession).first()
    assert session, "No onboarding sessions in DB for testing."
    session_id = str(session.id)
    user_id = str(session.user_id)
    
    # Generate token for the test user
    token = create_access_token({"sub": user_id, "role": "developer"})
    headers = {"Authorization": f"Bearer {token}"}
    
    base_url = f"http://localhost:8000/api/v1/chat/{session_id}/message"

    # We can test the FastAPI endpoint directly via requests
    print("Test 2.1: Tool Binding (Greeting)")
    r1 = requests.post(base_url, json={"message": "Hi, who are you?"}, headers=headers)
    if r1.status_code != 200:
        print("Error Response 1:", r1.text)
    r1.raise_for_status()
    resp1 = r1.json()
    print("Agent Response 1:", resp1["content"])
    assert "Hermes" in resp1["content"] or len(resp1["content"]) > 10, "Failed to respond to greeting."
    print("Test 2.1 Passed!")

    print("Test 2.2: Agentic RAG")
    r2 = requests.post(base_url, json={"message": "Who is Harshvardhan Patil?"}, headers=headers)
    r2.raise_for_status()
    resp2 = r2.json()
    print("Agent Response 2:", resp2["content"])
    assert "Harshvardhan" in resp2["content"], "Agent did not answer correctly based on RAG."
    print("Test 2.2 Passed!")

    print("Test 2.3: Memory Persistence")
    # Verify DB logs
    logs = db.query(ConversationLog).filter_by(session_id=session_id).order_by(ConversationLog.created_at.desc()).limit(4).all()
    # The last 4 should be our two interactions (user, assistant, user, assistant)
    user_msgs = [l.content for l in logs if l.role == "user"]
    ai_msgs = [l.content for l in logs if l.role == "assistant"]
    assert "Who is Harshvardhan Patil?" in user_msgs, "Failed to persist user message."
    assert any("Harshvardhan" in a for a in ai_msgs), "Failed to persist AI message."
    print("Test 2.3 Passed!")

    print("Test 2.4: Context Recall")
    r3 = requests.post(base_url, json={"message": "What is his contact info or email?"}, headers=headers)
    r3.raise_for_status()
    resp3 = r3.json()
    print("Agent Response 3:", resp3["content"])
    assert "@" in resp3["content"] or "email" in resp3["content"].lower(), "Agent forgot context of 'his'."
    print("Test 2.4 Passed!")

if __name__ == "__main__":
    asyncio.run(test_phase_1())
    asyncio.run(test_phase_2())
    print("\nALL BACKEND TESTS PASSED.")

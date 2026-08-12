import os
from typing import List, Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langgraph.prebuilt import create_react_agent
from app.core.rag_tool import search_company_knowledge_base

def get_hermes_agent():
    """
    Initializes the Hermes LLM Supervisor agent with the Hybrid Search RAG tool.
    Returns a runnable graph.
    """
    api_key = os.getenv("NVIDIA_API_KEY", "dummy-key")
    
    # Initialize the LLM
    llm = ChatOpenAI(
        model="meta/llama-3.1-70b-instruct",
        api_key=api_key,
        base_url="https://integrate.api.nvidia.com/v1",
        temperature=0.2
    )

    # Bind the hybrid search tool to the LLM
    tools = [search_company_knowledge_base]
    
    # Create the agent using LangGraph's prebuilt react agent
    agent = create_react_agent(llm, tools)
    
    return agent

async def run_hermes_agent(message: str, history: List[Dict[str, str]]) -> str:
    """
    Runs the Hermes agent with the given message and conversation history.
    """
    agent = get_hermes_agent()
    
    # Build System Prompt
    system_prompt = SystemMessage(content="""You are Hermes, the primary AI onboarding mentor and supervisor for Nexus AI Innovations. 
Your job is to assist engineers with HR queries, tech stack setups, and system architecture. 
Always use the `search_company_knowledge_base` tool when asked about company-specific policies, code snippets, or setups. 
Do not guess or hallucinate. Keep your answers concise, accurate, and professional.""")
    
    # Convert history into LangChain messages
    chat_history = [system_prompt]
    for msg in history:
        if msg["role"] == "user":
            chat_history.append(HumanMessage(content=msg["content"]))
        elif msg["role"] == "assistant":
            chat_history.append(AIMessage(content=msg["content"]))
            
    # Add new message
    chat_history.append(HumanMessage(content=message))
            
    # Invoke the agent asynchronously
    result = await agent.ainvoke({"messages": chat_history})
    
    # The result contains the messages list with the final AI message at the end
    final_message = result["messages"][-1].content
    return final_message

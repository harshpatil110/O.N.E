import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.core.langgraph_agent import app_graph, tools, tool_node
from app.core.hermes_tool import delegate_to_hermes
from langchain_core.messages import HumanMessage

def test_integration():
    print("=" * 60)
    print("Testing Hermes Agent Integration in LangGraph")
    print("=" * 60)
    
    # 1. Verify Tool Registration
    tool_names = [t.name for t in tools]
    print(f"\n1. Registered tools in tools list: {tool_names}")
    assert "delegate_to_hermes" in tool_names, "delegate_to_hermes missing from tools!"
    
    node_tools = [t.name for t in tool_node.tools_by_name.values()]
    print(f"2. Registered tools in ToolNode: {node_tools}")
    assert "delegate_to_hermes" in node_tools, "delegate_to_hermes missing from ToolNode!"
    
    # 2. Direct Tool Call Test
    print("\n3. Testing direct Hermes tool invocation...")
    tool_result = delegate_to_hermes.invoke({"query": "Check Slack channels and Jira status"})
    print(f"Direct Tool Output: {tool_result[:180]}...")
    assert len(tool_result) > 0, "Empty tool result!"
    
    print("\n" + "=" * 60)
    print("All Hermes integration checks passed successfully!")
    print("=" * 60)

if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    test_integration()

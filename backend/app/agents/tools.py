AGENT_TOOLS = [
    {
        "name": "search_knowledge_base",
        "description": "Search the company knowledge base for relevant documentation to answer developer questions.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "The search query"},
                "category": {
                    "type": "string",
                    "enum": ["setup", "engineering", "compliance", "team", "company", "devops"],
                    "description": "Optional: filter by document category"
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "mark_checklist_item",
        "description": "Update the status of a checklist item when a developer completes, starts, or skips it.",
        "parameters": {
            "type": "object",
            "properties": {
                "item_id": {"type": "string"},
                "status": {"type": "string", "enum": ["completed", "in_progress", "skipped"]},
                "notes": {"type": "string", "description": "Optional notes about completion"}
            },
            "required": ["item_id", "status"]
        }
    },
    {
        "name": "get_checklist_status",
        "description": "Get the current checklist with all item statuses and progress percentage.",
        "parameters": {"type": "object", "properties": {}}
    },
    {
        "name": "send_hr_completion_email",
        "description": "Send the onboarding completion report to HR. Only call this after all required items are done AND the developer has confirmed they want to complete.",
        "parameters": {
            "type": "object",
            "properties": {
                "include_pending": {"type": "boolean", "description": "Include pending/skipped items in the report"}
            },
            "required": ["include_pending"]
        }
    },
    {
        "name": "escalate_to_human",
        "description": "Escalate to a human buddy or manager when the agent cannot answer a question.",
        "parameters": {
            "type": "object",
            "properties": {
                "reason": {"type": "string"},
                "channel": {"type": "string", "enum": ["email"]}
            },
            "required": ["reason", "channel"]
        }
    }
]

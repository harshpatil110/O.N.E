AGENT_TOOLS = [
    {
        "type": "function",
        "function": {
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
                "required": ["query"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "mark_checklist_item",
            "description": "Update the status of a checklist item when a developer completes, starts, or skips it.",
            "parameters": {
                "type": "object",
                "properties": {
                    "item_id": {"type": "string"},
                    "status": {"type": "string", "enum": ["completed", "in_progress", "skipped"]},
                    "notes": {"type": "string", "description": "Optional notes about completion"}
                },
                "required": ["item_id", "status"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "mark_task_complete",
            "description": (
                "Mark an onboarding task as complete by its title or category. "
                "Use this when the user says they have finished, completed, or done with a task. "
                "This finds the best matching pending task and marks it as completed."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "task_name": {
                        "type": "string",
                        "description": "The name or title of the task the user says they completed (e.g. 'security training', 'laptop setup')"
                    },
                    "task_category": {
                        "type": "string",
                        "description": "Optional: the category of the task (e.g. 'General', 'Access', 'Security', 'Development')"
                    }
                },
                "required": ["task_name"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_checklist_status",
            "description": "Get the current checklist with all item statuses and progress percentage.",
            "parameters": {"type": "object", "properties": {}, "additionalProperties": False}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "send_hr_completion_email",
            "description": "Send the onboarding completion report to HR. Only call this after all required items are done AND the developer has confirmed they want to complete.",
            "parameters": {
                "type": "object",
                "properties": {
                    "include_pending": {"type": "boolean", "description": "Include pending/skipped items in the report"}
                },
                "required": ["include_pending"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "escalate_to_human",
            "description": "Escalate to a human buddy or manager when the agent cannot answer a question.",
            "parameters": {
                "type": "object",
                "properties": {
                    "reason": {"type": "string"},
                    "channel": {"type": "string", "enum": ["email"]}
                },
                "required": ["reason", "channel"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "send_onboarding_email",
            "description": "Send a welcome onboarding email to the developer with their next steps.",
            "parameters": {
                "type": "object",
                "properties": {
                    "recipient_name": {"type": "string", "description": "The full name of the developer"},
                    "recipient_email": {"type": "string", "description": "The email address of the developer"}
                },
                "required": ["recipient_name", "recipient_email"],
                "additionalProperties": False
            }
        }
    }
]

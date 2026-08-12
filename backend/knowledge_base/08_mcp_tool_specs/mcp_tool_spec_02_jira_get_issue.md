    # MCP Tool Specification: `jira_get_issue`

    ## Integration
    **Jira** (via Model Context Protocol)

    ## Description
    Retrieves a Jira issue by key.

    ## Tool Registration
    ```python
    @tool("jira_get_issue")
    def jira_get_issue(**kwargs) -> dict:
        """Retrieves a Jira issue by key."""
        ...
    ```

    ## Input Schema
    | Parameter | Type |
    |-----------|------|
    | `issue_key` | `str` |

    ### Example Input
    ```json
{
    "issue_key": "<str>"
}
    ```

    ## Output Schema
    | Field | Type |
    |-------|------|
    | `key` | `str` |
| `summary` | `str` |
| `status` | `str` |
| `assignee` | `str` |
| `description` | `str` |

    ### Example Output
    ```json
{
    "key": "<str>",
    "summary": "<str>",
    "status": "<str>",
    "assignee": "<str>",
    "description": "<str>"
}
    ```

    ## Error Handling
    | Code | Description |
    |------|-------------|
    | `401` | Authentication failed — invalid or expired PAT/API token. |
| `500` | Internal server error on the external service. |
| `403` | Insufficient permissions for the requested operation. |
| `404` | Resource not found (invalid key, repo, or PR number). |

    ## Usage Context
    This tool is invoked by the **Hermes Supervisor Agent** when the
    user's intent matches a `jira` operation. The
    agent orchestrator passes the structured arguments and receives
    the response for inclusion in the chat reply.

    ## Permissions
    * Requires a valid **Jira API Token** configured in the backend environment.
    * The token must have the following scopes:
      * `read:jira-work`, `write:jira-work`

    ---
    *MCP Tool Documentation — Nexus AI Innovations — Spec #02*

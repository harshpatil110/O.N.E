    # MCP Tool Specification: `jira_create_issue`

    ## Integration
    **Jira** (via Model Context Protocol)

    ## Description
    Creates a new issue in Jira Cloud.

    ## Tool Registration
    ```python
    @tool("jira_create_issue")
    def jira_create_issue(**kwargs) -> dict:
        """Creates a new issue in Jira Cloud."""
        ...
    ```

    ## Input Schema
    | Parameter | Type |
    |-----------|------|
    | `project_key` | `str` |
| `summary` | `str` |
| `description` | `str` |
| `issue_type` | `str (Task|Bug|Story)` |
| `assignee_email` | `str (optional)` |

    ### Example Input
    ```json
{
    "project_key": "<str>",
    "summary": "<str>",
    "description": "<str>",
    "issue_type": "<str (Task|Bug|Story)>",
    "assignee_email": "<str (optional)>"
}
    ```

    ## Output Schema
    | Field | Type |
    |-------|------|
    | `issue_key` | `str` |
| `url` | `str` |
| `status` | `str` |

    ### Example Output
    ```json
{
    "issue_key": "<str>",
    "url": "<str>",
    "status": "<str>"
}
    ```

    ## Error Handling
    | Code | Description |
    |------|-------------|
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
    *MCP Tool Documentation — Nexus AI Innovations — Spec #01*

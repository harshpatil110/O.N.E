    # MCP Tool Specification: `jira_assign_issue`

    ## Integration
    **Jira** (via Model Context Protocol)

    ## Description
    Assigns a Jira issue to a user.

    ## Tool Registration
    ```python
    @tool("jira_assign_issue")
    def jira_assign_issue(**kwargs) -> dict:
        """Assigns a Jira issue to a user."""
        ...
    ```

    ## Input Schema
    | Parameter | Type |
    |-----------|------|
    | `issue_key` | `str` |
| `assignee_email` | `str` |

    ### Example Input
    ```json
{
    "issue_key": "<str>",
    "assignee_email": "<str>"
}
    ```

    ## Output Schema
    | Field | Type |
    |-------|------|
    | `success` | `bool` |

    ### Example Output
    ```json
{
    "success": "<bool>"
}
    ```

    ## Error Handling
    | Code | Description |
    |------|-------------|
    | `403` | Insufficient permissions for the requested operation. |
| `500` | Internal server error on the external service. |

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
    *MCP Tool Documentation — Nexus AI Innovations — Spec #08*

    # MCP Tool Specification: `jira_transition_issue`

    ## Integration
    **Jira** (via Model Context Protocol)

    ## Description
    Transitions a Jira issue to a new status.

    ## Tool Registration
    ```python
    @tool("jira_transition_issue")
    def jira_transition_issue(**kwargs) -> dict:
        """Transitions a Jira issue to a new status."""
        ...
    ```

    ## Input Schema
    | Parameter | Type |
    |-----------|------|
    | `issue_key` | `str` |
| `target_status` | `str (To Do|In Progress|Done)` |

    ### Example Input
    ```json
{
    "issue_key": "<str>",
    "target_status": "<str (To Do|In Progress|Done)>"
}
    ```

    ## Output Schema
    | Field | Type |
    |-------|------|
    | `success` | `bool` |
| `new_status` | `str` |

    ### Example Output
    ```json
{
    "success": "<bool>",
    "new_status": "<str>"
}
    ```

    ## Error Handling
    | Code | Description |
    |------|-------------|
    | `401` | Authentication failed — invalid or expired PAT/API token. |
| `429` | Rate limit exceeded — retry after cooldown period. |

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
    *MCP Tool Documentation — Nexus AI Innovations — Spec #03*

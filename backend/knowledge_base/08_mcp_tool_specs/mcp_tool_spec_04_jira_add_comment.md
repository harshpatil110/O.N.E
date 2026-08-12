    # MCP Tool Specification: `jira_add_comment`

    ## Integration
    **Jira** (via Model Context Protocol)

    ## Description
    Adds a comment to a Jira issue.

    ## Tool Registration
    ```python
    @tool("jira_add_comment")
    def jira_add_comment(**kwargs) -> dict:
        """Adds a comment to a Jira issue."""
        ...
    ```

    ## Input Schema
    | Parameter | Type |
    |-----------|------|
    | `issue_key` | `str` |
| `body` | `str` |

    ### Example Input
    ```json
{
    "issue_key": "<str>",
    "body": "<str>"
}
    ```

    ## Output Schema
    | Field | Type |
    |-------|------|
    | `comment_id` | `str` |
| `created` | `datetime` |

    ### Example Output
    ```json
{
    "comment_id": "<str>",
    "created": "<datetime>"
}
    ```

    ## Error Handling
    | Code | Description |
    |------|-------------|
    | `500` | Internal server error on the external service. |
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
    *MCP Tool Documentation — Nexus AI Innovations — Spec #04*

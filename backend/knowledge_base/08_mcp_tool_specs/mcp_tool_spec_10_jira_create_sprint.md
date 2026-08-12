    # MCP Tool Specification: `jira_create_sprint`

    ## Integration
    **Jira** (via Model Context Protocol)

    ## Description
    Creates a new sprint on a board.

    ## Tool Registration
    ```python
    @tool("jira_create_sprint")
    def jira_create_sprint(**kwargs) -> dict:
        """Creates a new sprint on a board."""
        ...
    ```

    ## Input Schema
    | Parameter | Type |
    |-----------|------|
    | `board_id` | `int` |
| `name` | `str` |
| `start_date` | `str` |
| `end_date` | `str` |

    ### Example Input
    ```json
{
    "board_id": "<int>",
    "name": "<str>",
    "start_date": "<str>",
    "end_date": "<str>"
}
    ```

    ## Output Schema
    | Field | Type |
    |-------|------|
    | `sprint_id` | `int` |
| `state` | `str` |

    ### Example Output
    ```json
{
    "sprint_id": "<int>",
    "state": "<str>"
}
    ```

    ## Error Handling
    | Code | Description |
    |------|-------------|
    | `403` | Insufficient permissions for the requested operation. |
| `404` | Resource not found (invalid key, repo, or PR number). |
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
    *MCP Tool Documentation — Nexus AI Innovations — Spec #10*

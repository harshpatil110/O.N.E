    # MCP Tool Specification: `jira_get_sprint`

    ## Integration
    **Jira** (via Model Context Protocol)

    ## Description
    Gets the active sprint for a board.

    ## Tool Registration
    ```python
    @tool("jira_get_sprint")
    def jira_get_sprint(**kwargs) -> dict:
        """Gets the active sprint for a board."""
        ...
    ```

    ## Input Schema
    | Parameter | Type |
    |-----------|------|
    | `board_id` | `int` |

    ### Example Input
    ```json
{
    "board_id": "<int>"
}
    ```

    ## Output Schema
    | Field | Type |
    |-------|------|
    | `sprint_id` | `int` |
| `name` | `str` |
| `start_date` | `str` |
| `end_date` | `str` |
| `issues` | `list` |

    ### Example Output
    ```json
{
    "sprint_id": "<int>",
    "name": "<str>",
    "start_date": "<str>",
    "end_date": "<str>",
    "issues": "<list>"
}
    ```

    ## Error Handling
    | Code | Description |
    |------|-------------|
    | `500` | Internal server error on the external service. |
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
    *MCP Tool Documentation — Nexus AI Innovations — Spec #05*

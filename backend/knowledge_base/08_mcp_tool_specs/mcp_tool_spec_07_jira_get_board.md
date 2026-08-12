    # MCP Tool Specification: `jira_get_board`

    ## Integration
    **Jira** (via Model Context Protocol)

    ## Description
    Gets board configuration and columns.

    ## Tool Registration
    ```python
    @tool("jira_get_board")
    def jira_get_board(**kwargs) -> dict:
        """Gets board configuration and columns."""
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
    | `id` | `int` |
| `name` | `str` |
| `type` | `str` |
| `columns` | `list` |

    ### Example Output
    ```json
{
    "id": "<int>",
    "name": "<str>",
    "type": "<str>",
    "columns": "<list>"
}
    ```

    ## Error Handling
    | Code | Description |
    |------|-------------|
    | `401` | Authentication failed — invalid or expired PAT/API token. |
| `403` | Insufficient permissions for the requested operation. |
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
    *MCP Tool Documentation — Nexus AI Innovations — Spec #07*

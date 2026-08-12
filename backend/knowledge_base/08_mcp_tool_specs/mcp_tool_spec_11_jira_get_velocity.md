    # MCP Tool Specification: `jira_get_velocity`

    ## Integration
    **Jira** (via Model Context Protocol)

    ## Description
    Gets sprint velocity metrics.

    ## Tool Registration
    ```python
    @tool("jira_get_velocity")
    def jira_get_velocity(**kwargs) -> dict:
        """Gets sprint velocity metrics."""
        ...
    ```

    ## Input Schema
    | Parameter | Type |
    |-----------|------|
    | `board_id` | `int` |
| `num_sprints` | `int (default 5)` |

    ### Example Input
    ```json
{
    "board_id": "<int>",
    "num_sprints": "<int (default 5)>"
}
    ```

    ## Output Schema
    | Field | Type |
    |-------|------|
    | `sprints` | `list` |
| `avg_velocity` | `float` |

    ### Example Output
    ```json
{
    "sprints": "<list>",
    "avg_velocity": "<float>"
}
    ```

    ## Error Handling
    | Code | Description |
    |------|-------------|
    | `500` | Internal server error on the external service. |
| `429` | Rate limit exceeded — retry after cooldown period. |
| `401` | Authentication failed — invalid or expired PAT/API token. |

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
    *MCP Tool Documentation — Nexus AI Innovations — Spec #11*

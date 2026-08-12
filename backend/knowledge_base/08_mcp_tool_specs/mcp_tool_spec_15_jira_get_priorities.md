    # MCP Tool Specification: `jira_get_priorities`

    ## Integration
    **Jira** (via Model Context Protocol)

    ## Description
    Lists all available priority levels.

    ## Tool Registration
    ```python
    @tool("jira_get_priorities")
    def jira_get_priorities(**kwargs) -> dict:
        """Lists all available priority levels."""
        ...
    ```

    ## Input Schema
    | Parameter | Type |
    |-----------|------|


    ### Example Input
    ```json
{

}
    ```

    ## Output Schema
    | Field | Type |
    |-------|------|
    | `priorities` | `list[Priority]` |

    ### Example Output
    ```json
{
    "priorities": "<list[Priority]>"
}
    ```

    ## Error Handling
    | Code | Description |
    |------|-------------|
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
    *MCP Tool Documentation — Nexus AI Innovations — Spec #15*

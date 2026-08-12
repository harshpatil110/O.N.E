    # MCP Tool Specification: `jira_link_issues`

    ## Integration
    **Jira** (via Model Context Protocol)

    ## Description
    Creates a link between two Jira issues.

    ## Tool Registration
    ```python
    @tool("jira_link_issues")
    def jira_link_issues(**kwargs) -> dict:
        """Creates a link between two Jira issues."""
        ...
    ```

    ## Input Schema
    | Parameter | Type |
    |-----------|------|
    | `inward_key` | `str` |
| `outward_key` | `str` |
| `link_type` | `str` |

    ### Example Input
    ```json
{
    "inward_key": "<str>",
    "outward_key": "<str>",
    "link_type": "<str>"
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
    | `404` | Resource not found (invalid key, repo, or PR number). |
| `429` | Rate limit exceeded — retry after cooldown period. |
| `403` | Insufficient permissions for the requested operation. |

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
    *MCP Tool Documentation — Nexus AI Innovations — Spec #14*

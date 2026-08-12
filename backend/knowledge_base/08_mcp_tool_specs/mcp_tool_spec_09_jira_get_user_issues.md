    # MCP Tool Specification: `jira_get_user_issues`

    ## Integration
    **Jira** (via Model Context Protocol)

    ## Description
    Gets all issues assigned to a user.

    ## Tool Registration
    ```python
    @tool("jira_get_user_issues")
    def jira_get_user_issues(**kwargs) -> dict:
        """Gets all issues assigned to a user."""
        ...
    ```

    ## Input Schema
    | Parameter | Type |
    |-----------|------|
    | `email` | `str` |
| `status_filter` | `str (optional)` |

    ### Example Input
    ```json
{
    "email": "<str>",
    "status_filter": "<str (optional)>"
}
    ```

    ## Output Schema
    | Field | Type |
    |-------|------|
    | `issues` | `list[Issue]` |

    ### Example Output
    ```json
{
    "issues": "<list[Issue]>"
}
    ```

    ## Error Handling
    | Code | Description |
    |------|-------------|
    | `404` | Resource not found (invalid key, repo, or PR number). |
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
    *MCP Tool Documentation — Nexus AI Innovations — Spec #09*

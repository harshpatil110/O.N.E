    # MCP Tool Specification: `jira_search_issues`

    ## Integration
    **Jira** (via Model Context Protocol)

    ## Description
    Searches issues using JQL query.

    ## Tool Registration
    ```python
    @tool("jira_search_issues")
    def jira_search_issues(**kwargs) -> dict:
        """Searches issues using JQL query."""
        ...
    ```

    ## Input Schema
    | Parameter | Type |
    |-----------|------|
    | `jql` | `str` |
| `max_results` | `int (default 50)` |

    ### Example Input
    ```json
{
    "jql": "<str>",
    "max_results": "<int (default 50)>"
}
    ```

    ## Output Schema
    | Field | Type |
    |-------|------|
    | `issues` | `list[Issue]` |
| `total` | `int` |

    ### Example Output
    ```json
{
    "issues": "<list[Issue]>",
    "total": "<int>"
}
    ```

    ## Error Handling
    | Code | Description |
    |------|-------------|
    | `403` | Insufficient permissions for the requested operation. |
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
    *MCP Tool Documentation — Nexus AI Innovations — Spec #06*

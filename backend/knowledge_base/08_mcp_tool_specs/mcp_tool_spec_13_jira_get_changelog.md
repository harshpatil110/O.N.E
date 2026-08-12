    # MCP Tool Specification: `jira_get_changelog`

    ## Integration
    **Jira** (via Model Context Protocol)

    ## Description
    Gets the change history for an issue.

    ## Tool Registration
    ```python
    @tool("jira_get_changelog")
    def jira_get_changelog(**kwargs) -> dict:
        """Gets the change history for an issue."""
        ...
    ```

    ## Input Schema
    | Parameter | Type |
    |-----------|------|
    | `issue_key` | `str` |

    ### Example Input
    ```json
{
    "issue_key": "<str>"
}
    ```

    ## Output Schema
    | Field | Type |
    |-------|------|
    | `changelog` | `list[ChangeEntry]` |

    ### Example Output
    ```json
{
    "changelog": "<list[ChangeEntry]>"
}
    ```

    ## Error Handling
    | Code | Description |
    |------|-------------|
    | `404` | Resource not found (invalid key, repo, or PR number). |
| `500` | Internal server error on the external service. |
| `401` | Authentication failed — invalid or expired PAT/API token. |
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
    *MCP Tool Documentation — Nexus AI Innovations — Spec #13*

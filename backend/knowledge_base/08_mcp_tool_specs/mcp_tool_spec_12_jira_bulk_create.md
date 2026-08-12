    # MCP Tool Specification: `jira_bulk_create`

    ## Integration
    **Jira** (via Model Context Protocol)

    ## Description
    Creates multiple Jira issues in batch.

    ## Tool Registration
    ```python
    @tool("jira_bulk_create")
    def jira_bulk_create(**kwargs) -> dict:
        """Creates multiple Jira issues in batch."""
        ...
    ```

    ## Input Schema
    | Parameter | Type |
    |-----------|------|
    | `issues` | `list[IssueInput]` |

    ### Example Input
    ```json
{
    "issues": "<list[IssueInput]>"
}
    ```

    ## Output Schema
    | Field | Type |
    |-------|------|
    | `created` | `list[str]` |
| `errors` | `list` |

    ### Example Output
    ```json
{
    "created": "<list[str]>",
    "errors": "<list>"
}
    ```

    ## Error Handling
    | Code | Description |
    |------|-------------|
    | `403` | Insufficient permissions for the requested operation. |
| `429` | Rate limit exceeded — retry after cooldown period. |
| `401` | Authentication failed — invalid or expired PAT/API token. |
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
    *MCP Tool Documentation — Nexus AI Innovations — Spec #12*

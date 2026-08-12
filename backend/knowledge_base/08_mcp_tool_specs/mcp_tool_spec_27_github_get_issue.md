    # MCP Tool Specification: `github_get_issue`

    ## Integration
    **GitHub** (via Model Context Protocol)

    ## Description
    Gets a GitHub issue by number.

    ## Tool Registration
    ```python
    @tool("github_get_issue")
    def github_get_issue(**kwargs) -> dict:
        """Gets a GitHub issue by number."""
        ...
    ```

    ## Input Schema
    | Parameter | Type |
    |-----------|------|
    | `owner` | `str` |
| `repo` | `str` |
| `issue_number` | `int` |

    ### Example Input
    ```json
{
    "owner": "<str>",
    "repo": "<str>",
    "issue_number": "<int>"
}
    ```

    ## Output Schema
    | Field | Type |
    |-------|------|
    | `title` | `str` |
| `state` | `str` |
| `body` | `str` |
| `labels` | `list` |

    ### Example Output
    ```json
{
    "title": "<str>",
    "state": "<str>",
    "body": "<str>",
    "labels": "<list>"
}
    ```

    ## Error Handling
    | Code | Description |
    |------|-------------|
    | `403` | Insufficient permissions for the requested operation. |
| `404` | Resource not found (invalid key, repo, or PR number). |
| `500` | Internal server error on the external service. |
| `401` | Authentication failed — invalid or expired PAT/API token. |

    ## Usage Context
    This tool is invoked by the **Hermes Supervisor Agent** when the
    user's intent matches a `github` operation. The
    agent orchestrator passes the structured arguments and receives
    the response for inclusion in the chat reply.

    ## Permissions
    * Requires a valid **GitHub Personal Access Token (PAT)** configured in the backend environment.
    * The token must have the following scopes:
      * `repo`, `read:org`, `workflow`

    ---
    *MCP Tool Documentation — Nexus AI Innovations — Spec #27*

    # MCP Tool Specification: `github_create_issue`

    ## Integration
    **GitHub** (via Model Context Protocol)

    ## Description
    Creates a new GitHub issue.

    ## Tool Registration
    ```python
    @tool("github_create_issue")
    def github_create_issue(**kwargs) -> dict:
        """Creates a new GitHub issue."""
        ...
    ```

    ## Input Schema
    | Parameter | Type |
    |-----------|------|
    | `owner` | `str` |
| `repo` | `str` |
| `title` | `str` |
| `body` | `str` |
| `labels` | `list[str]` |

    ### Example Input
    ```json
{
    "owner": "<str>",
    "repo": "<str>",
    "title": "<str>",
    "body": "<str>",
    "labels": "<list[str]>"
}
    ```

    ## Output Schema
    | Field | Type |
    |-------|------|
    | `issue_number` | `int` |
| `url` | `str` |

    ### Example Output
    ```json
{
    "issue_number": "<int>",
    "url": "<str>"
}
    ```

    ## Error Handling
    | Code | Description |
    |------|-------------|
    | `500` | Internal server error on the external service. |
| `404` | Resource not found (invalid key, repo, or PR number). |

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
    *MCP Tool Documentation — Nexus AI Innovations — Spec #26*

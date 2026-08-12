    # MCP Tool Specification: `github_get_pr`

    ## Integration
    **GitHub** (via Model Context Protocol)

    ## Description
    Gets details of a specific pull request.

    ## Tool Registration
    ```python
    @tool("github_get_pr")
    def github_get_pr(**kwargs) -> dict:
        """Gets details of a specific pull request."""
        ...
    ```

    ## Input Schema
    | Parameter | Type |
    |-----------|------|
    | `owner` | `str` |
| `repo` | `str` |
| `pr_number` | `int` |

    ### Example Input
    ```json
{
    "owner": "<str>",
    "repo": "<str>",
    "pr_number": "<int>"
}
    ```

    ## Output Schema
    | Field | Type |
    |-------|------|
    | `title` | `str` |
| `state` | `str` |
| `author` | `str` |
| `reviewers` | `list` |
| `diff_url` | `str` |

    ### Example Output
    ```json
{
    "title": "<str>",
    "state": "<str>",
    "author": "<str>",
    "reviewers": "<list>",
    "diff_url": "<str>"
}
    ```

    ## Error Handling
    | Code | Description |
    |------|-------------|
    | `404` | Resource not found (invalid key, repo, or PR number). |
| `500` | Internal server error on the external service. |
| `429` | Rate limit exceeded — retry after cooldown period. |

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
    *MCP Tool Documentation — Nexus AI Innovations — Spec #19*

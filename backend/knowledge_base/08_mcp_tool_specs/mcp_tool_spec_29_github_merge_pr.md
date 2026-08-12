    # MCP Tool Specification: `github_merge_pr`

    ## Integration
    **GitHub** (via Model Context Protocol)

    ## Description
    Merges a pull request.

    ## Tool Registration
    ```python
    @tool("github_merge_pr")
    def github_merge_pr(**kwargs) -> dict:
        """Merges a pull request."""
        ...
    ```

    ## Input Schema
    | Parameter | Type |
    |-----------|------|
    | `owner` | `str` |
| `repo` | `str` |
| `pr_number` | `int` |
| `merge_method` | `str (squash|merge|rebase)` |

    ### Example Input
    ```json
{
    "owner": "<str>",
    "repo": "<str>",
    "pr_number": "<int>",
    "merge_method": "<str (squash|merge|rebase)>"
}
    ```

    ## Output Schema
    | Field | Type |
    |-------|------|
    | `merged` | `bool` |
| `sha` | `str` |

    ### Example Output
    ```json
{
    "merged": "<bool>",
    "sha": "<str>"
}
    ```

    ## Error Handling
    | Code | Description |
    |------|-------------|
    | `429` | Rate limit exceeded — retry after cooldown period. |
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
    *MCP Tool Documentation — Nexus AI Innovations — Spec #29*

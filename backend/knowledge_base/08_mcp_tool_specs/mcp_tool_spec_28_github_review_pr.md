    # MCP Tool Specification: `github_review_pr`

    ## Integration
    **GitHub** (via Model Context Protocol)

    ## Description
    Submits a review on a pull request.

    ## Tool Registration
    ```python
    @tool("github_review_pr")
    def github_review_pr(**kwargs) -> dict:
        """Submits a review on a pull request."""
        ...
    ```

    ## Input Schema
    | Parameter | Type |
    |-----------|------|
    | `owner` | `str` |
| `repo` | `str` |
| `pr_number` | `int` |
| `body` | `str` |
| `event` | `str (APPROVE|REQUEST_CHANGES|COMMENT)` |

    ### Example Input
    ```json
{
    "owner": "<str>",
    "repo": "<str>",
    "pr_number": "<int>",
    "body": "<str>",
    "event": "<str (APPROVE|REQUEST_CHANGES|COMMENT)>"
}
    ```

    ## Output Schema
    | Field | Type |
    |-------|------|
    | `review_id` | `int` |

    ### Example Output
    ```json
{
    "review_id": "<int>"
}
    ```

    ## Error Handling
    | Code | Description |
    |------|-------------|
    | `429` | Rate limit exceeded — retry after cooldown period. |
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
    *MCP Tool Documentation — Nexus AI Innovations — Spec #28*

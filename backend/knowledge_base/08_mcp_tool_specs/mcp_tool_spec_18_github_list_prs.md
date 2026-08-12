    # MCP Tool Specification: `github_list_prs`

    ## Integration
    **GitHub** (via Model Context Protocol)

    ## Description
    Lists pull requests for a repository.

    ## Tool Registration
    ```python
    @tool("github_list_prs")
    def github_list_prs(**kwargs) -> dict:
        """Lists pull requests for a repository."""
        ...
    ```

    ## Input Schema
    | Parameter | Type |
    |-----------|------|
    | `owner` | `str` |
| `repo` | `str` |
| `state` | `str (open|closed|all)` |

    ### Example Input
    ```json
{
    "owner": "<str>",
    "repo": "<str>",
    "state": "<str (open|closed|all)>"
}
    ```

    ## Output Schema
    | Field | Type |
    |-------|------|
    | `pull_requests` | `list[PR]` |

    ### Example Output
    ```json
{
    "pull_requests": "<list[PR]>"
}
    ```

    ## Error Handling
    | Code | Description |
    |------|-------------|
    | `429` | Rate limit exceeded — retry after cooldown period. |
| `401` | Authentication failed — invalid or expired PAT/API token. |
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
    *MCP Tool Documentation — Nexus AI Innovations — Spec #18*

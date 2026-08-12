    # MCP Tool Specification: `github_list_branches`

    ## Integration
    **GitHub** (via Model Context Protocol)

    ## Description
    Lists branches in a repository.

    ## Tool Registration
    ```python
    @tool("github_list_branches")
    def github_list_branches(**kwargs) -> dict:
        """Lists branches in a repository."""
        ...
    ```

    ## Input Schema
    | Parameter | Type |
    |-----------|------|
    | `owner` | `str` |
| `repo` | `str` |

    ### Example Input
    ```json
{
    "owner": "<str>",
    "repo": "<str>"
}
    ```

    ## Output Schema
    | Field | Type |
    |-------|------|
    | `branches` | `list[Branch]` |

    ### Example Output
    ```json
{
    "branches": "<list[Branch]>"
}
    ```

    ## Error Handling
    | Code | Description |
    |------|-------------|
    | `500` | Internal server error on the external service. |
| `404` | Resource not found (invalid key, repo, or PR number). |
| `401` | Authentication failed — invalid or expired PAT/API token. |
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
    *MCP Tool Documentation — Nexus AI Innovations — Spec #21*

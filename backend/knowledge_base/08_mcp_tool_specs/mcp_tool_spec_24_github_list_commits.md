    # MCP Tool Specification: `github_list_commits`

    ## Integration
    **GitHub** (via Model Context Protocol)

    ## Description
    Lists recent commits on a branch.

    ## Tool Registration
    ```python
    @tool("github_list_commits")
    def github_list_commits(**kwargs) -> dict:
        """Lists recent commits on a branch."""
        ...
    ```

    ## Input Schema
    | Parameter | Type |
    |-----------|------|
    | `owner` | `str` |
| `repo` | `str` |
| `branch` | `str (optional)` |
| `limit` | `int (default 20)` |

    ### Example Input
    ```json
{
    "owner": "<str>",
    "repo": "<str>",
    "branch": "<str (optional)>",
    "limit": "<int (default 20)>"
}
    ```

    ## Output Schema
    | Field | Type |
    |-------|------|
    | `commits` | `list[Commit]` |

    ### Example Output
    ```json
{
    "commits": "<list[Commit]>"
}
    ```

    ## Error Handling
    | Code | Description |
    |------|-------------|
    | `429` | Rate limit exceeded — retry after cooldown period. |
| `403` | Insufficient permissions for the requested operation. |

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
    *MCP Tool Documentation — Nexus AI Innovations — Spec #24*

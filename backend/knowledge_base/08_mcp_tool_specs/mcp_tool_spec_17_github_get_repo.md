    # MCP Tool Specification: `github_get_repo`

    ## Integration
    **GitHub** (via Model Context Protocol)

    ## Description
    Gets repository details.

    ## Tool Registration
    ```python
    @tool("github_get_repo")
    def github_get_repo(**kwargs) -> dict:
        """Gets repository details."""
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
    | `name` | `str` |
| `description` | `str` |
| `default_branch` | `str` |
| `open_issues` | `int` |

    ### Example Output
    ```json
{
    "name": "<str>",
    "description": "<str>",
    "default_branch": "<str>",
    "open_issues": "<int>"
}
    ```

    ## Error Handling
    | Code | Description |
    |------|-------------|
    | `429` | Rate limit exceeded — retry after cooldown period. |
| `403` | Insufficient permissions for the requested operation. |
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
    *MCP Tool Documentation — Nexus AI Innovations — Spec #17*

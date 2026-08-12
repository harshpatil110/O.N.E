    # MCP Tool Specification: `github_get_collaborators`

    ## Integration
    **GitHub** (via Model Context Protocol)

    ## Description
    Lists collaborators for a repository.

    ## Tool Registration
    ```python
    @tool("github_get_collaborators")
    def github_get_collaborators(**kwargs) -> dict:
        """Lists collaborators for a repository."""
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
    | `collaborators` | `list[User]` |

    ### Example Output
    ```json
{
    "collaborators": "<list[User]>"
}
    ```

    ## Error Handling
    | Code | Description |
    |------|-------------|
    | `403` | Insufficient permissions for the requested operation. |
| `429` | Rate limit exceeded — retry after cooldown period. |
| `404` | Resource not found (invalid key, repo, or PR number). |
| `500` | Internal server error on the external service. |

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
    *MCP Tool Documentation — Nexus AI Innovations — Spec #30*

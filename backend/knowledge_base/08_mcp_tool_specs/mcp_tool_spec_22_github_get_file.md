    # MCP Tool Specification: `github_get_file`

    ## Integration
    **GitHub** (via Model Context Protocol)

    ## Description
    Gets the content of a file from a repo.

    ## Tool Registration
    ```python
    @tool("github_get_file")
    def github_get_file(**kwargs) -> dict:
        """Gets the content of a file from a repo."""
        ...
    ```

    ## Input Schema
    | Parameter | Type |
    |-----------|------|
    | `owner` | `str` |
| `repo` | `str` |
| `path` | `str` |
| `ref` | `str (optional)` |

    ### Example Input
    ```json
{
    "owner": "<str>",
    "repo": "<str>",
    "path": "<str>",
    "ref": "<str (optional)>"
}
    ```

    ## Output Schema
    | Field | Type |
    |-------|------|
    | `content` | `str` |
| `sha` | `str` |
| `encoding` | `str` |

    ### Example Output
    ```json
{
    "content": "<str>",
    "sha": "<str>",
    "encoding": "<str>"
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
    *MCP Tool Documentation — Nexus AI Innovations — Spec #22*

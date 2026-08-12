    # MCP Tool Specification: `github_create_pr`

    ## Integration
    **GitHub** (via Model Context Protocol)

    ## Description
    Creates a new pull request.

    ## Tool Registration
    ```python
    @tool("github_create_pr")
    def github_create_pr(**kwargs) -> dict:
        """Creates a new pull request."""
        ...
    ```

    ## Input Schema
    | Parameter | Type |
    |-----------|------|
    | `owner` | `str` |
| `repo` | `str` |
| `title` | `str` |
| `body` | `str` |
| `head` | `str` |
| `base` | `str` |

    ### Example Input
    ```json
{
    "owner": "<str>",
    "repo": "<str>",
    "title": "<str>",
    "body": "<str>",
    "head": "<str>",
    "base": "<str>"
}
    ```

    ## Output Schema
    | Field | Type |
    |-------|------|
    | `pr_number` | `int` |
| `url` | `str` |

    ### Example Output
    ```json
{
    "pr_number": "<int>",
    "url": "<str>"
}
    ```

    ## Error Handling
    | Code | Description |
    |------|-------------|
    | `404` | Resource not found (invalid key, repo, or PR number). |
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
    *MCP Tool Documentation — Nexus AI Innovations — Spec #20*

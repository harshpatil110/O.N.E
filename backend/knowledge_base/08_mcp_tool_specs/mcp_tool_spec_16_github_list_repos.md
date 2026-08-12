    # MCP Tool Specification: `github_list_repos`

    ## Integration
    **GitHub** (via Model Context Protocol)

    ## Description
    Lists repositories in the organization.

    ## Tool Registration
    ```python
    @tool("github_list_repos")
    def github_list_repos(**kwargs) -> dict:
        """Lists repositories in the organization."""
        ...
    ```

    ## Input Schema
    | Parameter | Type |
    |-----------|------|
    | `org` | `str (default nexusai)` |

    ### Example Input
    ```json
{
    "org": "<str (default nexusai)>"
}
    ```

    ## Output Schema
    | Field | Type |
    |-------|------|
    | `repos` | `list[Repo]` |

    ### Example Output
    ```json
{
    "repos": "<list[Repo]>"
}
    ```

    ## Error Handling
    | Code | Description |
    |------|-------------|
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
    *MCP Tool Documentation — Nexus AI Innovations — Spec #16*

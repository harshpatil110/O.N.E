    # MCP Tool Specification: `github_search_code`

    ## Integration
    **GitHub** (via Model Context Protocol)

    ## Description
    Searches for code across repositories.

    ## Tool Registration
    ```python
    @tool("github_search_code")
    def github_search_code(**kwargs) -> dict:
        """Searches for code across repositories."""
        ...
    ```

    ## Input Schema
    | Parameter | Type |
    |-----------|------|
    | `query` | `str` |
| `org` | `str (optional)` |

    ### Example Input
    ```json
{
    "query": "<str>",
    "org": "<str (optional)>"
}
    ```

    ## Output Schema
    | Field | Type |
    |-------|------|
    | `results` | `list[CodeResult]` |
| `total` | `int` |

    ### Example Output
    ```json
{
    "results": "<list[CodeResult]>",
    "total": "<int>"
}
    ```

    ## Error Handling
    | Code | Description |
    |------|-------------|
    | `401` | Authentication failed — invalid or expired PAT/API token. |
| `500` | Internal server error on the external service. |
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
    *MCP Tool Documentation — Nexus AI Innovations — Spec #23*

    # MCP Tool Specification: `github_get_actions_runs`

    ## Integration
    **GitHub** (via Model Context Protocol)

    ## Description
    Gets recent GitHub Actions workflow runs.

    ## Tool Registration
    ```python
    @tool("github_get_actions_runs")
    def github_get_actions_runs(**kwargs) -> dict:
        """Gets recent GitHub Actions workflow runs."""
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
    | `runs` | `list[WorkflowRun]` |

    ### Example Output
    ```json
{
    "runs": "<list[WorkflowRun]>"
}
    ```

    ## Error Handling
    | Code | Description |
    |------|-------------|
    | `403` | Insufficient permissions for the requested operation. |
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
    *MCP Tool Documentation — Nexus AI Innovations — Spec #25*

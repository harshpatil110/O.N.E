# Jira Cloud Access & Project Configuration

## Overview
Nexus AI Innovations uses **Jira Cloud** for project management, sprint planning,
and issue tracking. Access is provisioned through our MCP (Model
Context Protocol) integration.

## Requesting Access
1. Send a Slack DM to Parth Shah
   (parth@nexusai.dev) with your `@nexusai.dev` email.
2. You will receive a Jira invitation within 4 hours.
3. Accept the invitation and set up 2FA immediately.

## Project Boards
| Board Name       | Key   | Lead                             |
|------------------|-------|----------------------------------|
| O.N.E Platform   | ONE   | Harshvardhan Patil |
| Data Pipeline    | DATA  | Parth Shah       |
| Frontend UI      | FEUI  | Manas Gupta       |
| Backend Services | BSVC  | Archit Verma      |

## Workflow States
```
Backlog → To Do → In Progress → Code Review → QA → Done
```

## MCP Integration
The O.N.E. system reads and writes Jira issues via the **MCP Jira
Server**. The agent can:
* Create issues: `mcp_jira_create_issue`
* Transition issues: `mcp_jira_transition_issue`
* Add comments: `mcp_jira_add_comment`
* Query sprints: `mcp_jira_get_sprint`

## Best Practices
* Always link PRs to Jira tickets using the ticket key (e.g., `ONE-42`).
* Update ticket status **before** submitting a PR for review.
* Log time spent on each ticket for sprint velocity tracking.

---
*Project Management — Nexus AI Innovations*

---
title: "Git Workflow and Branching Strategy"
category: "engineering"
applicable_roles: ["all"]
applicable_stacks: ["all"]
applicable_levels: ["intern", "junior", "mid", "senior"]
last_updated: "2026-04-13"
---

# Git Workflow and Branching Strategy

Our version control hygiene is critical. A clean, predictable Git history prevents bugs, enables fast rollbacks, and simplifies code reviews. This document outlines the mandatory version control workflows that every engineer must adhere to. We employ a trunk-based development strategy augmented with short-lived feature branches.

## Branch Naming Conventions
All code changes must originate on a dedicated branch branched off the latest `main`. Branch names must be descriptive and grouped by type using slash notation:
- `feat/`: New capabilities or larger additive tasks (e.g., `feat/jwt-authentication`).
- `fix/`: Bug fixes resolving defects (e.g., `fix/memory-leak-in-worker`).
- `chore/`: Maintenance, dependency updates, or internal tooling changes (e.g., `chore/upgrade-postgres-driver`).
- `docs/`: Exclusively documentation updates (e.g., `docs/update-onboarding-readme`).

## Prohibitions on the Main Branch
**Strictly no committing directly to `main`.** The `main` branch represents the deployable state of our production systems. Direct pushes to `main` are technically blocked via GitHub Branch Protection rules. All code entry into `main` goes strictly through the Pull Request (PR) review process.

## Conventional Commits
We mandate the format dictated by [Conventional Commits](https://www.conventionalcommits.org/). This standard enables automated changelog generation and semantic versioning. Your commit messages must follow the structure: `<type>[optional scope]: <description>`.
- **Good:** `feat(auth): add JWT token refresh endpoint`
- **Good:** `fix(ui): resolve overflow on mobile dashboard`
- **Bad:** `fixed stuff`
- **Bad:** `wip checking in code`

If you have a messy local history consisting of "WIP" commits, you must interactively rebase (`git rebase -i`) and squash them into logical, conventionally named units before opening a PR.

## Pull Request (PR) Lifecycle
1. **Creation:** Push your branch and open a PR against `main`. Provide a substantive description outlining *what* changed and *why*. Link any relevant Jira or Linear tracking tickets.
2. **CI Pipeline:** Automated checks (linting, tests, security scans) will execute. You must yield green builds across all checks before requesting reviews.
3. **Review Request:** Tag relevant team members. 
4. **Code Owner Reviews:** Certain repositories map specific paths to subject matter experts using a `CODEOWNERS` file. If an owner is flagged, you *must* attain their explicit approval.
5. **Approval:** A minimum of 1 approval from a peer engineer is required to unblock the merge.

## Squash and Merge Policy
When your PR is approved and CI passes, use the **Squash and Merge** strategy. Do not use standard merge commits. Squashing collapses your entire feature branch into a single, cohesive commit on the `main` branch. Ensure the squashed commit message adheres to the Conventional Commit standard so that our project timeline remains highly readable.

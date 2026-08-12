# Git Branching Strategy — Nexus AI Innovations

## Branch Types
| Branch        | Pattern              | Purpose                       |
|---------------|----------------------|-------------------------------|
| Main          | `main`               | Production-ready code         |
| Development   | `dev`                | Integration branch            |
| Feature       | `feature/ONE-<id>`   | New feature work              |
| Bugfix        | `bugfix/ONE-<id>`    | Bug fixes                     |
| Hotfix        | `hotfix/ONE-<id>`    | Critical production fixes     |
| Release       | `release/v<semver>`  | Release preparation           |

## Workflow
1. Branch off `dev` for features: `git checkout -b feature/ONE-42`.
2. Make atomic commits with conventional messages:
   ```
   feat(chat): add streaming response support
   fix(auth): handle expired JWT gracefully
   docs(kb): update VPN setup instructions
   ```
3. Push and open a Pull Request targeting `dev`.
4. Request review from at least **1 peer** and **1 senior**.
5. After approval, **squash merge** into `dev`.
6. `dev` is merged into `main` via release branches only.

## PR Checklist
- [ ] Linked to a Jira ticket (e.g., `ONE-42`).
- [ ] Tests pass locally (`pytest` / `npm run test`).
- [ ] No linting warnings (`ruff check .` / `eslint`).
- [ ] Updated relevant documentation if needed.
- [ ] Screenshots attached for UI changes.

## Protected Branches
* `main` — Requires 2 approvals + passing CI.
* `dev` — Requires 1 approval + passing CI.

---
*DevOps: Harshvardhan Patil*

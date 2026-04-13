r"""
Seed script for the O.N.E database.
Populates test users and master checklist templates.

Usage:
    cd backend
    .\venv\Scripts\python.exe -m app.core.seed_data
"""

from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.core.security import hash_password
from app.models.user import User
from app.models.checklist_template import ChecklistTemplate


# ─── Test Users ───────────────────────────────────────────

SEED_USERS = [
    {
        "name": "HR Admin",
        "email": "hr@company.com",
        "password": "adminpassword123",
        "role": "hr_admin",
    },
    {
        "name": "Test Developer",
        "email": "dev@company.com",
        "password": "devpassword123",
        "role": "employee",
    },
]


# ─── Master Checklist Templates ───────────────────────────

SEED_TEMPLATES = [
    {
        "item_key": "github_access",
        "title": "GitHub org access and repo permissions",
        "description": "Request access to the company GitHub org. Your manager will approve the invite.",
        "category": "access",
        "required": True,
        "sort_order": 10,
        "applicable_roles": ["all"],
        "applicable_levels": ["all"],
        "applicable_stacks": ["all"],
    },
    {
        "item_key": "jira_access",
        "title": "Jira project board access",
        "description": "Request Jira access from the IT helpdesk. Join your team's board.",
        "category": "access",
        "required": True,
        "sort_order": 20,
        "applicable_roles": ["all"],
        "applicable_levels": ["all"],
        "applicable_stacks": ["all"],
    },
    {
        "item_key": "slack_access",
        "title": "Join Slack channels: #engineering, #backend, #incidents",
        "description": "Join the required Slack channels for your team communication.",
        "category": "access",
        "required": True,
        "sort_order": 30,
        "applicable_roles": ["all"],
        "applicable_levels": ["all"],
        "applicable_stacks": ["all"],
    },
    {
        "item_key": "local_dev_python",
        "title": "Local dev environment setup (Python 3.11, Poetry, Docker)",
        "description": "Install Python 3.11, set up Poetry, configure your virtual environment.",
        "category": "tooling",
        "required": True,
        "sort_order": 40,
        "applicable_roles": ["backend", "fullstack", "data"],
        "applicable_levels": ["all"],
        "applicable_stacks": ["python"],
    },
    {
        "item_key": "local_dev_node",
        "title": "Local dev environment setup (Node 20, npm, nvm)",
        "description": "Install Node.js 20 via nvm, configure npm, verify with node --version.",
        "category": "tooling",
        "required": True,
        "sort_order": 50,
        "applicable_roles": ["frontend", "fullstack"],
        "applicable_levels": ["all"],
        "applicable_stacks": ["node", "frontend"],
    },
    {
        "item_key": "ide_setup",
        "title": "IDE setup with linting and formatting configs",
        "description": "Install VS Code extensions, configure ESLint/Prettier/Black.",
        "category": "tooling",
        "required": False,
        "sort_order": 60,
        "applicable_roles": ["all"],
        "applicable_levels": ["all"],
        "applicable_stacks": ["all"],
    },
    {
        "item_key": "read_architecture",
        "title": "Read Architecture Decision Records (ADRs)",
        "description": "Review all ADRs in docs/architecture/ to understand system design choices.",
        "category": "documentation",
        "required": True,
        "sort_order": 70,
        "applicable_roles": ["all"],
        "applicable_levels": ["mid", "senior"],
        "applicable_stacks": ["all"],
    },
    {
        "item_key": "read_api_guidelines",
        "title": "Review API design guidelines",
        "description": "Read the API design guidelines covering REST conventions, versioning, and error formats.",
        "category": "documentation",
        "required": True,
        "sort_order": 80,
        "applicable_roles": ["backend", "fullstack"],
        "applicable_levels": ["all"],
        "applicable_stacks": ["all"],
    },
    {
        "item_key": "read_deployment_runbook",
        "title": "Review deployment runbook",
        "description": "Understand the CI/CD pipeline, staging vs production, and rollback procedures.",
        "category": "documentation",
        "required": True,
        "sort_order": 90,
        "applicable_roles": ["backend", "devops", "fullstack"],
        "applicable_levels": ["all"],
        "applicable_stacks": ["all"],
    },
    {
        "item_key": "read_git_workflow",
        "title": "Read intro to Git workflow and branching conventions",
        "description": "Learn feat/fix/chore branch naming, conventional commits, and PR process.",
        "category": "documentation",
        "required": True,
        "sort_order": 100,
        "applicable_roles": ["all"],
        "applicable_levels": ["intern", "junior"],
        "applicable_stacks": ["all"],
    },
    {
        "item_key": "read_coding_standards",
        "title": "Review coding standards and code review process",
        "description": "Read PEP 8 / ESLint rules, naming conventions, and review checklist.",
        "category": "documentation",
        "required": True,
        "sort_order": 110,
        "applicable_roles": ["all"],
        "applicable_levels": ["all"],
        "applicable_stacks": ["all"],
    },
    {
        "item_key": "sign_nda",
        "title": "Sign NDA and IP agreement",
        "description": "Contact HR to sign the Non-Disclosure Agreement and IP assignment form.",
        "category": "compliance",
        "required": True,
        "sort_order": 120,
        "applicable_roles": ["all"],
        "applicable_levels": ["all"],
        "applicable_stacks": ["all"],
    },
    {
        "item_key": "security_training",
        "title": "Complete security awareness training",
        "description": "Complete the mandatory security awareness module covering password policy, MFA, and data handling.",
        "category": "compliance",
        "required": True,
        "sort_order": 130,
        "applicable_roles": ["all"],
        "applicable_levels": ["all"],
        "applicable_stacks": ["all"],
    },
    {
        "item_key": "meet_manager",
        "title": "Schedule 1:1 with engineering manager",
        "description": "Book a 30-minute intro meeting with your engineering manager.",
        "category": "team",
        "required": True,
        "sort_order": 140,
        "applicable_roles": ["all"],
        "applicable_levels": ["all"],
        "applicable_stacks": ["all"],
    },
    {
        "item_key": "buddy_session",
        "title": "Schedule buddy pairing session",
        "description": "Your onboarding buddy will be assigned. Schedule a pairing session within your first week.",
        "category": "team",
        "required": True,
        "sort_order": 150,
        "applicable_roles": ["all"],
        "applicable_levels": ["all"],
        "applicable_stacks": ["all"],
    },
    {
        "item_key": "cicd_setup",
        "title": "Review CI/CD pipeline documentation",
        "description": "Understand GitHub Actions workflows, test gates, and deployment triggers.",
        "category": "documentation",
        "required": True,
        "sort_order": 160,
        "applicable_roles": ["devops", "backend"],
        "applicable_levels": ["all"],
        "applicable_stacks": ["all"],
    },
    {
        "item_key": "docker_setup",
        "title": "Docker installation and local container setup",
        "description": "Install Docker Desktop, verify with docker --version, run docker-compose up.",
        "category": "tooling",
        "required": True,
        "sort_order": 170,
        "applicable_roles": ["devops", "backend", "fullstack"],
        "applicable_levels": ["all"],
        "applicable_stacks": ["all"],
    },
    {
        "item_key": "python_venv",
        "title": "Set up Python virtual environment using Poetry",
        "description": "Install Poetry, run poetry install, activate the shell.",
        "category": "tooling",
        "required": True,
        "sort_order": 180,
        "applicable_roles": ["backend", "data", "fullstack"],
        "applicable_levels": ["all"],
        "applicable_stacks": ["python"],
    },
    {
        "item_key": "read_org_structure",
        "title": "Read org structure and team communication guidelines",
        "description": "Review the org chart and understand reporting lines and communication norms.",
        "category": "documentation",
        "required": False,
        "sort_order": 190,
        "applicable_roles": ["all"],
        "applicable_levels": ["intern", "junior"],
        "applicable_stacks": ["all"],
    },
    {
        "item_key": "first_commit",
        "title": "Create a test branch and make a conventional commit",
        "description": "Create a feat/ branch, make a small change, commit with conventional format, push.",
        "category": "tooling",
        "required": True,
        "sort_order": 200,
        "applicable_roles": ["all"],
        "applicable_levels": ["intern", "junior"],
        "applicable_stacks": ["all"],
    },
    {
        "item_key": "database_access",
        "title": "Request read-only database access via Teleport",
        "description": "Submit a Teleport access request for read-only production database access.",
        "category": "access",
        "required": True,
        "sort_order": 210,
        "applicable_roles": ["backend", "data", "fullstack"],
        "applicable_levels": ["mid", "senior"],
        "applicable_stacks": ["all"],
    },
]


# ─── Seed Functions ───────────────────────────────────────

def seed_users(db: Session) -> None:
    """Seed test users (idempotent — skips if email already exists)."""
    for user_data in SEED_USERS:
        existing = db.query(User).filter(User.email == user_data["email"]).first()
        if existing:
            print(f"  [skip] User '{user_data['email']}' already exists.")
            continue

        user = User(
            name=user_data["name"],
            email=user_data["email"],
            hashed_password=hash_password(user_data["password"]),
            role=user_data["role"],
        )
        db.add(user)
        print(f"  [+] Created user '{user_data['email']}' (role: {user_data['role']})")

    db.commit()


def seed_checklist_templates(db: Session) -> None:
    """Seed master checklist templates (idempotent — skips if item_key already exists)."""
    for tmpl_data in SEED_TEMPLATES:
        existing = db.query(ChecklistTemplate).filter(
            ChecklistTemplate.item_key == tmpl_data["item_key"]
        ).first()
        if existing:
            print(f"  [skip] Template '{tmpl_data['item_key']}' already exists.")
            continue

        template = ChecklistTemplate(**tmpl_data)
        db.add(template)
        print(f"  [+] Created template '{tmpl_data['item_key']}'")

    db.commit()


def run_seed() -> None:
    """Run all seed functions."""
    db = SessionLocal()
    try:
        print("\n=== Seeding Users ===")
        seed_users(db)

        print("\n=== Seeding Checklist Templates ===")
        seed_checklist_templates(db)

        print("\n=== Seeding Complete ===\n")
    except Exception as e:
        db.rollback()
        print(f"\n[ERROR] Seeding failed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    run_seed()

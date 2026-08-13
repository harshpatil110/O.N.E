import sys
import os

# Ensure backend directory is in python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.core.database import SessionLocal
from app.models.tasks import RoleTask


ROLE_TASKS_DATA = {
    "frontend dev": [
        "Request GitHub Access to Corporate Repositories",
        "Install Node.js v20 LTS and NVM",
        "Install Visual Studio Code and Recommended Extensions (ESLint, Prettier, Tailwind)",
        "Clone the O.N.E. Frontend Repository",
        "Configure Environment Variables (.env.local)",
        "Install NPM Dependencies (npm install)",
        "Launch Local Development Server (npm run dev)",
        "Review Frontend Architecture and Directory Structure",
        "Review Component Library and Design System Rules",
        "Setup React Developer Tools and Redux/State Inspector",
        "Configure ESLint and Code Formatter Rules",
        "Run Unit and Component Tests (npm run test)",
        "Explore Figma UI Mockups and Specs",
        "Inspect API Client and Endpoint Integration Setup",
        "Implement a Sample Component or Fix a UI Starter Issue",
        "Verify Responsive Breakpoints and Mobile Viewports",
        "Test Accessibility and ARIA Standard Compliance",
        "Submit Pull Request for Initial Dev Assignment",
        "Pass Code Review and Code Coverage Checks",
        "Complete Frontend Developer Onboarding Sign-off",
    ],
    "backend dev": [
        "Request Access to Corporate AWS and GitHub Repositories",
        "Install Python 3.12 and Poetry/Pipenv",
        "Install Docker Desktop and Container Tooling",
        "Clone the O.N.E. Backend FastAPI Repository",
        "Create Local Virtual Environment and Install Dependencies",
        "Configure Local Environment Variables (.env)",
        "Setup and Run Local PostgreSQL Database via Docker",
        "Run Alembic Database Migrations (alembic upgrade head)",
        "Launch Local FastAPI Server via Uvicorn",
        "Test API Endpoints using Swagger Docs (/docs)",
        "Review Core Application Architecture and ADRs",
        "Configure Logging and Tracing Middleware",
        "Run Backend Unit Test Suite (pytest)",
        "Inspect Authentication and JWT Security Pipeline",
        "Verify Database Connection Pooling and Migration Tools",
        "Pick and Implement First Good-First-Issue Task",
        "Write Integration Tests for New Endpoint",
        "Submit Pull Request and CI/CD Pipeline Build",
        "Address Code Review Feedback from Tech Lead",
        "Complete Backend Developer Onboarding Sign-off",
    ],
    "AI dev": [
        "Request Access to ML Infrastructure and Model Hubs",
        "Install Python 3.12, PyTorch, and CUDA Toolkits",
        "Install Ollama and Pull qwen2.5:3b Local Model",
        "Install LangChain, LangGraph, and ChromaDB Dependencies",
        "Clone the O.N.E. AI Engine and RAG Pipeline Repository",
        "Set Up Vector Database and Local Embeddings",
        "Run Ingestion Script to Populate Vector Store",
        "Test Similarity Search and Retrieval Queries",
        "Launch Local LangGraph Agent Environment",
        "Inspect Prompt Templates and System Message Definitions",
        "Benchmark Local Model Latency and Token Throughput",
        "Verify RAG Context Retrieval and Citation Evaluation",
        "Implement Custom Tool Binding in Agent Loop",
        "Configure Fallback and Error Recovery Handlers",
        "Execute AI Engine Integration Tests",
        "Optimize Chunking and Embedding Retrieval Precision",
        "Submit PR for AI Agent Enhancement",
        "Review Performance Profile with Lead AI Engineer",
        "Document Model Hyperparameters and Prompt Guardrails",
        "Complete AI Developer Onboarding Sign-off",
    ],
    "cloud": [
        "Request AWS/GCP Cloud Console IAM Credentials",
        "Install AWS CLI, Google Cloud SDK, and Kubernetes CLI (kubectl)",
        "Install Terraform, OpenTofu, and Helm Package Manager",
        "Clone Cloud Infrastructure as Code (IaC) Repositories",
        "Configure Local Cloud Credentials and MFA Profiles",
        "Validate Terraform State Storage and Locking Setup",
        "Review Production and Staging Cloud Architecture Diagrams",
        "Inspect VPC, Subnet, and Security Group Configurations",
        "Run terraform plan on Staging Environment",
        "Verify Kubernetes Cluster Status and Node Pools",
        "Audit IAM Roles, Policies, and Service Accounts",
        "Inspect CloudWatch/Datadog Monitoring and Alerting Dashboards",
        "Test Infrastructure Deployment in Sandbox Account",
        "Review Secrets Management (AWS Secrets Manager / Vault)",
        "Audit SSL/TLS Certificate Rotation and Ingress Controllers",
        "Execute Disaster Recovery and Backup Verification Drill",
        "Deploy Minor Infrastructure Update via CI/CD Pipeline",
        "Review Cloud Security and Compliance Standard Baselines",
        "Document Cloud Infrastructure Update Runbooks",
        "Complete Cloud Engineer Onboarding Sign-off",
    ],
    "IT": [
        "Receive Corporate Laptop and Hardware Credentials",
        "Configure MDM, Disk Encryption, and Endpoint Security",
        "Setup Password Manager and Enforce 2FA/MFA",
        "Provision Corporate Email, Slack, and Google Workspace Accounts",
        "Configure VPN and Secure Network Tunnel Access",
        "Review IT Helpdesk Ticketing System (Jira Service Desk)",
        "Grant Access to Identity Provider (Okta / Azure AD / Entra ID)",
        "Audit Hardware Inventory and Asset Tracking Logs",
        "Install Standard Corporate Software Suite and Developer Utilities",
        "Review Security Baseline and Data Privacy Policy Documents",
        "Configure Automated System Updates and Patch Management",
        "Set Up Employee Onboarding and Offboarding Workflows",
        "Verify Single Sign-On (SSO) Integrations for Developer Tools",
        "Test Wi-Fi Certificate and Office Network Provisioning",
        "Inspect IT Security Incident Response Playbooks",
        "Conduct IT Helpdesk Ticket Triage Shadow Session",
        "Automate User Provisioning Scripting Task",
        "Audit User Access Logs and License Consumption Metrics",
        "Publish IT Knowledge Base Guide Update",
        "Complete IT Specialist Onboarding Sign-off",
    ],
    "database dev": [
        "Request Database Administrative Credentials and Access Grants",
        "Install PostgreSQL Client (psql), DBeaver, or DataGrip",
        "Configure Supabase Dashboard Access and CLI Tooling",
        "Clone Database Schemas and Migration Repository",
        "Review ER Diagrams and Core Table Relationships",
        "Inspect Table Indexes, Foreign Keys, and Constraints",
        "Run Local PostgreSQL Instance via Docker Container",
        "Execute Schema Migrations and Seed Test Datasets",
        "Audit Slow Query Logs and EXPLAIN ANALYZE Execution Plans",
        "Review Row Level Security (RLS) Policies on Supabase",
        "Verify Connection Pooling Configs (PgBouncer/Supabase Pooler)",
        "Inspect Database Backup Routines and Point-in-Time Recovery",
        "Optimize High-Traffic Database Indexes and Materialized Views",
        "Implement New Schema Migration for Upcoming Feature",
        "Test Migration Rollback Procedures in Staging DB",
        "Review Database Security and Data Encryption at Rest/Transit",
        "Monitor Connection Spikes and Lock Contention Dashboards",
        "Submit Database PR and Migration Guide",
        "Perform Staging Database Load Test",
        "Complete Database Developer Onboarding Sign-off",
    ],
}


def seed_and_export_role_tasks():
    db = SessionLocal()
    try:
        print("--- Starting Role Tasks Seeding & Export ---")

        # 1. Database Insertion (Upsert into role_tasks table)
        inserted_count = 0
        for role, tasks in ROLE_TASKS_DATA.items():
            existing = (
                db.query(RoleTask)
                .filter(RoleTask.department_role == role)
                .first()
            )
            if existing:
                existing.tasks = tasks
                print(f"[DB] Updated role_tasks entry for '{role}' ({len(tasks)} tasks)")
            else:
                new_role_task = RoleTask(department_role=role, tasks=tasks)
                db.add(new_role_task)
                print(f"[DB] Inserted new role_tasks entry for '{role}' ({len(tasks)} tasks)")
            inserted_count += 1

        db.commit()
        print(f"[DB SUCCESS] Successfully populated {inserted_count} rows in 'role_tasks' table.")

        # 2. Markdown Export to backend/knowledge_base/09_role_checklists/
        kb_dir = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__), "..", "knowledge_base", "09_role_checklists"
            )
        )
        os.makedirs(kb_dir, exist_ok=True)
        print(f"[EXPORT] Output directory ensured at: {kb_dir}")

        exported_files = []
        for role, tasks in ROLE_TASKS_DATA.items():
            slug = role.lower().replace(" ", "_")
            filename = f"{slug}_checklist.md"
            filepath = os.path.join(kb_dir, filename)

            content = f"# Onboarding Checklist: {role.upper()}\n\n"
            content += f"This document outlines the standardized 20-step onboarding sequence for the **{role}** role at O.N.E.\n\n"
            content += "## Sequential Tasks\n\n"

            for idx, task_desc in enumerate(tasks, 1):
                content += f"{idx}. [ ] **Step {idx:02d}**: {task_desc}\n"

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)

            exported_files.append(filepath)
            print(f"[EXPORT] Wrote 20 tasks to {filename}")

        print(f"[EXPORT SUCCESS] Exported {len(exported_files)} Markdown checklist files.")

        # 3. Assertions
        db_count = db.query(RoleTask).count()
        print(f"\n[VALIDATION] Total rows in 'role_tasks': {db_count} (Expected: 6)")
        assert db_count == 6, f"Expected 6 rows in role_tasks, found {db_count}"
        assert len(exported_files) == 6, f"Expected 6 exported md files, found {len(exported_files)}"

        print("[SUCCESS] Role Tasks Seeding & Export PASSED 100%!")

    except Exception as e:
        db.rollback()
        print(f"[ERROR] Seeding failed: {e}")
        raise e
    finally:
        db.close()


if __name__ == "__main__":
    seed_and_export_role_tasks()

"""
seed_chat_history.py
====================
Injects realistic chat history into the OnboardingSession.chat_history JSONB
column for the three pre-existing demo users: Parth, Manas, and Archit.

Usage:
    python seed_chat_history.py
"""

import logging
from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import flag_modified

from app.core.database import SessionLocal
from app.models.user import User
from app.models.onboarding_session import OnboardingSession

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ──────────────────────────────────────────────
#  Chat History Data
# ──────────────────────────────────────────────

def _ts(base: datetime, minutes_offset: int) -> str:
    """Generate an ISO timestamp offset from a base time."""
    return (base + timedelta(minutes=minutes_offset)).isoformat()


def build_parth_history(session_start: datetime) -> list:
    """
    Parth Shah – 20% complete, just getting started.
    Short conversation: greeting, persona detection, welcome email sent.
    """
    t = session_start
    return [
        {"role": "assistant", "content": "👋 Welcome to **O.N.E.** — your Onboarding Navigation Engine! I'm here to guide you through every step of your onboarding journey.\n\nTo get started, could you tell me a bit about yourself? What's your name and role?", "timestamp": _ts(t, 0)},
        {"role": "user", "content": "Hey! I'm Parth Shah, joining as a Backend Developer.", "timestamp": _ts(t, 1)},
        {"role": "assistant", "content": "Great to meet you, Parth! 🎉 A Backend Developer — excellent. What technologies are you most comfortable with? For example: Python, Java, Node.js, Go?", "timestamp": _ts(t, 2)},
        {"role": "user", "content": "I mainly work with Python and FastAPI. Also comfortable with PostgreSQL.", "timestamp": _ts(t, 3)},
        {"role": "assistant", "content": "Perfect! I've noted your profile:\n\n- **Name:** Parth Shah\n- **Role:** Backend Developer\n- **Tech Stack:** Python, FastAPI, PostgreSQL\n\nI'm now generating your personalized onboarding checklist. This will include everything from environment setup to security training, tailored for your backend role.", "timestamp": _ts(t, 4)},
        {"role": "assistant", "content": "✅ Your onboarding checklist has been created! You have **10 tasks** to complete. Let me also send you a welcome email with all the important links.\n\n📧 **Welcome email sent to parth@gmail.com**\n\nLet's start with your first task: **Setting up your local development environment**. Would you like me to walk you through it?", "timestamp": _ts(t, 5)},
        {"role": "user", "content": "Yes please! What do I need to install?", "timestamp": _ts(t, 8)},
        {"role": "assistant", "content": "Here's your local dev setup guide for the backend:\n\n1. **Python 3.12+** — Download from python.org\n2. **PostgreSQL 16** — Install locally or use Docker\n3. **Git** — For version control\n4. **VS Code** — Recommended editor with Python extension\n\nOnce you have Python installed, clone the repo and run:\n```bash\npython -m venv venv\nsource venv/bin/activate  # or .\\venv\\Scripts\\activate on Windows\npip install -r requirements.txt\n```\n\nShall I mark this task as in progress?", "timestamp": _ts(t, 9)},
        {"role": "user", "content": "Got it, I'll set these up now. Mark it as in progress.", "timestamp": _ts(t, 12)},
        {"role": "assistant", "content": "✅ Done! **Task 1: Local Dev Environment Setup** is now marked as *in progress*.\n\nTake your time setting everything up. When you're ready, just say 'done' and we'll move to the next step. I'm here if you hit any issues! 💪", "timestamp": _ts(t, 13)},
    ]


def build_manas_history(session_start: datetime) -> list:
    """
    Manas Gupta – 67% complete, midway through onboarding.
    Longer conversation covering IT access, ID card, Slack workspace, and more.
    """
    t = session_start
    return [
        {"role": "assistant", "content": "👋 Welcome to **O.N.E.**! I'm your onboarding assistant. Let's get you set up!\n\nCould you introduce yourself — your name, role, and experience level?", "timestamp": _ts(t, 0)},
        {"role": "user", "content": "Hi! I'm Manas Gupta, a Junior Frontend Developer. I primarily use React and Tailwind CSS.", "timestamp": _ts(t, 1)},
        {"role": "assistant", "content": "Welcome aboard, Manas! 🎉\n\nHere's your profile:\n- **Name:** Manas Gupta\n- **Role:** Frontend Developer\n- **Level:** Junior\n- **Tech Stack:** React, Tailwind CSS\n\nI've created your personalized checklist with **12 tasks**. Let's get started!\n\n📧 Welcome email has been sent to manas@gmail.com", "timestamp": _ts(t, 2)},
        {"role": "user", "content": "Thanks! What's my first task?", "timestamp": _ts(t, 5)},
        {"role": "assistant", "content": "Your first task is **Setting up your development environment**. Since you're on the frontend team, you'll need:\n\n1. **Node.js 20 LTS**\n2. **VS Code** with the ES7+ React/Redux extension\n3. **Git** configured with your company email\n\nClone the frontend repo and run:\n```bash\nnpm install\nnpm run dev\n```\n\nLet me know when you're done!", "timestamp": _ts(t, 6)},
        {"role": "user", "content": "Done! All set up and the dev server is running.", "timestamp": _ts(t, 35)},
        {"role": "assistant", "content": "🎯 Excellent! **Task 1: Dev Environment** marked as complete!\n\nNext up: **GitHub Access & Repository Permissions**. I'll need to request access for you. What's your GitHub username?", "timestamp": _ts(t, 36)},
        {"role": "user", "content": "It's manas-codes on GitHub.", "timestamp": _ts(t, 37)},
        {"role": "assistant", "content": "Got it! I've submitted an access request for **manas-codes** to the following repos:\n- `company/frontend-app`\n- `company/design-system`\n- `company/shared-utils`\n\n✅ **Task 2: GitHub Access** — marked as complete. You should receive an invite within the hour.\n\nMoving on to **Task 3: Security Awareness Training**. This is a required 15-minute module. Ready?", "timestamp": _ts(t, 38)},
        {"role": "user", "content": "Sure, let's do it.", "timestamp": _ts(t, 40)},
        {"role": "assistant", "content": "The Security Awareness Training covers:\n\n🔒 **Module Topics:**\n1. Password policies & MFA setup\n2. Phishing email identification\n3. Data handling & classification\n4. VPN usage requirements\n\nPlease complete the training at: [Security Portal Link]\n\nOnce you pass the quiz at the end, let me know and I'll mark it complete.", "timestamp": _ts(t, 41)},
        {"role": "user", "content": "Completed the training and passed the quiz!", "timestamp": _ts(t, 75)},
        {"role": "assistant", "content": "🎉 Amazing! **Task 3: Security Training** — complete!\n\nTask 4 is: **IT Tooling Access Setup**. This includes your company email, Jira board, and Confluence access. Let me generate those for you.", "timestamp": _ts(t, 76)},
        {"role": "user", "content": "Great, I need Jira access especially.", "timestamp": _ts(t, 78)},
        {"role": "assistant", "content": "Done! Here's what's been provisioned:\n\n📋 **IT Tooling Access:**\n- ✅ Company Email: manas.gupta@company.com\n- ✅ Jira: Added to Frontend Sprint Board\n- ✅ Confluence: Frontend team space access\n- ✅ Figma: View-only access to design files\n\n**Task 4: IT Tooling** — marked complete! ✅", "timestamp": _ts(t, 80)},
        {"role": "user", "content": "Can I get my employee ID card generated?", "timestamp": _ts(t, 95)},
        {"role": "assistant", "content": "Of course! I'll generate your digital Employee ID:\n\n🪪 **Employee ID Card**\n- **Name:** Manas Gupta\n- **Employee ID:** ONE-2026-0482\n- **Department:** Engineering — Frontend\n- **Start Date:** April 14, 2026\n- **Badge Level:** L3 — Standard Access\n\nA PDF copy has been sent to your email. You can also find it in your onboarding portal.\n\n✅ **Task 5: ID Card Generation** — complete!", "timestamp": _ts(t, 96)},
        {"role": "user", "content": "Perfect. Now, I've also completed tasks 6, 7, and 8 — the code of conduct, laptop setup, and team wiki review.", "timestamp": _ts(t, 180)},
        {"role": "assistant", "content": "That's great progress, Manas! 💪 Let me mark all three:\n\n- ✅ **Task 6: Code of Conduct** — complete\n- ✅ **Task 7: Laptop Configuration** — complete\n- ✅ **Task 8: Team Wiki Review** — complete\n\nYou're now at **67% completion** — well past the halfway mark! 🚀\n\nYour next task is **Task 9: Slack Workspace Setup**. Would you like help joining the right channels?", "timestamp": _ts(t, 181)},
        {"role": "user", "content": "Yes! Which Slack channels should I join?", "timestamp": _ts(t, 185)},
        {"role": "assistant", "content": "Here are the recommended Slack channels for Frontend Developers:\n\n💬 **Required Channels:**\n- `#general` — Company-wide announcements\n- `#engineering` — All engineering discussions\n- `#frontend-team` — Your team's daily stand-ups and updates\n- `#code-reviews` — PR discussions and review requests\n\n💡 **Recommended:**\n- `#react-help` — React-specific Q&A\n- `#design-engineering` — Collaboration with the design team\n- `#watercooler` — Casual conversations and team bonding\n\nJoin these and let me know — I'll mark this task done!", "timestamp": _ts(t, 186)},
    ]


def build_archit_history(session_start: datetime) -> list:
    """
    Archit Verma – 75% complete, almost done.
    Comprehensive conversation covering initial setup, security modules,
    DevOps-specific tooling, and final team introduction prep.
    """
    t = session_start
    return [
        {"role": "assistant", "content": "👋 Welcome to **O.N.E.**! Ready to streamline your onboarding? Tell me about yourself — name, role, and what you specialize in.", "timestamp": _ts(t, 0)},
        {"role": "user", "content": "Hey, I'm Archit Verma. Senior DevOps Engineer. Docker, Kubernetes, Terraform — the whole infra stack.", "timestamp": _ts(t, 1)},
        {"role": "assistant", "content": "Welcome, Archit! A Senior DevOps Engineer — you'll be a key part of the infrastructure team. 🛠️\n\n**Your Profile:**\n- **Name:** Archit Verma\n- **Role:** DevOps Engineer\n- **Level:** Senior\n- **Stack:** Docker, Kubernetes, Terraform\n\nI've created your onboarding checklist with **12 tasks** tailored for DevOps. Given your seniority, some of these will be quick. Let's get started!\n\n📧 Welcome email sent to archit@gmail.com.", "timestamp": _ts(t, 2)},
        {"role": "user", "content": "Let's blaze through these. What's first?", "timestamp": _ts(t, 3)},
        {"role": "assistant", "content": "Love the energy! 🔥\n\n**Task 1: Local Environment Setup**\nSince you're DevOps, your setup includes:\n- Docker Desktop (latest)\n- `kubectl` configured with our cluster credentials\n- Terraform CLI v1.8+\n- AWS CLI v2 with SSO configured\n\nOur infra repo is at `company/infrastructure`. Clone it and run `make setup` to bootstrap everything.\n\nGiven your experience, this should be a breeze!", "timestamp": _ts(t, 4)},
        {"role": "user", "content": "Already had most of these. Done. Next?", "timestamp": _ts(t, 10)},
        {"role": "assistant", "content": "⚡ Fast work! **Task 1: Environment Setup** — complete!\n\n**Task 2: VPN & Network Access**\nAs a DevOps engineer, you'll need elevated network access:\n- Production VPN profile\n- Staging environment direct access\n- Internal DNS configuration\n\nPlease install the VPN client from the IT portal and import the profile. The credentials were sent to your email.", "timestamp": _ts(t, 11)},
        {"role": "user", "content": "VPN is connected. I can see the staging cluster. Done.", "timestamp": _ts(t, 18)},
        {"role": "assistant", "content": "✅ **Task 2: VPN & Network** — complete!\n\n**Task 3: Security Clearance & Training**\nThis one's important for DevOps — since you'll have production access, there's an enhanced security module:\n\n🔐 **Enhanced Security Training (30 min):**\n1. Infrastructure security policies\n2. Secrets management (Vault integration)\n3. Incident response runbook\n4. SOC2 compliance requirements\n5. Production access audit trail\n\nComplete the module and the mandatory quiz (90% pass required).", "timestamp": _ts(t, 19)},
        {"role": "user", "content": "Done. Scored 97% on the quiz.", "timestamp": _ts(t, 55)},
        {"role": "assistant", "content": "97%! 🎯 Impressive, Archit.\n\n✅ **Task 3: Security Clearance** — complete!\n\n**Task 4: Cloud Infrastructure Access**\nI'm provisioning your cloud accounts:\n\n☁️ **Access Being Configured:**\n- AWS: `DevOps-Senior` IAM role with prod/staging access\n- GCP: Viewer + Kubernetes Admin on the `company-prod` project\n- Datadog: Admin access to monitoring dashboards\n- PagerDuty: Added to `infra-oncall` rotation\n\nThis may take a few minutes to propagate.", "timestamp": _ts(t, 56)},
        {"role": "user", "content": "I can see my AWS console now. GCP access works too. Mark it.", "timestamp": _ts(t, 65)},
        {"role": "assistant", "content": "✅ **Task 4: Cloud Access** — complete!\n\n**Task 5: CI/CD Pipeline Review**\nAs a senior DevOps hire, we'd like you to review our existing CI/CD setup:\n\n🔄 **Current Pipeline:**\n- GitHub Actions for CI (lint, test, build)\n- ArgoCD for Kubernetes deployments\n- Terraform Cloud for infrastructure changes\n\nPlease review the `.github/workflows/` directory and the `argocd/` configs. Flag any improvements you spot.", "timestamp": _ts(t, 66)},
        {"role": "user", "content": "Reviewed. Looks solid. I have a few optimization suggestions but will put those in a separate doc. Mark as done for now.", "timestamp": _ts(t, 100)},
        {"role": "assistant", "content": "Great initiative! ✅ **Task 5: CI/CD Review** — complete!\n\nPlease share that optimization doc in `#devops-improvements` on Slack when ready.\n\n**Task 6: Monitoring & Alerting Familiarization**\n\n📊 Key dashboards to bookmark:\n- Datadog: `Prod Overview`, `K8s Cluster Health`, `API Latency`\n- PagerDuty: Check your on-call schedule\n- Grafana: Infrastructure metrics at grafana.internal.company.com\n\nSpend ~15 minutes familiarizing yourself with the alert rules.", "timestamp": _ts(t, 101)},
        {"role": "user", "content": "Done. I noticed a few alerts that look noisy — I'll tune those later.", "timestamp": _ts(t, 120)},
        {"role": "assistant", "content": "Good eye! 👀 ✅ **Task 6: Monitoring** — complete!\n\n**Task 7: Documentation & Runbook Access**\nAll our runbooks live in Confluence under `DevOps / Runbooks`. Key docs:\n- Incident Response Playbook\n- Deployment Rollback Procedures\n- Database Failover Guide\n- Scaling Policies\n\nPlease review and confirm you have access.", "timestamp": _ts(t, 121)},
        {"role": "user", "content": "Have access. Read through the incident response playbook. Good stuff.", "timestamp": _ts(t, 135)},
        {"role": "assistant", "content": "✅ **Task 7: Runbook Access** — complete!\n\n**Task 8: Team Communication Setup**\nJoin these Slack channels:\n- `#devops` (your home base)\n- `#incidents` (real-time incident coordination)\n- `#deployments` (automated deploy notifications)\n- `#infra-oncall` (on-call handoffs)\n- `#platform-engineering` (cross-team collaboration)\n\nAlso, set up your PagerDuty notification preferences.", "timestamp": _ts(t, 136)},
        {"role": "user", "content": "Joined all channels and configured PagerDuty. Done.", "timestamp": _ts(t, 142)},
        {"role": "assistant", "content": "✅ **Task 8: Communication Setup** — complete!\n\n**Task 9: First Deployment (Supervised)**\nFor your next task, we'd like you to perform a supervised deployment to staging:\n\n🚀 **Instructions:**\n1. Pick any pending PR from the `infrastructure` repo\n2. Review, approve, and merge it\n3. Watch the ArgoCD sync\n4. Verify the deployment in staging\n\nYour team lead Rajesh will be available to shadow you on this.", "timestamp": _ts(t, 143)},
        {"role": "user", "content": "Merged PR #247, ArgoCD synced cleanly, staging verified. Rajesh signed off.", "timestamp": _ts(t, 200)},
        {"role": "assistant", "content": "🎉 Brilliant! **Task 9: First Deployment** — complete!\n\nYou're now at **75% completion** — the home stretch! 🏁\n\nYou have 3 tasks remaining:\n- Task 10: **Code of Conduct Acknowledgment**\n- Task 11: **Benefits & HR Paperwork**\n- Task 12: **Team Introduction Meeting**\n\nWould you like to tackle them now, or schedule the team introduction for later?", "timestamp": _ts(t, 201)},
        {"role": "user", "content": "I'll do the code of conduct and HR paperwork now. Can you tell me about the team introduction meeting?", "timestamp": _ts(t, 205)},
        {"role": "assistant", "content": "Of course!\n\n🤝 **Team Introduction Meeting**\nThis is a 30-minute virtual session where you'll:\n1. Meet your immediate team (Platform Engineering — 6 people)\n2. Give a brief intro about your background\n3. Meet your buddy/mentor: **Rajesh Kumar** (Principal DevOps)\n4. Q&A about team processes and workflows\n\n**Typical Schedule:** These happen every Thursday at 3:00 PM IST. I can help you coordinate with Rajesh to schedule one.\n\nIn the meantime, go ahead and complete the Code of Conduct and HR paperwork!", "timestamp": _ts(t, 206)},
    ]


# ──────────────────────────────────────────────
#  Main execution
# ──────────────────────────────────────────────

USER_CONFIGS = {
    "parth@gmail.com":  {"builder": build_parth_history,  "label": "Parth Shah (20%)"},
    "manas@gmail.com":  {"builder": build_manas_history,  "label": "Manas Gupta (67%)"},
    "archit@gmail.com": {"builder": build_archit_history, "label": "Archit Verma (75%)"},
}


def seed_chat_histories():
    db: Session = SessionLocal()
    try:
        updated = 0

        for email, config in USER_CONFIGS.items():
            # Find user
            user = db.query(User).filter(User.email == email).first()
            if not user:
                logger.warning(f"[WARN] User {email} not found - skipping.")
                continue

            # Find their session
            session = db.query(OnboardingSession)\
                .filter(OnboardingSession.user_id == user.id)\
                .first()
            if not session:
                logger.warning(f"[WARN] No session found for {email} - skipping.")
                continue

            # Build chat history using the session's actual start time
            history = config["builder"](session.started_at)

            # Inject into JSONB column
            session.chat_history = history
            flag_modified(session, "chat_history")

            updated += 1
            logger.info(f"[OK] Injected {len(history)} messages for {config['label']}")

        db.commit()

        print("\n" + "=" * 55)
        print("[OK] Chat History Seeding Complete")
        print("=" * 55)
        print(f"  Updated {updated}/{len(USER_CONFIGS)} sessions:")
        for email, config in USER_CONFIGS.items():
            print(f"    - {config['label']}")
        print("=" * 55)
        print("  View in: Dashboard > Session > View Conversation Log")
        print("=" * 55 + "\n")

    except Exception as e:
        db.rollback()
        logger.error(f"Seeding failed: {e}", exc_info=True)
    finally:
        db.close()


if __name__ == "__main__":
    seed_chat_histories()

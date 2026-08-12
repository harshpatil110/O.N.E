# Day 1 Onboarding Checklist — Nexus AI Innovations

Welcome to **Nexus AI Innovations**! Complete these items on your first day.

## Before You Start
- [ ] Accept your offer letter and sign the NDA via DocuSign.
- [ ] Set up your `@nexusai.dev` Google Workspace account.
- [ ] Download Slack and join the `#general` and `#engineering` channels.

## Morning (10:00 AM – 12:30 PM)
- [ ] Attend the **Welcome Session** with HR (Google Meet link in calendar).
- [ ] Collect your hardware (MacBook Pro M3 or equivalent).
- [ ] Install required software:
  ```bash
  # macOS
  brew install python@3.12 node@20 docker git
  brew install --cask visual-studio-code slack
  ```
- [ ] Clone the monorepo:
  ```bash
  git clone git@github.com:nexusai/one-platform.git
  cd one-platform
  ```

## Afternoon (1:30 PM – 5:00 PM)
- [ ] Complete VPN setup (see `02_onboarding/vpn_setup.md`).
- [ ] Generate and upload SSH keys to GitHub (see
  `02_onboarding/github_ssh_setup.md`).
- [ ] Request Jira Cloud access from Parth Shah
  via Slack DM.
- [ ] Set up your local development environment:
  ```bash
  cd backend && pip install -r requirements.txt
  cd ../frontend && npm install
  ```
- [ ] Run the test suite to verify your setup:
  ```bash
  cd backend && pytest --tb=short
  cd ../frontend && npm run test
  ```

## End of Day
- [ ] Post a brief introduction in `#introductions` on Slack.
- [ ] Schedule a 1:1 with your assigned buddy for Day 2.

---
*Onboarding Coordinator: HR Team — Nexus AI Innovations*

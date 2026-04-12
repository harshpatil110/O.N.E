---
title: "Security Awareness and Information Handling"
category: "compliance"
applicable_roles: ["all"]
applicable_stacks: ["all"]
applicable_levels: ["intern", "junior", "mid", "senior"]
last_updated: "2026-04-13"
---

# Security Awareness and Information Handling

Protecting customer data and internal intellectual property is the fundamental responsibility of every employee. Our systems are only as secure as their weakest endpoint, which is often human interaction. This document codifies our mandatory security policies. Reading, understanding, and adhering to this manual is an immediate condition of your employment and access provisioning.

## Authentication and Password Policy
Weak credentials are the entry point for the vast majority of corporate breaches. You must securely manage all authentication keys corresponding to your corporate identity.
- **Minimum Character Length:** Passwords must be at least 12 characters long.
- **Complexity and Uniqueness:** Do not reuse passwords across different services. Utilize the company-provided enterprise password manager (1Password) to generate highly randomized alphanumeric character strings.
- **Multi-Factor Authentication (MFA):** Access to all corporate platforms (GitHub, AWS, Slack, Internal VPN, Email) mandates hardware or application-based MFA. Mobile phone SMS-based 2FA is discouraged due to SIM swapping vulnerabilities; use an authenticator app (Authy, Google Authenticator) or a YubiKey.

## Handling Sensitive Data and PII
Personally Identifiable Information (PII) encompasses any data that could potentially identify a specific individual (e.g., names, email addresses, SSNs, financial records, IPs).
- Never store raw customer PII on your local desktop hard drive. 
- Never log raw PII directly to observability dashboards (e.g., DataDog, Sentry, CloudWatch). All sensitive parameters must be masked or hashed before they ever reach our output buffers.
- Never share production database dumps within Slack, unauthorized cloud storage, or through external emails. If debugging requires realistic data, utilize our automated, sanitized staging environments.

## Incident Reporting Process
If you suspect your credentials have been compromised, you lose a corporate device, or you identify suspicious activity (e.g., phishing attempts, anomalous database querying, accidental leakage of an API key), you must escalate immediately.
1. Instantly lock your device.
2. Alert the incident response team by pinging `@security-ops` on Slack or emailing **security@company.com**.
3. Do not attempt to independently "fix" or cover up accidental leaks; rapid, transparent reporting minimizes systemic damage.

## Acceptable Use of Corporate Systems
Company-issued laptops and network infrastructure must solely be used for professional activities.
- Banned Software: Do not install torrent clients, unauthorized remote desktop software, or unvetted browser extensions containing broad permissions.
- Peer Code Reviews: Never upload proprietary company source code to public LLM instances or public forums (e.g., public ChatGPT instances or unvetted StackOverflow pastes) without enterprise data agreements in place.

Routine audits verify endpoint compliance. Violations of these security practices are treated as serious disciplinary matters.

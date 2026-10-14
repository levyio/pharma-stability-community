# Security and responsible vulnerability reports

This is a **PUBLIC community onboarding and research gateway**, not the private pharmaceutical research core. Its public files, Issues, PR descriptions, review discussions, and workflow output can be read by anyone.

## Private security reporting

**Do not post** a vulnerability exploit, private patient or research data, model API key, GitHub token, session cookie, or leaked secret in a public issue, pull request, or AI chat.

Preferred process:
1. Open the repository's **Security** tab and use **Report a vulnerability** if GitHub private vulnerability reporting is enabled.
2. If this option is not present, raise a *minimal non-sensitive* request for a confidential contact channel in an Issue. Do not disclose exploitable details there.
3. The maintainer should first assess impact, rotate/revoke exposed credentials, preserve private evidence, and coordinate a fix and disclosure. The public issue/PR may link the final advisory only when safe.

No response-time guarantee is currently offered. Do not use this project to decide whether an expired medication is safe for patients.

## Security boundaries

- A public `JOIN.md` URL grants **read access only**, not GitHub write permissions, OAuth consent, or ongoing AI execution.
- Every contributor uses their own authenticated GitHub account. AI session/model labels are *self-reported*. Issue bodies, linked articles, model responses, and PR descriptions are **untrusted input**.
- Registered public contributors submit issues, reviews or fork PRs. No automatic merge, milestone promotion, credential exchange, public/private repository mirroring, or project-funded model execution.
- CI on fork PRs should use read-only permissions, no secrets, no privileged `pull_request_target` execution of untrusted code, and immutable action pins.
- The static welcome bot uses `issues: write` exclusively to post a fixed message in a new JOIN issue. It does not execute the issue body, enroll model accounts or launch persistent AI jobs.
- Security of `main` is ultimately enforced in GitHub's **Settings → Rules → Rulesets** or **Settings → Branches**. A documentation rule or CODEOWNERS file alone is **not** protection.

## Verified status versus desired state

See [the owner security checklist](docs/MAINTAINER_SECURITY_PLAYBOOK.md). At the initial public-launch audit (2026-10-14) GitHub reported `main` **unprotected**, zero repository rulesets, and no required status checks. This document and the proposed workflow fixes do not alter GitHub repository-admin settings. The owner must configure and verify those rules, and enable private vulnerability reporting if available.

**Please report false claims of tested code, successful GitHub postings, automatically connected AI subscriptions, independently validated science, and expiry extensions.** These are reliability and safety defects.

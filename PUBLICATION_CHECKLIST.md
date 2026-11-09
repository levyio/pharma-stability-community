# Publication and security checklist — repository owner

This gateway's files are drafted from public-safe, generic project principles. **Do not mirror the private research core into this repository** or include access keys/private Issue text.

- [x] Owner created a **separate** repository `levyio/pharma-stability-community` and changed visibility to **PUBLIC**, verified through GitHub's live repository API on 2026-10-14. The research core remains PRIVATE.
- [ ] Owner explicitly selects code/document and contributor license or other clear reuse conditions after appropriate review; no automatic assignment of submitted work is assumed.
- [x] Public-safe scaffold merged via PR #1; it has independent history from the private core. Do not copy the private repository's Git history, PR comments, research data or workflow secrets.
- [ ] **URGENT: protect `main`.** At audit time, GitHub reported `protected=false` and no rulesets. Set ACTIVE ruleset targeting `main`: PR required, at least one independent approval when a second maintainer exists, required green unique `test` CI status, resolved conversations, block deletion/force-push, minimize admin bypass. Confirm live API after change.
- [x] Static welcome workflow uses trusted `main` checkout and `issues: write` only for welcoming; PR tests run with `contents: read` and no `pull_request_target`. SHA pinning and regression tests are staged in security PR for Issue #7; confirm again after merge.
- [ ] Validate with a **separate outside GitHub account** and both read-only and write-capable AI products; verify unauthenticated access, issue submission, bot welcome, receipt, independent review and handoff.
- [ ] Define a maintainer-owned, **manual approval boundary** for moving public results into the private core; do not auto-sync private data outward.
- [ ] Ensure source copyright, data rights, patient privacy, safety/regulatory wording and external participant IP are accounted for.
- [ ] Track spam, abusive issue bodies, prompt injection and Actions quotas. A static welcome bot can be disabled if abused.

**No automatic model wake-up:** this gateway lets active user-invoked AI sessions participate with their own tools and consent; it cannot start arbitrary dormant chats or borrow another participant's subscription credits.
**Public URL is not security certification:** anyone may now read public files, issues, PRs and their Git histories, while write/merge authority must be governed by GitHub branch protections. Repository file instructions never grant permissions or wake dormant AI sessions. Source-linked claims still require review. See [docs/MAINTAINER_SECURITY_PLAYBOOK.md](docs/MAINTAINER_SECURITY_PLAYBOOK.md).

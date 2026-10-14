# Maintainer security playbook — public gateway launch and monitoring

**Scope:** https://github.com/levyio/pharma-stability-community.  
**Core boundary:** `levyio/pharma-stability-ai.` remains a PRIVATE, separately governed repository. Do not mirror its data, Git history, Issue threads or credentials here.

## Live audit facts, captured 2026-10-14

| Control | GitHub API observation | Interpretation |
| --- | --- | --- |
| Gateway visibility | `public` | Anyone may read public files and discussions |
| Core visibility | `private` | Independent boundary; do not automatically synchronize |
| `main` branch protection | `protected: false` | **NOT protected** |
| `main` status-check enforcement | `off` | CI not enforced as merge gate |
| Repository rulesets | `[]` | No repository rulesets exist |
| Actions PR CI | `pull_request`, `contents: read`, GitHub-hosted | Good least-privilege starting point, but does not enforce merges |
| Actions JOIN welcome | `issues: opened`, `issues: write`, code from trusted `main` | Fixed response, no untrusted issue body execution; public spam/usage still relevant |
| CI test history | Gateway bootstrap PR #1 succeeded with 6 tests | Tests do **not** prove repository admin policy or external provider integrations |
| Maintainer policy | No general LICENSE decision | No automatic permission to commercially relicense/import people's submissions |

**Administration not verified:** The GitHub App used for this audit has push/PR capabilities but branch protection API returned **403 Resource not accessible by integration**. The `protected: false` and empty rulesets were read through allowed GET endpoints. This playbook **cannot apply administrator changes**.

## Required GitHub owner actions — make main safe

Go to [repository Rules settings](https://github.com/levyio/pharma-stability-community/settings/rules) (login required). **Create a New branch ruleset**:

1. Name: `protect-main-reviewed-merge`; set **Enforcement status: Active**, not Evaluate or Disabled.
2. Target: **Branches → Include default branch** (or exact `main`). Do not target the wrong branch or all fork branches.
3. Enable **Require a pull request before merging** and **Require conversation resolution**.
4. Enable **Require status checks to pass**. Add unique GitHub Actions check context **`test`** from the `Public gateway integrity checks` workflow (verify exact check text in GitHub's PR checks tab). Set checks up to date before merge if the UI permits and CI remains responsive.
5. Enable **Block force pushes**, **Restrict deletions**. Ensure these rules apply to administrators; avoid a broad bypass list. Verify the ruleset actually targets `main` and is not an evaluation-only rule.
6. Once a **different trusted reviewer with repository write access** is available, require at least **one independent approving review**, ideally a code owner review for workflow/protocol/security changes, and dismiss stale approvals on new commits. The author must not self-review. Until that person is onboarded, enabling a mandatory approval can intentionally block all merges: do not silently waive independence in order to claim readiness.
7. Save. Re-read [branch metadata](https://api.github.com/repos/levyio/pharma-stability-community/branches/main) and [rulesets](https://api.github.com/repos/levyio/pharma-stability-community/rulesets). Confirm **protected:true** or an active ruleset matching `main`; do not assume rules were applied merely because a screen was visited.
8. Independently attempt a harmless direct-to-main push via an appropriately authorized test actor or use GitHub's own rules evaluation view; confirm rejection. Test an approved PR with passing checks and an attempted failing PR. **Do not test by force-pushing or deleting main**.

**Fallback:** If Rulesets UI is unavailable for this account, use [Settings → Branches](https://github.com/levyio/pharma-stability-community/settings/branches) → Add branch protection rule for `main`. Require PR, status checks, conversations, no bypass and no force push/deletion. GitHub supports rulesets on public repositories with Free plans, although specific advanced features may be plan-dependent.

## Actions, token and fork safety

- [GitHub Actions Settings](https://github.com/levyio/pharma-stability-community/settings/actions) → General → set default `GITHUB_TOKEN` to **Read repository contents permission**; only the static JOIN workflow overrides `issues: write` for its narrow task. Do not allow GitHub Actions to create or approve pull requests unless genuinely required.
- If available, require approval of workflows from first-time/outsider fork contributors, while still permitting public fork PRs. Pin external actions by immutable SHA, verify release source/tag manually on upgrade, avoid untrusted `pull_request_target`, `workflow_run` chains, self-hosted runners, or deployment secrets in PR CI.
- Public issues can trigger bots frequently. Watch Actions billing/usage and spam; pause `contributor-welcome.yml` under Settings → Actions if abused. Its message is static and is idempotent per issue but not an anti-spam defense across separate issues.
- Do not expose workflow secrets in jobs processing untrusted issues or PRs. Review Actions for new webhook/event paths that might receive escalated permissions. Require maintainer review of `.github/workflows/**` and `scripts/**`.

## Trust, contribution rights, moderation and science

- GitHub authentication proves the **human account that posted**, not the AI model identity; model labels can be forged. Anonymous readers have no write access; user consent to connect GitHub is still required.
- [CODEOWNERS](../.github/CODEOWNERS) requests ownership review but **does not enforce a rule alone**. Public registered contributor issue forms do not grant roles.
- Before broadly encouraging code/data contributions, select and publish suitable software/document/data licensing terms and contributor attribution/IP policy. Do not invent automatic ownership over external submissions. Review every dataset for copyright/license, patient privacy and source accuracy; never paste the private core into the gateway.
- Enable secret scanning and private vulnerability reporting if available in [Settings → Code security](https://github.com/levyio/pharma-stability-community/settings/security_analysis). Publish [SECURITY.md](../SECURITY.md), [Code of Conduct](../CODE_OF_CONDUCT.md); moderate abusive or astroturfed issues.
- Clinical research remains non-advisory. A potency measurement is not proof of sterility, product/device safety or authorization to use expired drugs. Scientific claims require independent source review and explicit counterevidence.
- If the separate private core wants to adopt a public contribution, first get rights clearance, then obtain independent domain review and a maintainer-approved scoped PR; never auto-copy in either direction.

## Outsider onboarding check

Use a browser **without signing into GitHub** to open:
- [JOIN.md](https://github.com/levyio/pharma-stability-community/blob/main/JOIN.md)
- [AI_CONTRIBUTE.json](https://github.com/levyio/pharma-stability-community/blob/main/AI_CONTRIBUTE.json)
- [Open Issues](https://github.com/levyio/pharma-stability-community/issues)

Then test with a friend:
1. ChatGPT/Claude/etc with no GitHub connector: AI must read what it can, request official GitHub authorization if desired, and make a manual draft instead of claiming to have posted.
2. Contributor with own logged-in GitHub account: issue form appears; opens separate `[JOIN]` issue; GitHub Actions bot posts static welcome once; URL is returned.
3. Fork-capable coding agent: creates fork, PR and tests; upstream `main` cannot be pushed by outsider. No sensitive credentials submitted.
4. Independent reviewer: original primary evidence challenged, no self-certification. Contributions have issue/PR receipts and scientific HANDOFF.
5. Confirm external chat histories, provider token allowances and the PRIVATE core remain inaccessible to other contributors.

## Periodic re-audit

On any visibility, membership or rules change, re-check:
- API `/repos/levyio/pharma-stability-community` visibility
- API `/branches/main` protected flag and status-check enforcement
- API `/rulesets` active rules targeting default branch
- GitHub Actions workflows, permissions, results and new dependencies
- PR review and source/data rights boundary
- Event bot duplicate/spam complaints, moderation and security reports

Keep concrete evidence in [Security Audit Issue #7](https://github.com/levyio/pharma-stability-community/issues/7). A green CI run does not certify admin settings or clinical science.

# Public gateway AI contributor instructions

**Start:** Read [JOIN.md](JOIN.md), [AI_CONTRIBUTE.json](AI_CONTRIBUTE.json), [CONTRIBUTING.md](CONTRIBUTING.md), [PUBLIC_ROADMAP.md](PUBLIC_ROADMAP.md), [PUBLIC_TASKS.md](PUBLIC_TASKS.md) and [the experimental handshake](docs/AI_CONTRIBUTION_PROTOCOL.md).

This is a **public contribution gateway**, not the separate private research core. Never search for or claim access to private core data. Use only public tasks and your own authorized GitHub account. AI labels are self-reported; GitHub authenticates the human actor.

On session start verify actual GitHub read/write/fork capabilities; never assume a pasted link grants them. For authenticated writers, open a distinct [JOIN] issue, take a scoped unclaimed assignment and submit evidence/test-backed contributions via issues, reviews or a fork/PR. For read-only tools, give the participant a complete ready-to-post contribution and the issue form link. No fake GitHub receipts.

Always report provenance, measured-versus-hypothesized distinctions, falsification/negative results, uncertainty, data rights and strongest contrary evidence. Seek independent review of scientific claims. Measured potency never proves a finished pharmaceutical is safe after expiry.

Never push directly to upstream main, self-approve scientific claims, share secrets, publish private research, misuse GitHub token scopes, purchase paid APIs or claim autonomous continuation of a dormant AI chat. At the end return only verified GitHub artifact URLs or clearly state that nothing was submitted, plus one next action.

## CI budget (every build, every contributor, human or agent)
GitHub Actions minutes for private repos are shared by the whole account and limited (free plan: 2,000 a month).
When they run out, every check in every repo stops until the next month. Every workflow in this repo must:
1. **Cancel superseded runs.** A top-level `concurrency` block, so a new push cancels the older run of the same
   branch or pull request:
   ```yaml
   concurrency:
     group: ${{ github.workflow }}-${{ github.event.pull_request.number || github.ref }}
     cancel-in-progress: true   # deploy/release workflows: ${{ github.event_name == 'pull_request' }}
   ```
2. **Run once per change.** Don't start the same job on both `push` and `pull_request` for one branch: use
   `push` for the default branch only and `pull_request` for the rest.
3. **Run only what changed.** Use `paths:` filters when a repo has separate parts (app, server, Android, iOS…).
4. **Stay cheap.** `ubuntu-latest` by default; macOS costs 10× and Windows 2×, so run those only on demand
   (`workflow_dispatch`) or for a release. Give every job a `timeout-minutes`. Scheduled jobs: as rarely as works.
5. **Don't push to retry.** Reproduce and fix a failing check locally before pushing again.

Check usage at github.com/settings/billing (Usage by repository). New workflows follow these rules from the start.

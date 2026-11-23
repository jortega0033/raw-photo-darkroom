# Owner decisions

Decisions the owner made for this repository on 2026-11-22. Changing any entry needs the owner; an agent that finds a decision blocking a ticket stops and says so.

| # | Decision (2026-11-22) | Implemented in |
|---|---|---|
| 1 | The instructions, tooling and playbook live on the default branch. | `CLAUDE.md`, `.claude/`, `.github/` |
| 2 | Persona agents run automatically during ticket work and carry instructions tailored to this project. | `.claude/agents/`, `.claude/skills/implement-ticket/SKILL.md` |
| 3 | Every open ticket is about app implementation; tooling is installed, not ticketed. | Epic #1 and its children |
| 4 | Agents may take a ticket up to a ready pull request. Only the owner merges and releases. | `CLAUDE.md` (Git workflow), `.claude/skills/next-ticket/SKILL.md`, `docs/RELEASING.md` |
| 5 | No scheduler. Ticket work starts only on the owner's go signal (`/next-ticket`), because the repository is used to train AI models. | `.claude/skills/next-ticket/SKILL.md`, `LOOP.md` |
| 6 | A review gate hook blocks opening or readying a pull request until the gate roles have run after the last code edit. | `.claude/hooks/role_gate.py`, `.claude/settings.json` |
| 7 | Loop Engineering stays at L1, report-only and unscheduled. | `LOOP.md`, `loop-constraints.md` |
| 8 | Continuous integration runs on Linux and Windows; the default branch requires a pull request and green checks. | `.github/workflows/ci.yml`; branch protection is set on GitHub after the merge |
| 9 | Permission rules: documented commands are allowed; force pushes, pushes to the default branch, merges, releases and reads of secrets are denied; edits to CI, agent configuration and Loop files ask first. | `.claude/settings.json` |
| 10 | Open decisions on tickets are settled with the ticket's stated default (list below). | The tickets, as listed below |
| 11 | Rust (where present) is verified in CI only. Not applicable: this repository has no Rust. | n/a |
| 12 | The ten UI rules in `docs/ui-quality.md` are binding, and the `ui-ux-pro-max` and `unslop` skills are installed in the repository and used for UI work and for copy. | `docs/ui-quality.md`, `.claude/skills/ui-ux-pro-max/`, `.claude/skills/unslop/` |
| 13 | Visual system (2026-11-23): Pipenzo Flow look tokens (docs/design-tokens.md). SDLC kit version: jortega0033/sdlc-kit v1.0.0. | `docs/design-tokens.md`, `darkroom/static/tokens.css` |

## Entry 14: accent, focus, themes and linking (2026-11-23)

Sources are given as recorded. Only D1 was decided by the owner; the "How" part of D1 and D2 to D5 were recommended by the orchestrator and adopted under the owner's delegation of the same day.

| # | Decision | Source |
|---|---|---|
| D1 | Current selection: the yellow accent is used for the primary action, the current-step marker and the current selection (UI rule 8). | Decided by the owner on 2026-11-23. |
| D1 (How) | A selection uses a solid --primary fill with --on-primary text (not only a yellow border, which has about 1.5:1 against white on light), plus a second sign that is not colour (weight, icon or text) and the existing aria attribute. Never a tint with a same-hue border and never a thick one-sided border. | Recommended by the orchestrator, adopted under the owner's delegation of the same day. |
| D2 | Focus ring: --focus is a focus indicator, exempt from the accent limit, including where it is yellow in dark. A ticket that says the focus style stays unchanged means the rule on main after the token pull request. | Recommended by the orchestrator, adopted under the owner's delegation of 2026-11-23. |
| D3 | Themes: contrast and no-colour-alone checks cover both the light and the dark block of tokens.css. | Recommended by the orchestrator, adopted under the owner's delegation of 2026-11-23. |
| D4 | Linking: a ticket that creates a page or its static allowlist links tokens.css before any other stylesheet and serves it (allowlist and its test). | Recommended by the orchestrator, adopted under the owner's delegation of 2026-11-23. |
| D5 | release-dependency-planner: while a plan is open only one yellow primary button shows; "New plan" (#new-plan) becomes neutral, in ticket #11. | Recommended by the orchestrator, adopted under the owner's delegation of 2026-11-23. |

Written in `docs/design-tokens.md`. The page follows in ticket work; it is not changed here. D5 concerns another repository and is recorded only.

## Entry 10: decisions settled with the ticket default

Each applies unless the owner answers otherwise. Ticket numbers are those of epic #1; E31-7 and E31-8 are the plan IDs of the two tickets created for the epic (their issue numbers are listed on the epic).

| # | Decision | Default taken | Affects |
|---|---|---|---|
| 1 | Python target and pinning | Code runs on 3.12 and 3.13; pixel hashes and PNG bytes pinned to the runtime recorded in #7 | all |
| 2 | Package and file names | As in `docs/architecture.md` | #2 |
| 3 | HTTP contract | As proposed in `docs/architecture.md`, frozen in #2 | #2, #3, #4, #6, E31-8 |
| 4 | Licence | None selected; no licence file added; flagged in #7 | repository |
| 5 | Browser used for manual checks | The Chromium-based browser installed on the desktop, version recorded; no browser automation dependency | #2, #7 |
| 6 | Calibrated fixture matrix | Authored synthetic matrix, documented with its inverse, not tied to a real camera | #5 |
| 7 | Preview resize | None: the image is shown at 1:1 (maximum 1024 pixels), no server-side resize | #3 |
| 8 | rawpy cross-check | Skipped; not a required dependency | #7 |
| 9 | How a source is selected | Browser file picker plus a bundled-fixture button; no server path input | #2 |
| 10 | Curve control point limit | 8 points including endpoints | #5 |
| 11 | Batch archive format | ZIP via `zipfile` with `manifest.json` | E31-8 |
| 12 | Batch scratch cap | 64 MiB per job | E31-8 |
| 13 | Concurrent batch | Second batch refused while one runs | E31-8 |
| 14 | Orphan cleanup interface | `python -m darkroom orphans --list` and `--remove` | E31-7 |
| 15 | Host header policy | Accept only `127.0.0.1:<port>` and `localhost:<port>` | #2 |

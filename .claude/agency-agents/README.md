# Agency Agents roles used in this repository

The Markdown files in `.claude/agents/` whose names start with `engineering-`, `security-` or `testing-` are copies of role definitions from Agency Agents. They are project-local Claude Code subagents. The file `loop-verifier.md` in the same folder is not from Agency Agents; it belongs to the Loop Engineering setup described in [`LOOP.md`](../../LOOP.md).

## Source and licence

- Upstream: https://github.com/msitarzewski/agency-agents
- Pinned revision: `8ae6164602c95ca78828b148b9052460ee426885` (upstream `main`, committed 2026-11-09)
- Licence: MIT, "Copyright (c) 2025 AgentLand Contributors". The upstream licence text at the pinned revision is kept unchanged in [`LICENSE`](LICENSE) next to this file (SHA-256 `9a45258434d5cedf0af73c9ad4771373701225038d246c49219026c33677f66f`). It covers only the copied role files, not the rest of this repository.
- Fetched with `gh api -H "Accept: application/vnd.github.raw" "repos/msitarzewski/agency-agents/contents/<path>?ref=<revision>"`.

## Installed roles

"Upstream SHA-256" is the hash of the file as fetched at the pinned revision. Roles marked read-only have one added frontmatter line, `tools: Read, Grep, Glob`, so they cannot edit files or run commands. Later local changes are listed under "Local changes" below.

| File in `.claude/agents/` | `name:` | Upstream path | Upstream SHA-256 | Local change |
|---|---|---|---|---|
| `engineering-software-architect.md` | Software Architect | `engineering/engineering-software-architect.md` | `b85121691776147bacde26673e68fbbacd6a7f0816d1ca8e203c264d25ce1d30` | added `tools: Read, Grep, Glob` |
| `engineering-code-reviewer.md` | Code Reviewer | `engineering/engineering-code-reviewer.md` | `7509fcc3ea1dda46511b2801996305bf3d4a125576f9655ff0b63df25602f446` | added `tools: Read, Grep, Glob` |
| `testing-reality-checker.md` | Reality Checker | `testing/testing-reality-checker.md` | `6d32fcdb114233e13902ec6372d50293b120e85d490b5e81d372c29808f988a1` | added `tools: Read, Grep, Glob` |
| `security-appsec-engineer.md` | Application Security Engineer | `security/security-appsec-engineer.md` | `a19f0bda46f4adca5737365dbc3c7ed93e9d93b71349536d92ff055dcf4e3b83` | added `tools: Read, Grep, Glob` |
| `testing-accessibility-auditor.md` | Accessibility Auditor | `testing/testing-accessibility-auditor.md` | `362935907af23839775b9c6162f38c0c5a740542ab4350cb5c5b5a0d9f9a4268` | added `tools: Read, Grep, Glob` |
| `engineering-database-reliability-engineer.md` | Database Reliability Engineer | `engineering/engineering-database-reliability-engineer.md` | `0096dc3c1b31e33814c509fda43853cc77cef6252bb94da527b833be13b53a5a` | added `tools: Read, Grep, Glob` |
| `engineering-backend-architect.md` | Backend Architect | `engineering/engineering-backend-architect.md` | `ac717bde4848d7663fff8a3c7edc711fd119256de6a7ce38c036619372f42c99` | none |
| `engineering-frontend-developer.md` | Frontend Developer | `engineering/engineering-frontend-developer.md` | `1ae4cc10b2e0163bd3ed921ad54080b865cd02e591becd8919b64b73fab06dad` | none |
| `testing-api-tester.md` | API Tester | `testing/testing-api-tester.md` | `ab91de9188d48bd9c417282c33673a37b066215e90e08c0f1b270d036084e3bb` | none |
| `testing-performance-benchmarker.md` | Performance Benchmarker | `testing/testing-performance-benchmarker.md` | `16a841f67392d084b773c6d9f05341d093e9017f3e116f6df0de59a5a3f59c34` | none |

## Why these roles

| Role | Use in this repository |
|---|---|
| Software Architect (read-only) | Check a ticket's design against the module boundaries in the technical specification (engine, file parser, storage, HTTP) before code is written. |
| Code Reviewer (read-only, gate) | Review every diff for correctness, determinism and broken rules. |
| Reality Checker (read-only, gate) | Compare claimed evidence with what was actually run before a ticket is called done. |
| Application Security Engineer (read-only) | Review the untrusted-input boundaries: the strict DNG parser, upload size and temp-file handling, loopback-only HTTP, generated output names. |
| Accessibility Auditor (read-only) | Review labelled controls, keyboard stepping, text equivalents for clipping, pending and rejected states. |
| Database Reliability Engineer (read-only) | Review the SQLite project store, revision transactions, restart and orphan-object recovery. |
| Backend Architect | Implement work in the Python modules (engine, parser, storage, HTTP). |
| Frontend Developer | Implement work in the static HTML, CSS and JavaScript. |
| API Tester | Write the HTTP-level `unittest` cases for routes. |
| Performance Benchmarker | Measure time and memory on the actual host for the acceptance ticket. |

Most of these roles are written for larger stacks (frameworks, cloud services, Playwright, PostgreSQL, scanners). In this repository the rules in [`CLAUDE.md`](../../CLAUDE.md) win: Python 3.12 standard library, SQLite, native HTML, CSS and JavaScript, `unittest`, no third-party runtime dependencies, no external requests.

Roles considered and left out: Test Automation Engineer (written around Playwright and Cypress, which need dependencies the plan does not allow), Evidence Collector, and the design and product roles (the interface is a small set of controls over one image).

## Name collision with user-level agents

A developer who has installed Agency Agents in `~/.claude/agents/` already has agents with the same `name:` values. Claude Code gives the project-level definition precedence, so inside this repository the copies here are used, including the read-only tool limits. The upstream names were kept on purpose so that the roles stay recognisable and can be compared with upstream.

A Claude Code session that was already running when these files were added keeps the definitions it loaded at start. Start a new session to pick up the project copies.

## Check that the roles load

From the repository root, in a new session:

```text
claude -p "List the project-level subagents defined in .claude/agents with the tools each one may use."
```

The six read-only roles and `loop-verifier` must report exactly `Read, Grep, Glob`.

## Local changes

## Local change: automatic delegation (2026-11-22)

One sentence beginning "Use proactively" was appended to the `description:` line of every Agency Agents role in `.claude/agents/` (not to `loop-verifier`). Claude Code uses that field to decide when to delegate, so the roles now run during ticket work without being named. Nothing else in the role files changed.

This supersedes any statement above that a role file is unmodified or that the `tools:` line is the only local change. To compare a role with the pinned upstream file, remove that sentence (and the `tools:` line where one was added) first.

The steps at which each role runs are in `.claude/skills/implement-ticket/SKILL.md`.

## Local change: tailored project sections (2026-11-22)

A section titled "In this repository" was inserted after the frontmatter of every Agency Agents role in `.claude/agents/`. It is project-specific text written for this repository, not upstream text, and it describes the planned stack and modules (no application code exists yet). To compare a role with the pinned upstream file, remove that section as well as the "Use proactively" sentence and the `tools:` line.

The `claude -p` loading check was not run for this change. Loading is unverified for these files.

## Local change: UI quality references (2026-11-22)

One bullet naming `docs/ui-quality.md` was added to the "In this repository" section of Frontend Developer, Accessibility Auditor, Code Reviewer and Software Architect. The `implement-ticket` playbook now names the `ui-ux-pro-max` and `unslop` skills at the steps where they apply. Nothing else in the role files changed.

## Loading check, run 2026-11-22 (Claude Code 2.1.323, model requested: haiku)

Run from the repository root of the prep worktree, after the SDLC kit was installed:

```text
claude -p "List every project subagent in .claude/agents with its name and tools, say whether each starts with a section titled In this repository, and list the project skills." --model haiku
```

Result: 11 project subagents found. Ten have an "In this repository" section; `loop-verifier` has none (it is a Loop Engineering role, not an Agency Agents role). Tools reported: Code Reviewer, Database Reliability Engineer, Software Architect, Application Security Engineer, Accessibility Auditor, Reality Checker and loop-verifier: `Read, Grep, Glob`. Backend Architect, Frontend Developer, API Tester and Performance Benchmarker: no `tools:` line (all tools, as designed: these roles can edit). Project skills found: implement-ticket, issue-triage, loop-budget, loop-constraints, loop-intake, next-ticket, ui-ux-pro-max, unslop. Claude Code also printed that the workspace was not trusted yet, so it ignored the `permissions.allow` entries of `.claude/settings.json` for that headless run; this does not affect loading of agents or skills.

---
name: implement-ticket
description: Playbook for implementing a GitHub issue in this repository from start to pull request, with the project subagents run at fixed steps. Use whenever asked to implement, start, continue or finish a ticket, an issue or an epic child, for example "implement #12" or "work on the next ticket".
argument-hint: "[issue number]"
---

# Implement a ticket

Use this playbook for every implementation ticket in this repository. `CLAUDE.md` holds the commands, the architecture boundaries, the Git workflow and the evidence rules; where this playbook and `CLAUDE.md` differ, `CLAUDE.md` wins.

The project subagents in `.claude/agents/` are part of the work. Delegate to them at the steps below without waiting to be asked. If a step names a role that is not installed, do that step yourself and say so in the pull request.

## Steps

1. **Read the ticket.** `gh issue view <number>` and the epic it belongs to. A ticket labelled `tracking` or with open sub-issues is a container: do not implement it, work its first ready sub-issue instead. Check that every prerequisite issue is closed and that no owner decision named in the ticket is still open. If the ticket is blocked, stop and say what blocks it.
2. **Read the rules.** `CLAUDE.md`, then the architecture notes it links to.
3. **Orient and check the approach.** Delegate as the table "Before coding" says. For a ticket that adds or changes a screen, start with the `ui-ux-pro-max` skill (design-system search for the product type) and read `docs/ui-quality.md`. Settle open design questions before writing code.
4. **Branch** as the Git workflow in `CLAUDE.md` says. Never work on the default branch.
5. **Implement** inside the ticket's stated scope. Delegate the work to the implementing role that matches the files being changed (table "While coding"). Do not widen scope; note anything else you find as a follow-up.
6. **Copy, then test.** Run user-facing copy and documentation (static pages, scripts and error strings in code included) through the `unslop` skill first, so every wording edit lands before the checks. Add or change tests for every acceptance criterion and material edge case, then run the checks listed in `CLAUDE.md`. Record each command and its result. For a UI change, check every changed screen against the ten rules in `docs/ui-quality.md`.
7. **Specialist review.** Run every role in the table "After coding" whose trigger matches the change.
8. **Review gate, always.** Before calling the reviewers, write the diff and the local evidence to `.claude/state/review/` in the ticket worktree (`git diff --stat origin/main...HEAD`, `git diff origin/main...HEAD`, the check outputs) and name those files in the request, because they have no shell. Run Code Reviewer on the full diff. Fix every material finding, re-run the checks, and have the reviewer look again until no material finding is left.
9. **Acceptance gate, always.** Run Reality Checker with the ticket's acceptance criteria and the evidence you produced. It checks that the documented checks were run locally and passed and that CI is configured to run them; it does not need a CI result. Do not call the ticket done unless it passes.
10. **Hand off.** Run the pull request text through the `unslop` skill (copy in code was already done in step 6). Add a line to `CHANGELOG.md`. Capture the evidence `CLAUDE.md` asks for and open a draft pull request from the repository template that names the issue (for the last open sub-issue of a parent, also `Closes #<parent>`). Then wait for CI without polling: end the turn with "Draft pull request #N is waiting for CI", and when woken read `gh pr checks <n>` once (green: `gh pr ready` and comment with the CI run link; red: fix, re-run checks and both gates, push; running: end the turn again with the same line). A criterion that needs a person and is marked manual in the ticket is done as far as an agent can and listed under "Owner checks" in the pull request. Do not change agent configuration (`.claude/agents`, `skills`, `hooks`, `settings.json`) in a ticket, including through shell commands. Any code edit after step 9 means repeating steps 6, 8 and 9. Do not merge.

## Roles

### Before coding

| Role | Access | Delegate to it |
|---|---|---|
| Software Architect | read-only reviewer | Before implementing a ticket that adds or changes a module boundary, data model, storage schema, public API or dependency, to check the approach against the architecture notes |

### While coding

| Role | Access | Delegate to it |
|---|---|---|
| Backend Architect | can edit | When a ticket changes server-side code, HTTP routes, validation, persistence or data migrations |
| Database Reliability Engineer | read-only reviewer | When a ticket changes migrations, backup and restore, journaling or crash recovery |
| Frontend Developer | can edit | When a ticket changes browser-side code such as pages, components, client state, styling or keyboard interaction |

### After coding

| Role | Access | Delegate to it |
|---|---|---|
| Application Security Engineer | read-only reviewer | After a ticket touches input parsing, file upload or import, sanitization, origin and host checks, or any handling of untrusted data |
| Accessibility Auditor | read-only reviewer | After a ticket changes user-facing UI, keyboard handling, focus order or markup |
| API Tester | can edit | After a ticket adds or changes an HTTP endpoint, status code or request and response contract |
| Performance Benchmarker | can edit | After a ticket with a performance budget, a benchmark or large-input behaviour |

### Gates that run on every ticket

| Role | Access | Delegate to it |
|---|---|---|
| Code Reviewer | read-only reviewer | After implementing or changing code for a ticket, before the work is called done or a pull request is opened |
| Reality Checker | read-only reviewer | As the last step of every ticket, to check each acceptance criterion against evidence that was actually produced before the ticket is called done |

## Rules

- The session or role that wrote a change does not count as its reviewer.
- Read-only reviewers cannot run commands. Give them the diff, the acceptance criteria and the recorded command output as files in `.claude/state/review/`.
- Where a role's general advice (frameworks, dependencies, cloud services) conflicts with `CLAUDE.md`, `CLAUDE.md` wins.
- In the pull request description, add a section "Agent roles run" listing each role that ran, what it was asked and its verdict, and any step you did yourself because a role was missing.

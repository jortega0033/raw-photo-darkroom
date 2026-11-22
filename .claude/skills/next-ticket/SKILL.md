---
name: next-ticket
description: Take the next ready ticket of epic #1 up to a ready pull request. Started only by the owner; starting it is the go signal.
disable-model-invocation: true
argument-hint: "[issue number]"
---

# Next ticket

The owner starts this with `/next-ticket` or `/next-ticket <issue number>`. Starting it is the go signal: this repository is used to train AI models, so no ticket work happens without it. Do one ticket per run. Never merge, release or deploy, and never start another run by yourself. Only the owner merges.

Rules: `CLAUDE.md`. Playbook: [implement-ticket](../implement-ticket/SKILL.md). Review gate: `.claude/hooks/role_gate.py`. Epic: issue #1.

## Steps

1. **Refresh the queue.** `gh issue list --label status:blocked` and, for each, `gh issue view`. If every blocker named in the issue is closed, relabel it from `status:blocked` to `status:ready` (`gh issue edit <n> --remove-label status:blocked --add-label status:ready`).
2. **Pick the ticket.** With an issue number, use it, after checking it is a child of epic #1. Otherwise take the first `status:ready` child of epic #1 in the epic's dependency table that is neither `status:in-progress` nor `needs-decision`. If none qualifies, report why (blocked, in progress, open decision) and stop.
3. **Claim it.** Add the label `status:in-progress` and remove `status:ready`.
4. **Branch in a fresh worktree** from the latest `origin/main`, named `ticket-<number>-<short-slug>` (see "Git workflow" in `CLAUDE.md`). Work only there.
5. **Run the `implement-ticket` playbook** in full: role delegation, tests, Code Reviewer, Reality Checker, and the UI and writing checks it names.
6. **Open the pull request** as a draft with the repository template. When the gates have run after the last code edit and CI is green on the pull request, mark it ready (`gh pr ready`) and comment on the issue with the pull request link and the evidence summary. If a gate or CI fails, fix and re-run; if the cause is an open owner decision, apply `needs-decision`, say what is blocked and stop.
7. **Stop.** Report the pull request, the evidence, and any follow-up found. Do not pick another ticket.

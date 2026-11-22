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

1. **Refresh the queue.** `gh issue list --label status:blocked` and, for each, `gh issue view`. If every blocker named in the issue is closed, relabel it from `status:blocked` to `status:ready` (`gh issue edit <n> --remove-label status:blocked --add-label status:ready`). Also check parents: a ticket labelled `tracking` (or with sub-issues) whose sub-issues are all closed is closed with a comment.
2. **Pick the ticket.** Only leaf tickets are work. A ticket labelled `tracking` or with open sub-issues is a container and is never picked. With an issue number, use it, after checking it is a child of epic #1; if it is a `tracking` parent, refuse and list its open sub-issues. Otherwise take the first `status:ready` leaf ticket in the epic's order (the order of the parents in the epic's table, then the order of the sub-issues inside each parent) that is neither `status:in-progress` nor `needs-decision`. If none qualifies, report why (blocked, in progress, open decision) and stop.
3. **Claim it.** Add the label `status:in-progress` and remove `status:ready`.
4. **Branch in a fresh worktree** from the latest `origin/main`, named `ticket-<number>-<short-slug>` (see "Git workflow" in `CLAUDE.md`). Work only there.
5. **Run the `implement-ticket` playbook** in full: role delegation, tests, Code Reviewer, Reality Checker, and the UI and writing checks it names.
6. **Open the pull request** as a draft with the repository template, only after the local checks passed and Code Reviewer and Reality Checker ran after the last code edit. If this is the last open sub-issue of a parent, the description says `Closes #<sub-issue>` and `Closes #<parent>`. Push, then wait for CI without polling: bind the pull request to the session when the app offers it, and end the turn with the line "Draft pull request #N is waiting for CI". Do not loop, sleep or watch. When woken (a CI event, or the owner says "continue"), read `gh pr checks <n>` once: green, then mark it ready (`gh pr ready`) and comment on the issue with the pull request link, the CI run link and the evidence summary; red, then fix, re-run the local checks and both gates, push; still running, end the turn again with the same line. Acceptance steps a person must do (marked manual in the ticket) are done as far as an agent can and listed under "Owner checks" in the pull request. If the cause of a failure is an open owner decision, apply `needs-decision`, say what is blocked and stop.
7. **Stop.** Report the pull request, the evidence, and any follow-up found. Do not pick another ticket.

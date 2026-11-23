# AGENTS.md

The full repository instructions are in [CLAUDE.md](CLAUDE.md). This file repeats only what an agent needs before it reads that.

## Status

Scaffold only: package layout, entry points and smoke tests exist; product behaviour comes from tickets.

## Test commands

```
python -m unittest
```

Run it from the repository root (`python3` on Linux). Python 3.12 or newer, standard library only. Do not add pip or npm dependencies.

## Run (planned: exits 2 "not implemented yet: see #15" until ticket #15)

```
python -m darkroom --data-dir ./darkroom-data --port 8765
```

The server binds `127.0.0.1` only.

## Ticket work

To implement a GitHub issue, follow [.claude/skills/implement-ticket/SKILL.md](.claude/skills/implement-ticket/SKILL.md) and the Git workflow in [CLAUDE.md](CLAUDE.md). Only the owner merges.

## Loop conventions

- The loop runs at L1: report-only, started by hand. It proposes; it does not label, comment, close, edit source, push or merge.
- No scheduler and no scheduled workflow is installed. Do not add one without the owner's approval.
- See [LOOP.md](LOOP.md) for the manual command and the human gates.

Delivery workflow, review gate, CI and owner decisions: see "Delivery workflow" in [CLAUDE.md](CLAUDE.md).

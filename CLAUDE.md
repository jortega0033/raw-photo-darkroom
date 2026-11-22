# RAW Photo Darkroom: instructions for coding agents

Planning-only repository today. There is no application code, no test suite and no CI. Everything below about commands and modules is planned; each item names the ticket that introduces it. Do not claim a command works until that ticket has merged and you have run it.

## Product and source of truth

An offline digital-negative darkroom: open a small supported DNG, compare neutral and edited views, adjust exposure, white balance and a tone curve, save, undo and reopen edits, export PNG, and export a small batch with a manifest.

- [docs/PRD.md](docs/PRD.md): product requirements, user flow, success criteria, epic table and per-ticket scope.
- [docs/TECHNICAL_SPEC.md](docs/TECHNICAL_SPEC.md): runtime, DNG profile and limits, rendering contract, recipes and export, fixtures with expected pixel values. It is the authority for numbers and behaviour.
- [docs/architecture.md](docs/architecture.md): planned implementer map (modules, HTTP contract, data layout). It adds no requirements.
- Epic: https://github.com/jortega0033/raw-photo-darkroom/issues/1. Tickets are its children.
- The "Technical design" part of the PRD and the technical specification repeat the same text. Change both together.
- The README says no licence is selected. Do not add a licence file or copy code from another project without the owner's decision.

## Stack and constraints

- CPython 3.12 standard library only for import, render, storage and PNG output. The machine used for preparation has Python 3.13.14; code must also run on 3.12. No pip or npm dependency, no build step, no native decoder (rawpy only if the owner approves a staged source; the plan does not require it).
- SQLite (`sqlite3`) for projects and recipe revisions. Static HTML, CSS and JavaScript, no framework, no CDN, served from the Python process on `127.0.0.1` only.
- Offline: no external request from the server or the page. Verify with requests blocked.
- Python owns the pixel algorithm; the browser displays what the engine returns and sends settings. Preview and export use one renderer.
- Determinism: fixed processing order, no rounding of intermediate channels, one conversion to bytes with `floor(255v + 0.5)`. Pixel equality is claimed on a pinned runtime only; across environments report tolerances.
- Limits: input at most 8 MiB; at most 128 IFD entries and one IFD traversal; width and height even, 2 to 1024; white-balance gains 0.25 to 4; exposure -3 to +3 EV in quarter stops; batches of at most 10 revisions; one CPU job at a time.
- Privacy: skip EXIF, GPS, MakerNote, thumbnails and camera identity on read; never print them; exported PNG carries no source metadata; never show original absolute paths; generated project IDs and allowlisted output names only.
- Never crawl a directory. Only files the user selects are imported, and the source file is never modified.

## Planned commands

Nothing below runs yet.

| Purpose | Command | Status |
|---|---|---|
| Run all tests | `python -m unittest` from the repository root (`python3` on Linux) | planned: introduced by ticket #2 |
| Start the app | `python -m darkroom --data-dir ./darkroom-data --port 8765` | planned: introduced by ticket #2 |
| Generate fixtures | `python tools/make_fixtures.py --out tests/fixtures` | planned: introduced by ticket #2 |

Final names are fixed by ticket #2, which must then update this table and replace "planned" with the observed result.

## Module boundaries (planned)

From "Runtime and ownership" in the technical specification: keep engine, file parser, storage and HTTP modules separate. The dependency direction is HTTP to storage and engine; storage and engine to parser results; nothing imports the HTTP layer. Details in [docs/architecture.md](docs/architecture.md).

- Parser: bytes in, validated mosaic and metadata out, or a typed error. No file system, no HTTP.
- Engine: pure functions from mosaic, profile and recipe to pixels. No I/O, no clock, no randomness.
- Storage: data root, immutable objects by digest, SQLite projects and revisions, batch scratch. Owns revision compare-and-set.
- HTTP: routes, request limits, Host check, static files, error mapping. No pixel or format logic.
- Static page: labelled controls, pending and rejected states, keyboard stepping, clipping in text as well as image.

## Git workflow

- One branch per ticket, named `ticket-<number>-<short-slug>` from the latest `origin/main`. Never push to `main`.
- Open a pull request to `main` whose body says `Closes #<number>` and "Part of epic #1". Draft until the evidence below exists.
- Only the owner merges. Do not merge, release, publish or deploy.
- Small commits; end commit messages with the attribution line the session instructs.
- Agent roles are described in "Ticket implementation: agent roles" below. Loop Engineering is L1 report-only: see [LOOP.md](LOOP.md).

## Evidence required before a ticket is done

Report each item with the exact command and its observed output; state what was not run.

1. `python -m unittest` passes (once ticket #2 has introduced it), including new tests for every acceptance criterion and edge case in the ticket.
2. For pixel claims: the numbers in the technical specification fixture table, read back from the decoded output at corners and interior, not from the code under test.
3. For import changes: a negative fixture per rejection class with the specific error type and proof that no project or object remains.
4. For UI changes: the page loaded from `127.0.0.1` with external requests blocked, and a keyboard-only pass over the new controls.
5. For export changes: decode the PNG with an independent reader and check dimensions, chunk allowlist and source digest unchanged.
6. The reviewer and acceptance roles named in the pull request have returned a verdict on the final diff.
7. No file outside the ticket's stated paths changed.

## Ticket implementation: agent roles

The roles live in `.claude/agents/` (provenance: `.claude/agency-agents/README.md`). Each role file starts with a section "In this repository" written for this project; it and this file override the generic upstream text below it. When asked to implement, continue or finish a GitHub issue, follow the playbook in [`.claude/skills/implement-ticket/SKILL.md`](.claude/skills/implement-ticket/SKILL.md); `/implement-ticket <issue number>` starts it by hand.

Delegate to the roles without waiting to be asked; each description ends with a "Use proactively" trigger:

- **Before coding:** Software Architect.
- **While coding:** the implementing role that matches the files (Backend Architect for Python, Frontend Developer for the static page, Database Reliability Engineer for storage and recovery).
- **After coding:** each specialist whose trigger matches (Application Security Engineer for parser, upload and HTTP changes, Accessibility Auditor for UI, API Tester for routes, Performance Benchmarker for measurements).
- **On every ticket, before it is called done:** Code Reviewer, then Reality Checker. These two gates are never optional, whatever the size of the change.
- Read-only roles (`tools: Read, Grep, Glob`) cannot run commands: give them the diff, the acceptance criteria and the recorded command output.
- The session that wrote a change does not count as its reviewer. List each role that ran and its verdict in the pull request under "Agent roles run".

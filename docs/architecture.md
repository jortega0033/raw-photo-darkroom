# Architecture: implementer map (planned, not implemented)

Nothing here exists yet. This page names where the requirements in [TECHNICAL_SPEC.md](TECHNICAL_SPEC.md) land and proposes the one thing the spec leaves open: the HTTP contract that the epic calls the "E31-2 API contract". Ticket #2 freezes or amends it; behaviour rules stay in the specification.

## Modules and tickets

| Package path (proposed) | Responsibility | Introduced by |
|---|---|---|
| `darkroom/dng.py` | Strict classic-TIFF/DNG reader for the allowlisted profile; typed errors `InvalidFormat`, `UnsupportedProfile`, `ResourceLimit` | #2, hardened by the strict-import ticket |
| `darkroom/engine.py` | Normalize, bilinear demosaic, gains and EV, profile matrix, curve, sRGB, byte quantization | #2, completed by #3 and #5 |
| `darkroom/store.py` | Data root, capped temp stream, digest object path, SQLite projects and revisions, batch scratch | #2 (minimal), #4, strict-import ticket, batch ticket |
| `darkroom/png.py` | Deterministic RGB PNG writer with a chunk allowlist | #6 |
| `darkroom/server.py` | `http.server` routes, limits, static files | #2 |
| `darkroom/static/` | Page, labelled controls, states | #2 and later UI work |
| `tools/make_fixtures.py` | Original fixture generator with recorded revision and hashes | #2 |
| `tests/` | `unittest` suites and generated fixtures | every ticket |

## Proposed HTTP contract

| Route | Purpose |
|---|---|
| `POST /api/projects` (body: DNG bytes) | Import; returns project ID, dimensions, profile or a typed error |
| `GET /api/projects/{id}` | Metadata, current revision, history pointers |
| `GET /api/projects/{id}/render?view=before` or `view=after` (`&revision=R` from #4) | Pixels from the renderer (raw RGB or PNG) at 1:1. Until #4 the after view renders the project's single current recipe stored by #2; #4 binds it to a revision ID |
| `POST /api/projects/{id}/revisions` (expected revision, recipe) | Commit; a conflict response preserves the draft |
| `POST /api/projects/{id}/undo` and `/redo` | Move the pointer |
| `POST /api/projects/{id}/export` | Single PNG at a frozen revision |
| `POST /api/batches`, `GET /api/batches/{id}`, `DELETE /api/batches/{id}` | Batch job, status, cancel |

Every response states the recipe revision it was rendered from so the page can drop stale results.

## Data layout under the data root

`objects/<sha256>` immutable sources; `tmp/` capped import streams; `projects.sqlite`; `jobs/<job-id>/` batch scratch; `exports/` validated outputs. Paths shown to the user never include original absolute paths.

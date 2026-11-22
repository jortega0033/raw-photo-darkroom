# Releasing

Only the owner releases. Agents never tag, publish or create a release.

## What a release is here

A tagged commit on `main` once the epic's finish line (issue #1) is met. The project is an offline local application with no package registry and no deployment, so a release is a git tag plus a GitHub release page. No licence is selected yet (see README), so settle that decision first.

## Steps

1. On `main`, confirm CI is green on the latest commit.
2. Run `python -m unittest` from a clean checkout (available after ticket #2).
3. Run the clean offline acceptance from `docs/acceptance.md` (introduced by the last ticket) and confirm it is current.
4. Move the `Unreleased` entries in `CHANGELOG.md` under a dated version heading in a pull request and merge it.
5. Tag the merge commit `vX.Y.Z` and create the GitHub release from the tag.

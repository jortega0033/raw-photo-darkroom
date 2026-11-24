# RAW Photo Darkroom

A planned offline project. Implementation has not started. The repository currently contains the product plan, technical specification and implementation backlog.

## Program goal

Build a RAW photo developer from sensor bytes to print: decode real camera files, develop them with a full colour-managed pipeline on CPU and GPU, and manage a large library, with no RAW library underneath.

The program is planned ([#29](https://github.com/jortega0033/raw-photo-darkroom/issues/29)). Phase 1 is the current epic [#1](https://github.com/jortega0033/raw-photo-darkroom/issues/1) and the only phase with tickets.

**Score.** Share of a fixed, licence-clean set of real camera files (many makers and compression schemes) that decode to the same sensor values as an independent reference decoder.

| Phase | Content | Hours (rough) | Issue |
|---|---|---|---|
| 1 | The current epic and its tickets | 26 to 42 | [#1](https://github.com/jortega0033/raw-photo-darkroom/issues/1) |
| 2 | Camera formats | 120 to 200 | [#30](https://github.com/jortega0033/raw-photo-darkroom/issues/30) |
| 3 | Image quality | 100 to 160 | [#31](https://github.com/jortega0033/raw-photo-darkroom/issues/31) |
| 4 | Colour | 80 to 130 | [#32](https://github.com/jortega0033/raw-photo-darkroom/issues/32) |
| 5 | GPU and scale | 100 to 170 | [#33](https://github.com/jortega0033/raw-photo-darkroom/issues/33) |
| 6 | Local editing | 100 to 160 | [#34](https://github.com/jortega0033/raw-photo-darkroom/issues/34) |

About 530 to 860 engineer hours in total: rough estimates, not measurements. The numbers in the score and the finish lines are targets until a run shows them. Only phase 1 has tickets to work; the sub-issues of a later phase are written when it starts. No single session is expected to reach the end.

## Plan

- [Full product plan and acceptance criteria](docs/PRD.md)
- [Technical specification and verification fixtures](docs/TECHNICAL_SPEC.md)
- [Implementation epic](https://github.com/jortega0033/raw-photo-darkroom/issues/1)

## Current status

The fixtures describe expected results for future checks. No working baseline or passing implementation tests are claimed. Required runtime versions and offline dependencies must be checked before the first build.

## Licensing

A license for this project has not been selected. Any upstream reference or adapted code must retain its applicable notices; see the plan.

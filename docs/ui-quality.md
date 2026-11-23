# UI quality rules

Binding for every screen this application ships. Rules 1 and 2 were stated by the owner; rules 3 to 10 were approved by the owner on 2026-11-22 and have the same standing. Recorded in [owner-decisions.md](owner-decisions.md).

1. No thick accent border on one side of a card, callout, alert, list item or quote (for example `border-left: 4px solid <accent>`). Use spacing, type weight, an icon or a full hairline border instead.
2. No soft tinted background with a thin border of the same hue as the default way to mark a status, tag, callout or card. One neutral surface and one clear signal (text, icon or a solid chip) is enough.
3. No gradient text and no purple-to-blue gradient as a default accent.
4. No blur or glass panels, and no drop shadow plus large radius on every card.
5. No emoji used as icons or bullets, and no sparkle marks.
6. No pill or badge on things that are not states. No all-caps, letter-spaced micro labels as section decoration.
7. No centred hero with a slogan in an application screen. Screens open on the user's task.
8. One accent colour, used for the primary action and the current selection. Status colours only for status.
9. Dense, aligned layouts on a consistent spacing scale. No card grid where a table or a list is the right form.
10. User-facing copy is plain and specific: no filler, no exclamation marks, and the same word for the same thing everywhere.

## How they are applied

- A UI ticket starts with the `ui-ux-pro-max` skill (design-system search for the product type) and ends with a check of every changed screen against this page.
- User-facing copy, documentation and pull request text go through the `unslop` skill before the pull request is opened.
- Code Reviewer checks these rules on every UI diff; Frontend Developer, Accessibility Auditor and Software Architect name this page in their checklists.
- Enforcement is by the review gate, not by a script. Rule 1 can be linted; rule 2 cannot be detected reliably from CSS.
- The product also has its own requirements (labelled controls, keyboard stepping, clipping shown in text as well as in the image, pending and rejected states) in [TECHNICAL_SPEC.md](TECHNICAL_SPEC.md); those apply in addition.
- Colours and type come from the shared tokens in [design-tokens.md](design-tokens.md) (`darkroom/static/tokens.css`); new UI uses them and adds no colour literals.

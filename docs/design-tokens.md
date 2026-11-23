# Design tokens

The visual system is the Pipenzo "Flow look": a black page in dark mode, Flow-style alpha layers, one accent (Pipenzo yellow `#FECE02`), red only for danger. Yellow is used for the primary action, the current-step marker and the current selection. Dark is the primary design. The light block in the file is the matching light theme.

- File: `darkroom/static/tokens.css`, an unedited copy of `extension/sidepanel/tokens.css` in [jortega0033/clip-to-reel-studio](https://github.com/jortega0033/clip-to-reel-studio) at commit `a13378ce73e5b27213c9a200fc960ec93afef054` (2026-11-21). Its header comment holds the contrast numbers and the usage rules.
- Resync: copy the file over `darkroom/static/tokens.css`. Nothing else. Never edit the copy here; a change belongs in the source repository.
- Rule: new UI uses these tokens. No new colour literals in CSS or JavaScript. Canvas or inline colours in JavaScript are read with `getComputedStyle(document.documentElement).getPropertyValue('--token')`. A colour that is data (a pixel value from the engine) is not a style colour and stays as data.
- Light and dark: the light values are in `:root`; the dark values are in a block under the operating system colour scheme query (`prefers-color-scheme: dark`). The page follows the operating system. There is no in-page switch.
- Precedence: the header comment of `tokens.css` is narrower than the rules below (it lists yellow only on the primary button, the current-step node and a few chips, and has no rule for selection or focus). It stays as it is because the copy must stay identical to the source. Where the header and this document differ, this document takes precedence.
- Accent: one accent colour, `--primary` with `--on-primary` text, per `docs/ui-quality.md` rule 8 read with decision D1. It marks the primary action, the current-step marker (this application has no step tracker, so none exists yet) and the current selection. Status colours are used for status only. Text never sits on a bare alpha layer; use the solid surface tokens.
- Current selection (decision D1, in [owner-decisions.md](owner-decisions.md), entry 14): a selected revision, control or list row is filled solid with `--primary` and its text uses `--on-primary`. A yellow border alone is not enough, because yellow is about 1.5:1 against white on light. A selection also carries a second sign that is not colour (weight, an icon or text) and the existing aria attribute (`aria-selected`, `aria-pressed`, `aria-current` or `aria-checked`, whichever fits). Never a tint with a border of the same hue, and never a thick one-sided border (rules 1 and 2). While a selection is shown this way, `--state-selected` is not used to mark it. `--state-hover` stays neutral.
- Focus ring (decision D2): `--focus` is a focus indicator, not an accent use, so it is exempt from the one-accent limit, including where it is yellow in the dark block. A ticket that says the focus style stays unchanged means the rule on main after the token pull request. Here main has only the `--focus` token (its comment mentions a 3px ring); there is no focus style until `app.css` is added in ticket work.
- Themes (decision D3): contrast checks and no-colour-alone checks cover both the light block (`:root`) and the dark block (under `prefers-color-scheme: dark`) of `tokens.css`. A selection that passes in one theme only fails the check.
- Status of the page: there is no page yet; `darkroom/static/` holds only the tokens. The page starts in ticket #15. Screens built in ticket work follow these rules from the start.
- Wiring (decision D4): a ticket that creates a page or its static-file allowlist links `tokens.css` before any other stylesheet and serves it (the allowlist and its test both include it). Concretely, the allowlist (#14) includes `tokens.css`; `index.html` (#15) links `tokens.css` with `<link rel="stylesheet">` before `app.css`; `app.css` and `app.js` only reference `var(--token)`. Until #14 and #15 land there is no page, so nothing is served or linked yet.
- Not used here: the glass, blur and gradient tokens (`--glass*`, `--blur`, `--grad-*`) belong to the source product. `docs/ui-quality.md` rules 3 and 4 forbid blur or glass panels and gradient accents, so this application leaves them unused.

## Tokens by role

| Role | Tokens |
|---|---|
| Surfaces | `--bg`, `--bg-raised`, `--surface`, `--bg-sunken`, `--hero-bg`, `--ink` |
| Text | `--fg`, `--muted`, `--faint`, `--on-hero`, `--on-hero-muted`, `--on-ink`, `--on-ink-muted`, `--on-media` |
| Lines and focus | `--border`, `--hairline`, `--control-border`, `--input-border`, `--hero-border`, `--hero-chip-border`, `--ink-border`, `--focus`, `--ring-accent` |
| Accent | `--primary`, `--primary-press`, `--primary-edge`, `--on-primary` |
| Status | `--ok`, `--ok-bg`, `--warn-fg`, `--warn-bg`, `--danger`, `--danger-bg`, `--success`, `--info` |
| Interaction layers | `--state-hover`, `--state-selected`, `--btn-secondary`, `--btn-secondary-border`, `--ink-hover`, `--scrim` |
| Type | `--font`, `--font-display`, `--mono` |
| Space, radius, motion | `--space-1`, `--radius-control`, `--radius-card`, `--radius-chip`, `--radius-hero`, `--radius-media`, `--radius-pill`, `--dur-1`, `--ease-in-out`, `--ease-out` |
| Shadow | `--shadow-1`, `--shadow-2`, `--shadow-3`, `--shadow-float`, `--shadow-on-video`, `--shadow-on-video-lg`, `--hero-shadow` |
| Unused here | `--glass`, `--glass-strong`, `--glass-border`, `--glass-highlight`, `--glass-video`, `--glass-video-border`, `--blur`, `--grad-canvas`, `--grad-ink`, `--grad-scrim-bottom` |

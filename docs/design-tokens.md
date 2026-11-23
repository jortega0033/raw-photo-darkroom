# Design tokens

The visual system is the Pipenzo "Flow look": a black page in dark mode, Flow-style alpha layers, one accent (Pipenzo yellow `#FECE02`), red only for danger. Dark is the primary design. The light block in the file is the matching light theme.

- File: `darkroom/static/tokens.css`, an unedited copy of `extension/sidepanel/tokens.css` in [jortega0033/clip-to-reel-studio](https://github.com/jortega0033/clip-to-reel-studio) at commit `a13378ce73e5b27213c9a200fc960ec93afef054` (2026-11-21). Its header comment holds the contrast numbers and the usage rules.
- Resync: copy the file over `darkroom/static/tokens.css`. Nothing else. Never edit the copy here; a change belongs in the source repository.
- Rule: new UI uses these tokens. No new colour literals in CSS or JavaScript. Canvas or inline colours in JavaScript are read with `getComputedStyle(document.documentElement).getPropertyValue('--token')`. A colour that is data (a pixel value from the engine) is not a style colour and stays as data.
- Light and dark: the light values are in `:root`; the dark values are in a block under the operating system colour scheme query (`prefers-color-scheme: dark`). The page follows the operating system. There is no in-page switch.
- Accent: `--primary` (with `--on-primary` text) is used on the primary action only. This application has no step tracker, so there is no current-step marker; `--primary` has exactly one use. `docs/ui-quality.md` rule 8 ("the primary action and the current selection") maps as follows: the primary action is filled with `--primary`; the current selection (a selected revision, control or list row) uses the neutral `--state-selected` layer over a solid surface token, never yellow. Text never sits on a bare alpha layer; use the solid surface tokens.
- Wiring: the static-file allowlist (#14) includes `tokens.css`; `index.html` (#15) links `tokens.css` with `<link rel="stylesheet">` before `app.css`; `app.css` and `app.js` only reference `var(--token)`. Until #14 and #15 land there is no page, so nothing is served or linked yet.
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

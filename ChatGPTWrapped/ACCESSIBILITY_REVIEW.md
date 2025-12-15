# Accessibility Review: Colour Blindness & Readability

This document summarizes a quick desktop review of the Streamlit UI focusing on colour blindness resilience and overall readability. It is based on a static review of the theme (`src/theme.py`) and CSS overrides (`src/ui_helpers.py`).

## Palette observations
- **Data colours (`src/theme.py`):** The palette mixes blues, greens, oranges, reds, and purples (`#418AB3`, `#A6B727`, `#F69200`, `#123552`, `#FEC306`, `#DF5327`, `#9D44B5`, `#6E0D25`). These hues include red/green and orange combinations that can collide under deuteranopia/protanopia. Stacked pies/bars and timelines that rely on colour alone will be ambiguous. Consider a colour-blind-safe set (e.g., Okabe–Ito) or add patterned fills / markers per series.
- **Heatmap scale:** The single-hue blue gradient (`HEATMAP_BLUE_SCALE`) maintains monotonic luminance, which is generally safe for CVD users.

## Readability and contrast
- **Background overlays:** The hero and cards layer radial gradients and `color-mix` overlays on top of light backgrounds. Because text inherits `var(--text)` (`#123552`) while muted copy uses `#5b6e80`, contrast is adequate on plain white but can dip against mixed backgrounds (e.g., `.hero__glow`, `.card:before`). Consider simplifying backgrounds or raising text weight/contrast on gradient areas.
- **Sidebar controls:** Buttons and pills use pastel fills (`color-mix` with `var(--accent)`/white) and thin borders. Default text (`#123552`) over light gradients should meet contrast, but disabled or secondary text (`--muted`) may fall below WCAG AA on the gradient sidebar. Increasing border weight and darkening muted text would help.
- **Chart labels:** Plotly inherits `TEXT_COLOR` (`#123552`) on `BACKGROUND_COLOR` (`#f5f8fb`), which is high contrast. Legends remain colour-coded; add direct value labels or textures to reduce reliance on colour.

## UX recommendations
- Provide non-colour encodings: add data labels or shapes in Plotly charts (e.g., patterns for categories, markers for roles) so users can distinguish series without hue.
- Offer a high-contrast mode: expose a toggle that swaps `DATA_COLORS` for a colour-blind-safe palette and boosts `--muted`/border colours.
- Check focus and hover states: ensure interactive elements (tabs, buttons, downloads) have visible focus outlines; current styles override defaults.
- Validate contrast with tooling: run the UI through a contrast checker (e.g., axe, WCAG contrast) using real screenshots to verify that gradient overlays do not drop below AA.

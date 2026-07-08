# UI Tokens

## Design Direction

The product analyzes real pigment (lip RGB) to recommend real pigment (lipstick shades) — color _is_ the content, not decoration. The palette is built around that: a warm porcelain base (like a lit vanity mirror), deep berry as the primary pigment color, and warm champagne as a premium accent. Text uses a warm near-black with a plum undertone instead of pure black, so nothing in the UI ever competes with the actual shade swatches being analyzed.

Display type is an editorial serif (beauty-magazine confidence) paired with a clean grotesk body face and a mono face reserved strictly for data — RGB values, confidence scores, hex codes — so numbers always read as measurements, not styling.

---

## Color Palette

| Token                  | Hex       | Role                                                            |
| ---------------------- | --------- | --------------------------------------------------------------- |
| `--background`         | `#FBF3EF` | App background — warm porcelain, not pure cream                 |
| `--surface`            | `#FFFFFF` | Cards, panels, upload dropzone                                  |
| `--surface-muted`      | `#F3E7E2` | Secondary surface — nested cards, table stripes                 |
| `--ink`                | `#2B1B21` | Primary text — warm near-black with plum undertone              |
| `--ink-muted`          | `#6E5A61` | Secondary text, captions, helper text                           |
| `--primary`            | `#8C2F45` | Deep berry — primary actions, active nav, brand mark            |
| `--primary-foreground` | `#FBF3EF` | Text/icons on primary                                           |
| `--accent`             | `#C9A46A` | Champagne gold — confidence scores, highlights, premium accents |
| `--accent-foreground`  | `#2B1B21` | Text/icons on accent                                            |
| `--border`             | `#E6D5CE` | Default border, dividers                                        |
| `--success`            | `#5B7A5A` | Upload success, completed analysis                              |
| `--warning`            | `#B8823E` | Low confidence, file size warnings                              |
| `--error`              | `#B23B4D` | Failed detection, validation errors                             |
| `--focus-ring`         | `#8C2F45` | Keyboard focus outline — always visible, never removed          |

### Lip Type Swatches (semantic, tied to model output)

These map 1:1 to the three MobileNetV2 labels. Never re-theme these per feature — they are the product's ground truth, always literal.

| Token                 | Hex       | Label    |
| --------------------- | --------- | -------- |
| `--lip-type-pinkish`  | `#E1849C` | Pinkish  |
| `--lip-type-brownish` | `#9C6B4F` | Brownish |
| `--lip-type-dark`     | `#4A1F2B` | Dark     |

---

## CSS Variables (root)

```css
:root {
  /* Base */
  --background: #fbf3ef;
  --surface: #ffffff;
  --surface-muted: #f3e7e2;
  --ink: #2b1b21;
  --ink-muted: #6e5a61;

  /* Brand */
  --primary: #8c2f45;
  --primary-foreground: #fbf3ef;
  --accent: #c9a46a;
  --accent-foreground: #2b1b21;

  /* Structure */
  --border: #e6d5ce;
  --focus-ring: #8c2f45;

  /* Status */
  --success: #5b7a5a;
  --warning: #b8823e;
  --error: #b23b4d;

  /* Lip type (semantic, literal) */
  --lip-type-pinkish: #e1849c;
  --lip-type-brownish: #9c6b4f;
  --lip-type-dark: #4a1f2b;

  /* Radius */
  --radius-sm: 6px;
  --radius-md: 12px;
  --radius-lg: 20px;
  --radius-full: 999px;

  /* Shadow */
  --shadow-sm: 0 1px 2px rgba(43, 27, 33, 0.06);
  --shadow-md: 0 4px 16px rgba(43, 27, 33, 0.08);
  --shadow-lg: 0 12px 32px rgba(43, 27, 33, 0.12);

  /* Motion */
  --ease-out: cubic-bezier(0.16, 1, 0.3, 1);
  --duration-fast: 120ms;
  --duration-base: 220ms;
  --duration-slow: 400ms;
}

@media (prefers-color-scheme: dark) {
  /* Not in MVP scope — reserved for Phase 2 */
}
```

Tailwind config maps each variable via `hsl(var(--token))` or direct `var(--token)` reference — components must reference the token name (e.g. `bg-[var(--primary)]` or a mapped Tailwind class like `bg-primary`), never a raw hex value or a default Tailwind palette class like `bg-rose-500`.

---

## Typography

| Role      | Typeface                              | Usage                                                                                 |
| --------- | ------------------------------------- | ------------------------------------------------------------------------------------- |
| Display   | **Fraunces** (variable, optical size) | Landing hero, section headers, shade names on result cards                            |
| Body      | **General Sans**                      | UI text, buttons, forms, navigation                                                   |
| Data/Mono | **IBM Plex Mono**                     | RGB values, confidence %, hex codes, timestamps — reserved strictly for measured data |

### Type Scale

| Token               | Size / Line Height | Weight          | Usage                         |
| ------------------- | ------------------ | --------------- | ----------------------------- |
| `--text-display-xl` | 56px / 60px        | 500 (Fraunces)  | Landing hero headline         |
| `--text-display-lg` | 36px / 42px        | 500 (Fraunces)  | Page titles ("Your Result")   |
| `--text-display-md` | 24px / 30px        | 500 (Fraunces)  | Card headers, shade names     |
| `--text-body-lg`    | 18px / 28px        | 400             | Lead paragraphs, empty states |
| `--text-body-md`    | 15px / 24px        | 400             | Default UI text               |
| `--text-body-sm`    | 13px / 20px        | 400             | Captions, helper text, labels |
| `--text-data-md`    | 15px / 24px        | 500 (Plex Mono) | RGB values, scores            |
| `--text-data-sm`    | 12px / 18px        | 500 (Plex Mono) | Timestamps, hex codes         |

---

## Spacing Scale

4px base unit — all spacing must be a multiple of 4.

| Token        | Value |
| ------------ | ----- |
| `--space-1`  | 4px   |
| `--space-2`  | 8px   |
| `--space-3`  | 12px  |
| `--space-4`  | 16px  |
| `--space-6`  | 24px  |
| `--space-8`  | 32px  |
| `--space-12` | 48px  |
| `--space-16` | 64px  |
| `--space-24` | 96px  |

---

## Radius

| Token           | Value | Usage                                  |
| --------------- | ----- | -------------------------------------- |
| `--radius-sm`   | 6px   | Inputs, small buttons, tags            |
| `--radius-md`   | 12px  | Cards, dropzone, modals                |
| `--radius-lg`   | 20px  | Hero panels, feature cards             |
| `--radius-full` | 999px | Avatar, color swatch dots, pill badges |

---

## Elevation

| Token         | Usage                                                      |
| ------------- | ---------------------------------------------------------- |
| `--shadow-sm` | Resting cards (history list items, nav)                    |
| `--shadow-md` | Hover state, dropdown menus                                |
| `--shadow-lg` | Modals, the recommendation result card on `/analysis/[id]` |

---

## Motion

| Token             | Value | Usage                                             |
| ----------------- | ----- | ------------------------------------------------- |
| `--duration-fast` | 120ms | Button press, hover                               |
| `--duration-base` | 220ms | Card transitions, tab switches                    |
| `--duration-slow` | 400ms | Pipeline progress step transitions, result reveal |

The analysis pipeline (`AnalysisProgress.tsx`) is the one place motion is allowed to be expressive — it should visibly step through Face Detection → Lip Segmentation → Classification → Recommendation as distinct beats, since that sequence is real backend work, not a generic spinner. Everywhere else, motion stays quiet and functional.

---

## Component Token Usage Notes

- **Color swatch chips** (recommendation cards, RGB preview): always rendered as a solid-fill circle (`--radius-full`) using the _actual_ extracted or recommended RGB value inline — this is the one place raw computed color values are permitted outside the token file, since the color itself is user data, not styling.
- **Confidence score**: rendered in `--text-data-md` (Plex Mono) using `--accent` when ≥90%, `--ink-muted` when below — never colored with `--success`/`--error`, since it's a measurement, not a status.
- **Lip type badge**: background uses the matching `--lip-type-*` token at 15% opacity, text uses the full-opacity token value.
- **Similarity score bar** (Top-3 ranking): fill uses `--primary`, track uses `--surface-muted`.

---

## Invariants

- No raw hex values or default Tailwind palette classes (e.g. `text-pink-500`, `bg-rose-100`) in any component — always reference a token above.
- `--lip-type-*` tokens are semantic and literal: never reused for anything other than displaying the actual classified lip type.
- Mono (`IBM Plex Mono`) is reserved for measured/computed data only — never used for UI labels or buttons.
- `--focus-ring` is never removed or overridden — every interactive element keeps a visible keyboard focus state.
- Motion beyond `--duration-slow` is not permitted anywhere in the MVP.

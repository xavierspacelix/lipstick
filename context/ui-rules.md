# UI Rules

Concise rules for building the AI Lipstick Recommendation System UI. `ui-tokens.md` is the source of truth for colors, type scale, spacing, radius, and motion — this file covers layout and component patterns built on top of those tokens, so the UI stays consistent without over-specifying every detail.

---

## Font

Always import all three typefaces via `next/font/google` in the root layout.

```typescript
import { Fraunces, IBM_Plex_Mono } from "next/font/google";
import localFont from "next/font/local"; // if General Sans is self-hosted

const fraunces = Fraunces({
  subsets: ["latin"],
  variable: "--font-display",
  axes: ["opsz"],
});
const plexMono = IBM_Plex_Mono({
  subsets: ["latin"],
  weight: ["500"],
  variable: "--font-mono",
});
// General Sans → --font-sans
```

Apply all font variable classes to the `<html>` tag in root layout. Never fall back to system fonts, and never use `IBM Plex Mono` outside RGB values, confidence scores, hex codes, or timestamps — see Invariants in `ui-tokens.md`.

---

## Layout

- Page max-width: 1120px, centered (tighter than a generic dashboard — this product is photo- and card-centric, not data-dense)
- Main content area padding: `--space-8` (32px) desktop, `--space-4` (16px) mobile
- Gap between page sections: `--space-8` (32px)
- Header height: 64px, full width, `--surface` background, `--border` bottom hairline, padding `0 24px`
- Desktop: fixed top navbar, no sidebar
- Mobile: bottom navigation bar replaces top navbar's nav items; header shrinks to logo + profile avatar only

---

## Navigation

Nav items: **Dashboard**, **Analyze**, **History**, **Profile** (per `project-overview.md`).

- Active item: `color: var(--primary)`, font-weight 500, `--text-body-md`
- Inactive item: `color: var(--ink-muted)`, font-weight 500, `--text-body-md`
- No underline, no pill background — active state is color change only
- Navbar/bottom nav always `var(--surface)` background, never transparent or blurred
- Bottom nav (mobile): icon + label, active icon filled in `--primary`, inactive icon outlined in `--ink-muted`

---

## Cards

Every content section — dashboard widgets, the result card, history items, forms — lives in a card.

```css
background: var(--surface);
border: 1px solid var(--border);
border-radius: var(
  --radius-md
); /* var(--radius-lg) for hero panels and the result card */
padding: var(--space-6);
box-shadow: var(
  --shadow-sm
); /* var(--shadow-lg) for the /analysis/[id] result card and modals */
```

Never use a colored or tinted card background. Color enters a card only through: lip type badges, swatch chips, score bars, and text — never the card surface itself.

---

## Typography Hierarchy

Follow the type scale from `ui-tokens.md` directly — do not introduce new sizes.

| Use                                    | Token                   |
| -------------------------------------- | ----------------------- |
| Landing hero headline                  | `--text-display-xl`     |
| Page titles ("Your Result", "History") | `--text-display-lg`     |
| Card headers, shade names              | `--text-display-md`     |
| Lead paragraphs, empty-state copy      | `--text-body-lg`        |
| Default UI text, forms, nav            | `--text-body-md`        |
| Captions, helper text, labels          | `--text-body-sm`        |
| RGB values, confidence, scores         | `--text-data-md` (mono) |
| Timestamps, hex codes                  | `--text-data-sm` (mono) |

Never pair Fraunces with anything other than 500 weight, and never use more than one font weight inside a single UI element (e.g. a button label is never mixed-weight).

---

## Badges

**Lip type badge** (Pinkish / Brownish / Dark):

```css
border-radius: var(--radius-full);
padding: 2px 10px;
font-size: 12px;
font-weight: 500;
background: var(--lip-type-{type}) at 15% opacity;
color: var(--lip-type-{type}); /* full opacity */
```

**Confidence score**: not a badge — rendered as plain `--text-data-md` (Plex Mono) text next to the lip type badge. Color is `var(--accent)` when confidence ≥90%, `var(--ink-muted)` when below. Never render confidence with `--success` or `--error` — it's a measurement, not a status.

**Status badges** (upload success, analysis failed): pill-shaped, `var(--success)` / `var(--error)` background at 15% opacity with full-opacity text, same shape as lip type badges.

---

## Buttons

**Primary button:**

```css
background: var(--primary);
color: var(--primary-foreground);
border-radius: var(--radius-sm);
padding: 8px 20px;
font-size: 14px;
font-weight: 500;
```

**Secondary button:**

```css
background: var(--surface);
border: 1px solid var(--border);
color: var(--ink);
border-radius: var(--radius-sm);
padding: 8px 20px;
```

**Destructive action** (delete history item): same shape as secondary, `color: var(--error)`, `border: 1px solid var(--error)` at 40% opacity.

Every button keeps `var(--focus-ring)` visible on keyboard focus — never remove it.

---

## Form Inputs

Used on Register, Login, Profile, and Password forms.

```css
background: var(--surface);
border: 1px solid var(--border);
border-radius: var(--radius-sm);
padding: 8px 12px;
font-size: 15px; /* --text-body-md */
color: var(--ink);
placeholder-color: var(--ink-muted);
focus:
  2px ring var(--focus-ring),
  border-color var(--primary);
```

Validation error text sits directly below the field in `--text-body-sm`, `color: var(--error)` — never a raw exception string (see Do Nots).

---

## Upload Dropzone

The entry point to the entire product (`UploadDropzone.tsx`) — treat it as a hero element, not a generic file input.

```css
background: var(--surface);
border: 2px dashed var(--border);
border-radius: var(--radius-md);
padding: var(--space-16) var(--space-8);
```

- Drag-over state: border becomes `var(--primary)`, background tints to `var(--surface-muted)`
- Once an image is selected: show preview thumbnail inline, replacing the dropzone prompt, not in a separate card
- File-size/type violations show inline as `--warning` (size) or `--error` (unsupported type) text directly under the dropzone — never a browser-native alert

---

## Analysis Progress (Pipeline Stepper)

`AnalysisProgress.tsx` is the one place motion is allowed to be expressive per `ui-tokens.md` — it must visibly step through **Face Detection → Lip Segmentation → Classification → Recommendation** as four distinct beats using `--duration-slow`, not a generic spinner. Completed steps use `var(--success)`, the active step uses `var(--primary)`, pending steps use `var(--ink-muted)`.

---

## Color Swatch Chips

Used for extracted lip RGB and recommended lipstick shades.

```css
border-radius: var(--radius-full);
width/height: 32px (list context) or 48px (result card);
background: rgb(
  r,
  g,
  b
); /* the actual extracted/recommended value — the one permitted
                              raw-color exception, since the color itself is user data */
```

Always paired with the mono RGB or hex value in `--text-data-sm` next to the chip — never the chip alone.

---

## Similarity Score Bar

Used on Top-3 recommendation ranking.

```css
height: 4px;
border-radius: var(--radius-full);
track-background: var(--surface-muted);
fill: var(--primary);
```

Fill width = similarity score (0–1) as a percentage. Score value itself renders as `--text-data-md` mono text beside the bar, not inside it.

---

## History List

History is a **list of cards**, not a data table — each analysis is a photo-led record, not a row of fields.

- No alternating row backgrounds — every item is its own card per the Cards section
- Card contents: thumbnail (cropped lip or original), lip type badge, top recommendation shade name, date in `--text-data-sm`
- Hover state: `box-shadow` steps up from `--shadow-sm` to `--shadow-md`
- Row separation comes from card spacing (`--space-4` between items), never a border-only table row

---

## Empty States

Every section that can be empty (History, Recent Analyses on Dashboard) must have one. Keep it minimal:

- Short descriptive copy in `--text-body-lg`, `color: var(--ink-muted)`
- Optional illustrative icon above the text, using `--ink-muted` or `--border` tones only — never a swatch color, since no color-coded UI element should imply a real lipstick result
- CTA button ("Analyze your first photo") when there's a logical next action

---

## Styling Approach

All tokens live as CSS variables in `:root` (see `ui-tokens.md`) and are mapped in the Tailwind config via `var(--token)` or `hsl(var(--token))`. Components reference token names or mapped Tailwind classes (`bg-primary`, `text-ink-muted`) — never a raw hex value and never a default Tailwind palette class.

---

## Do Nots

- Never use a raw hex value or default Tailwind palette class (`bg-rose-500`, `text-pink-400`) — always reference a token, except the one documented exception: swatch chips rendering actual extracted/recommended RGB.
- Never reuse a `--lip-type-*` token for anything other than displaying the literal classified lip type.
- Never use `IBM Plex Mono` for UI labels, buttons, or headings — reserved strictly for measured/computed data.
- Never show a raw error message or stack trace to the user — always map to human-readable copy (e.g. "No face detected — try a clearer, front-facing photo").
- Never color the confidence score with `--success`/`--error` — it is a measurement, not a status.
- Never remove or override `--focus-ring` on any interactive element.
- Never stack more than 2 levels of border radius inside each other (e.g. a pill badge inside a `--radius-lg` card is fine; a pill inside a `--radius-md` card inside another rounded container is not).
- Never use `position: fixed` for anything besides the top navbar / bottom nav.
- Never introduce motion beyond `--duration-slow`, and never make any element besides `AnalysisProgress.tsx` "expressive" — everywhere else motion stays quiet and functional.
- Never render a lipstick recommendation, history item, or analysis result without its paired color swatch chip — color is the content of this product, not decoration.

# UI Registry

Living document. Updated after every component is built. Read this before building any new component — match existing patterns exactly before inventing new ones.

---

## How to Use

Before building any component:

1. Check if a similar component already exists here
2. If yes — match its exact classes
3. If no — build it following `ui-rules.md` and `ui-tokens.md`, then add it here

After building any component — update this file with the component name, file path, and exact classes used.

Component paths follow the structure defined in `architecture.md` (`frontend/components/{layout,landing,dashboard,analysis,history,profile}/`).

---

## Design Language — Glass Beauty

Overall aesthetic: Light, airy, editorial. Glassmorphism surfaces with backdrop blur, warm porcelain background with subtle radial gradient atmosphere, brand colors used sparingly for emphasis.

### Glass Card (Base Pattern)

Used for all card surfaces across the app — auth forms, feature cards, FAQ items, dashboard widgets, history items.

| Property            | Class / Value                                      |
| ------------------- | -------------------------------------------------- |
| Background          | `bg-white/60` or `bg-white/70`                     |
| Border              | `border border-[var(--border-glass)]`              |
| Border radius       | `rounded-[var(--radius-md)]` (16px) or `rounded-[var(--radius-lg)]` (24px) for auth |
| Shadow              | `shadow-[var(--shadow-glass)]` or `shadow-[var(--shadow-glass-lg)]` |
| Backdrop blur       | `backdrop-blur-xl` or `backdrop-blur-sm`           |
| Hover state         | `hover:bg-white/80 hover:shadow-[var(--shadow-glass-lg)]` |

### Background Atmosphere

| Property            | Class / Value                                      |
| ------------------- | -------------------------------------------------- |
| Page background     | `bg-[var(--background)]` (#FBF3EF)                 |
| Ambient glow        | `::before` pseudo-element with radial-gradient in primary/accent at 3-4% opacity |

### Navbar (Floating Glass)

File: `frontend/src/components/layout/Navbar.tsx`

| Property            | Class / Value                                      |
| ------------------- | -------------------------------------------------- |
| Position            | `fixed top-4 left-1/2 -translate-x-1/2 z-50`      |
| Container           | `rounded-[var(--radius-md)] border border-[var(--border-glass)] bg-white/70 shadow-[var(--shadow-glass)] backdrop-blur-xl` |
| Height              | `h-14`                                             |
| Logo                | `font-display text-display-md text-[var(--primary)]` |
| Nav link (active)   | `text-[var(--primary)] bg-[rgba(139,47,69,0.08)] rounded-[var(--radius-sm)]` |
| Nav link (inactive) | `text-[var(--ink-muted)]`                          |
| Desktop             | `hidden md:flex gap-1`                             |

### BottomNav (Floating Glass)

File: `frontend/src/components/layout/BottomNav.tsx`

| Property            | Class / Value                                      |
| ------------------- | -------------------------------------------------- |
| Position            | `fixed bottom-4 left-1/2 -translate-x-1/2 z-50 md:hidden` |
| Container           | Same glass pattern as Navbar                       |
| Icon (active)       | `color: var(--primary), fill: var(--primary)`      |
| Icon (inactive)     | `color: var(--ink-muted), fill: none`              |
| Active tab          | `bg-[rgba(139,47,69,0.08)]`                        |

### Footer

File: `frontend/src/components/layout/Footer.tsx`

| Property            | Class / Value                                      |
| ------------------- | -------------------------------------------------- |
| Background          | `bg-white/40 backdrop-blur-sm`                     |
| Border top          | `border-t border-[var(--border)]/50`               |
| Brand               | `font-display text-display-md text-[var(--primary)]` |
| Text                | `text-body-sm text-[var(--ink-muted)]`             |

### Auth Form (Login / Register)

File: `frontend/src/app/(auth)/login/page.tsx`, `frontend/src/app/(auth)/register/page.tsx`

| Property            | Class / Value                                      |
| ------------------- | -------------------------------------------------- |
| Container           | `rounded-[var(--radius-lg)] border border-[var(--border-glass)] bg-white/60 p-8 shadow-[var(--shadow-glass-lg)] backdrop-blur-xl` |
| Max width           | `max-w-sm`                                         |
| Title               | `font-display text-display-md`                     |
| Description         | `text-body-sm text-[var(--ink-muted)]`             |
| Input               | `border-[var(--border)] bg-white/70 backdrop-blur-sm` |
| Error banner        | `rounded-[var(--radius-sm)] border border-[var(--error)]/20 bg-[var(--error)]/5` |
| Submit button       | shadcn Button primary variant, `w-full`            |
| Footer text         | `text-body-sm text-[var(--ink-muted)]`             |
| Footer link         | `font-medium text-[var(--primary)] hover:underline` |

### Landing Hero

File: `frontend/src/components/landing/Hero.tsx`

| Property            | Class / Value                                      |
| ------------------- | -------------------------------------------------- |
| Tag                 | `rounded-full border border-[var(--border-glass)] bg-white/60 px-4 py-1.5 text-body-sm backdrop-blur-sm` |
| Headline            | `font-display text-display-xl leading-[1.1] tracking-tight` |
| Brand accent        | `text-[var(--primary)]` (block element)            |
| Subtitle            | `text-body-lg text-[var(--ink-muted)] max-w-md`    |
| CTA (primary)       | `bg-[var(--primary)] text-[var(--primary-foreground)] h-12 px-6 rounded-[var(--radius-sm)]` |
| CTA (secondary)     | `border border-[var(--border)] bg-white/60 shadow-[var(--shadow-glass)] backdrop-blur-sm h-12 px-6 rounded-[var(--radius-sm)]` |
| Ambient glow        | Centered radial gradient glow behind hero (3% opacity) |
| Layout              | 2-col grid `md:grid-cols-2` — text left, 3D lipstick right |
| 3D lipstick         | `Lipstick3D` component with mouse-follow tilt via `useMotionValue` + `useSpring` |
| Scroll indicator    | Centered below fold, bouncing `y: [0,6,0]` arrow, `uppercase tracking-[0.15em]` label |

### Landing Features

File: `frontend/src/components/landing/Features.tsx`

| Property            | Class / Value                                      |
| ------------------- | -------------------------------------------------- |
| Icon container      | `h-12 w-12 rounded-[var(--radius-sm)] bg-white/80 shadow-sm backdrop-blur-sm` |
| Icon                | `h-6 w-6 text-[var(--primary)]`                    |
| Card                | Same glass card pattern                            |
| Grid                | `grid gap-6 md:grid-cols-2 lg:grid-cols-4`         |

### Dashboard

File: `frontend/src/app/(main)/dashboard/page.tsx`

| Property            | Class / Value                                      |
| ------------------- | -------------------------------------------------- |
| Header pill         | `rounded-full border border-[var(--border-glass)] bg-white/60 px-3 py-1 text-[11px] font-medium uppercase tracking-wider text-[var(--ink-muted)] backdrop-blur-sm` |
| Title               | `font-display text-display-xl`                     |
| Subtitle            | `text-body-lg text-[var(--ink-muted)]`             |
| Stats card          | `rounded-[var(--radius-md)] border border-[var(--border-glass)] bg-white/60 p-5 shadow-[var(--shadow-glass)] backdrop-blur-sm hover:bg-white/80 hover:shadow-[var(--shadow-glass-lg)]` |
| Stat icon container | `flex h-10 w-10 items-center justify-center rounded-[var(--radius-sm)] bg-white/80 shadow-sm backdrop-blur-sm` |
| Stat label          | `text-body-sm text-[var(--ink-muted)]`             |
| Stat value          | `font-display text-display-md text-[var(--ink)]`   |
| Recent card         | Same glass pattern as stats card, `px-6 py-4` header, `px-6 py-2` list body |
| Recent item         | `flex items-center gap-4 px-2 py-3 rounded-[var(--radius-sm)] hover:bg-[rgba(139,47,69,0.04)]` |
| Recent swatch       | `h-10 w-10 shrink-0 rounded-[var(--radius-sm)]` (inline style with hex) |
| Quick analyze       | `bg-gradient-to-br from-white/70 to-white/40` glass card with radial glow accent |
| Action button       | `inline-flex h-10 items-center gap-2 rounded-[var(--radius-sm)] bg-[var(--primary)] px-5 text-body-sm font-medium text-[var(--primary-foreground)]` |

### Upload & Analysis

File: `frontend/src/app/(main)/analysis/page.tsx`

| Property | Class / Value |
|----------|---------------|
| Page header | Same pill + title + subtitle pattern as dashboard |
| Dropzone (empty) | `rounded-[var(--radius-md)] border-2 border-dashed border-[var(--border)] bg-white/40 p-8 hover:border-[var(--primary)]/50 hover:bg-white/60` |
| Dropzone (drag) | `border-[var(--primary)] bg-[rgba(139,47,69,0.04)]` |
| Dropzone (filled) | `border-[var(--border-glass)] bg-white/60` |
| Icon container | `flex h-16 w-16 items-center justify-center rounded-[var(--radius-sm)] bg-white/80 shadow-sm backdrop-blur-sm` |
| Error banner | `rounded-[var(--radius-sm)] border border-[var(--error)]/20 bg-[var(--error)]/5 px-4 py-2 flex items-center gap-2` |
| File confirm bar | `rounded-[var(--radius-sm)] border border-[var(--border-glass)] bg-white/60 px-4 py-3 shadow-[var(--shadow-glass)] backdrop-blur-sm` |
| Analyze button | `inline-flex h-9 items-center gap-2 rounded-[var(--radius-sm)] bg-[var(--primary)] px-4 text-body-sm font-medium text-[var(--primary-foreground)]` |
| Camera option | `flex w-full items-center justify-center gap-2 rounded-[var(--radius-md)] border-2 border-dashed border-[var(--border)] bg-white/40 px-6 py-4 text-body-sm font-medium text-[var(--ink-muted)] backdrop-blur-sm transition-all duration-base hover:border-[var(--primary)]/50 hover:bg-white/60` |

### CameraCapture (Camera Modal)

File: `frontend/src/components/analysis/CameraCapture.tsx`

| Property | Class / Value |
|----------|---------------|
| Overlay | `fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm` |
| Container | `relative mx-4 w-full max-w-md overflow-hidden rounded-[var(--radius-lg)] bg-[var(--background)] shadow-2xl` |
| Header | `flex items-center justify-between border-b border-[var(--border)]/50 px-4 py-3` |
| Title | `font-display text-display-md text-[var(--ink)]` |
| Close btn | `flex h-8 w-8 items-center justify-center rounded-[var(--radius-sm)] text-[var(--ink-muted)] transition-colors hover:bg-white/60` |
| Video area | `relative aspect-[3/4] bg-black` |
| Controls | `flex items-center justify-center gap-8 px-4 py-5` |
| Capture btn | `flex h-16 w-16 items-center justify-center rounded-full border-4 border-white bg-white/20 transition-colors hover:bg-white/30` |
| Flip btn | `flex h-12 w-12 items-center justify-center rounded-full border border-[var(--border)] bg-white/60 text-[var(--ink-muted)] backdrop-blur-sm transition-colors hover:bg-white/80` |
| Action btns | `rounded-[var(--radius-sm)] px-5 py-2 text-body-sm font-medium` — retake has border, use photo has `bg-[var(--primary)]` |
| Error overlay | `absolute inset-0 flex items-center justify-center bg-black/60 p-6`, text `text-body-sm text-white` |

### Analysis Progress (4-step stepper)

File: `frontend/src/components/analysis/AnalysisProgress.tsx`

| Property | Class / Value |
|----------|---------------|
| Card | Same glass pattern |
| Step icon (done) | `bg-[var(--success)]/10 text-[var(--success)]`, SVG checkmark |
| Step icon (active) | `bg-[var(--primary)]/10 text-[var(--primary)]`, pulsing scale |
| Step icon (pending) | `bg-white/60 text-[var(--ink-muted)]` |
| Progress bar | `h-1.5 w-16 overflow-hidden rounded-full bg-white/60`, inner bar `bg-[var(--primary)]` with infinite width animation |
| Error | Same error banner pattern |

### CroppedLipPreview

File: `frontend/src/components/analysis/CroppedLipPreview.tsx`

| Property | Class / Value |
|----------|---------------|
| Card | Same glass pattern, `p-4` |
| Header | `flex items-center justify-between` — title left, toggle button right |
| Toggle btn | `rounded-[var(--radius-sm)] border border-[var(--border)] bg-white/60 px-3 py-1.5 text-[11px] font-medium uppercase tracking-wider text-[var(--ink-muted)] backdrop-blur-sm transition-colors hover:bg-white/80` |
| Image container | `overflow-hidden rounded-[var(--radius-sm)] bg-white/80` |
| RGB swatch | `h-8 w-8 rounded-[var(--radius-sm)] border border-[var(--border)]` with inline `rgb()` |

### LipAnalysisCard

File: `frontend/src/components/analysis/LipAnalysisCard.tsx`

| Property | Class / Value |
|----------|---------------|
| Card | Same glass pattern, `p-5` |
| Lip type badge | `rounded-[var(--radius-full)] px-3 py-1 text-data-sm font-medium text-white`, bg uses `var(--lip-type-{name})` |
| Confidence bar | `h-2 overflow-hidden rounded-full bg-white/60`, inner `bg-[var(--primary)]` |
| RGB display | Swatch + `font-mono text-data-md text-[var(--ink)]` |

### RecommendationCard

File: `frontend/src/components/analysis/RecommendationCard.tsx`

| Property | Class / Value |
|----------|---------------|
| Card | Same glass pattern, `p-5`, `hover:bg-white/80 hover:shadow-[var(--shadow-glass-lg)]` |
| Swatch | `h-14 w-14 rounded-[var(--radius-sm)] border border-[var(--border)] shadow-sm` |
| Rank badge | `absolute -top-2 -right-2 h-6 w-6 rounded-full bg-white text-[10px] font-bold shadow-sm text-[var(--ink-muted)]` |
| Category pill | `rounded-[var(--radius-full)] px-2.5 py-0.5 text-data-sm font-medium text-white`, bg uses `var(--lip-type-{name})` |
| Score bar | `h-1.5 rounded-full bg-white/60`, inner `bg-[var(--primary)]` with animated width |

### Analysis Result Page

File: `frontend/src/app/(main)/analysis/[id]/page.tsx`

| Property | Class / Value |
|----------|---------------|
| Layout | 3-col grid `lg:grid-cols-3` — left sidebar (1 col) + recommendations (2 col) |
| Loading state | Centered spinning `RefreshCw` icon `text-[var(--primary)]` |
| Error state | `rounded-[var(--radius-md)] border border-[var(--error)]/20 bg-[var(--error)]/5 p-6 text-center` |
| Back link | `inline-flex items-center gap-1.5 text-body-sm text-[var(--ink-muted)] hover:text-[var(--ink)]` |

### History

File: `frontend/src/app/(main)/history/page.tsx`

| Property | Class / Value |
|----------|---------------|
| Page header | Same pill + title + subtitle pattern as dashboard |
| Container | `mx-auto max-w-[800px]` |

### HistoryItem

File: `frontend/src/components/history/HistoryItem.tsx`

| Property | Class / Value |
|----------|---------------|
| Card | Same glass pattern, `px-5 py-4`, `hover:bg-white/80 hover:shadow-[var(--shadow-glass-lg)]` |
| Color dot | `h-10 w-10 rounded-[var(--radius-sm)]` with inline bg from lip type color map |
| Lip type badge | Same pattern as analysis card |
| Date | `text-body-sm text-[var(--ink-muted)]` formatted via `toLocaleDateString` |
| Delete btn | `h-8 w-8 rounded-[var(--radius-sm)] text-[var(--ink-muted)] opacity-0 group-hover:opacity-100 hover:bg-[var(--error)]/10 hover:text-[var(--error)]` |
| View btn | `h-8 w-8 rounded-[var(--radius-sm)] hover:bg-[rgba(139,47,69,0.08)] hover:text-[var(--primary)]` |
| Loading skeleton | `animate-pulse rounded-[var(--radius-md)] border border-[var(--border-glass)] bg-white/40 p-5`, inner bars `bg-[var(--border)]/50` |
| Empty state | `p-12 text-center`, icon container `h-16 w-16` with `HistoryIcon`, title `font-display text-display-md`, subtitle `text-body-sm text-[var(--ink-muted)]` |
| Error state | Same error banner pattern |

### Landing FAQ

File: `frontend/src/components/landing/FAQ.tsx`

| Property            | Class / Value                                      |
| ------------------- | -------------------------------------------------- |
| Details wrapper     | Same glass card pattern                            |
| Expand indicator    | `h-6 w-6 rounded-full border border-[var(--border)] bg-white/60 text-sm text-[var(--primary)] group-open:rotate-45` |
| Answer border       | `border-t border-[var(--border)]/50`               |

---

---

## Ambient & Decorative Elements

| Component | File | Pattern |
|-----------|------|---------|
| AmbientBackground | `components/ambient/AmbientBackground.tsx` | Canvas-based animated floating glass orbs (6 orbs, 200-500px, 80-140px blur, primary/accent/brand colors at 5-8% opacity, 0.3px/s drift) |
| Lipstick3D | `components/ambient/Lipstick3D.tsx` | Detailed SVG lipstick (body/cap/bullet/gold metal bands), 4 color variants (primary/pinkish/brownish/dark), mouse-follow 3D tilt via `useMotionValue` + `useSpring` (-15° to 15°), capsule gradient reflections + highlight streak, `preserve-3d` perspective |
| SwatchScatter | `components/ambient/SwatchScatter.tsx` | 8 floating color dots (8-28px, positioned across viewport by %, spring-bob animation with 4-7s cycle, uses all brand lip-type colors) |

All ambient elements use `pointer-events-none fixed inset-0 z-0 overflow-hidden` to stay behind content.

---

## Component Rules

- **Every interactive element** must have visible `var(--focus-ring)` on keyboard focus
- **Never use raw hex values** — always reference CSS variables or Tailwind token classes
- **Never use default Tailwind palette classes** (e.g., `bg-rose-500`, `text-pink-400`)
- **Color swatch chips** (recommendation cards, RGB preview) are the one exception to the hex rule — they render actual extracted/recommended RGB values inline
- **IBM Plex Mono** reserved strictly for measured/computed data (RGB values, confidence scores, timestamps)
- **Ambient/decorative elements** use `pointer-events-none fixed inset-0 z-0` and must never interfere with content or layout

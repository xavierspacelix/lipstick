# Memory — MVP Complete

Last updated: July 8, 2026

## What was built

Full AI Lipstick Recommendation System from scratch across 7 phases (51/51 tasks). Greenfield project — no legacy code.

**Frontend (Next.js 16.2, Tailwind 3.4.19):**
- 11 routes: `/`, `/login`, `/register`, `/dashboard`, `/analysis`, `/analysis/[id]`, `/history`, `/profile`, `/settings`, `/analysis/[id]`, `/_not-found`
- Landing page with glass hero, animated 3D lipstick (mouse-follow), shade showcase, features grid, collapsible FAQ
- Auth pages (login/register) with React Hook Form + Zod, wired to AuthContext
- Dashboard with live stats from API, recent analyses list, quick-analyze CTA
- Analysis page with drag-drop upload, 4-step progress stepper, redirect to result
- Analysis result page (3-col layout: lip preview + analysis card + recommendations)
- History page with API list/delete, loading skeletons, empty state
- Profile page with edit name, change password, sign out
- Settings page (placeholder cards)
- Navbar (desktop, floating glass, user name + logout) + BottomNav (mobile)
- SmoothScroll (Lenis), page transitions (AnimatePresence), ambient canvas background, floating swatch dots, noise texture overlay

**Backend (FastAPI):**
- POST `/api/v1/register`, POST `/api/v1/login` (sets HttpOnly cookies), POST `/api/v1/logout`
- GET/PATCH `/api/v1/profile`, PATCH `/api/v1/profile/password`, GET `/api/v1/profile/stats`
- POST `/api/v1/analysis` (FormData upload → S3 → ai-service → save), GET `/api/v1/analysis/{id}`
- GET `/api/v1/history`, GET `/api/v1/history/{id}`, DELETE `/api/v1/history/{id}`
- SQLAlchemy models, Alembic migration, JWT + bcrypt, S3 storage service

**AI Service (FastAPI, internal port 8001):**
- POST `/pipeline/analyze` — face detection (MediaPipe), lip segmentation, RGB extraction (NumPy), classification (MobileNetV2 + fallback rule), hybrid recommender (18 lipstick entries across 3 categories)

## Decisions made

- **Tailwind 3.4 pinned** — v4 is forbidden (AGENTS.md rule)
- **CSS variables for all colors** — no hardcoded hex values except for color swatch chips (inline style with extracted RGB or brand swatch hexes), and SVG elements inside Lipstick3D component
- **JWT HttpOnly cookies only** — no localStorage for tokens; `credentials: include` on every fetch
- **AI never runs in frontend** — ai-service is internal only, backend orchestrates calls
- **Proxy.ts (Next.js 16 middleware)** — checks `access_token` cookie on protected routes, redirects to `/login`
- **AuthContext** — checks session on mount via `GET /api/v1/profile`, exposes `login/register/logout/refresh`
- **Glass Beauty design** — glassmorphism (backdrop-blur, semi-transparent white backgrounds, soft shadows), warm porcelain `#FBF3EF`, deep berry `#8C2F45`, Fraunces + Geist + IBM Plex Mono
- **PostgreSQL + MinIO as cloud URLs** — no Docker Compose setup

## Problems solved

- **Next.js 16 middleware renamed** — file is `proxy.ts`, not `middleware.ts`, exports `proxy` not `middleware`
- **Next.js 16 params** — dynamic route params are `Promise<{...}>` in server components; used `useParams()` hook for client component result page
- **shadcn/ui v4 components** — needed custom rewrite for Tailwind 3.4 compatibility (v4 of shadcn assumes v4 of Tailwind)
- **Turbopack build** — works clean with current config; no webpack config needed
- **`useScroll` hook inside mapped components** — extracted `ShadeCard` to separate component to avoid hook ordering issues

## Current state

- **All 51 tasks complete.** Build passes clean (11 routes, no errors).
- No running backend or database needed for frontend dev — all API calls gracefully degrade
- Foundation (7), Auth (9), UI Shell (7), Upload & Analysis UI (6), AI Pipeline (8), Results & History (6), Polish (8)

## Next session starts with

Project is feature-complete. Potential next areas:
- Deploy to production (set up PostgreSQL + MinIO + run migrations + start services)
- Add loading/skeleton states to remaining spots if needed
- Add virtual try-on / upload photo of lipstick shade
- Any UX refinements or bug fixes from real usage

## Open questions

- None — project is MVP-complete pending user feedback

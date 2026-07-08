# Memory — Polish, Multi-Photo, Training, Production Prep

Last updated: July 8, 2026

## What was built

**Lipstick database sync:**
- Updated `backend/seed.py` from 18 → 288 entries (matching ai-service)
- Created `GET /api/v1/lipsticks` with optional `?lip_type=` and `?category=` filters
- Created `/shades` frontend page with grid of swatch cards and filter tabs (All/Pinkish/Brownish/Dark)

**Camera capture fix:**
- Rewrote `CameraCapture.tsx` start logic — camera now starts via `useEffect` on mount, not `onLoadedMetadata` (which never fired)
- Added `muted` for mobile autoplay, proper cleanup on unmount

**Multi-photo analysis (max 3):**
- Frontend: 3 photo slots with preview/remove, each clickable for upload or camera
- Backend: accepts `list[UploadFile]` (field `images`), averages RGB, majority-votes lip type, averages confidence
- Created `backend/app/services/recommendation_service.py` — local `get_top3()` without numpy dependency
- Backend runs recommendation on averaged RGB locally (no extra ai-service call)

**Training pipeline:**
- Added `--female-only` flag to `prepare_dataset.py` (filters CelebA by `Male == -1`)
- Fixed Python 3.9 type hint syntax (`Optional[np.ndarray]` instead of `np.ndarray | None`)
- Trained `mobilenetv2_lip.h5` with 3000 female CelebA images — 99.5% val_accuracy (Phase 1 only; Phase 2 fine-tune OOM)

**Production:**
- Dockerfile frontend fixed — `RUN mkdir -p public` ensures build doesn't fail on missing `public/`
- Login redirect fixed — replaced `router.push` with `window.location.href` + added `useEffect` auto-redirect if already authenticated

**Docs:**
- README.md fully rewritten with setup, Docker, API endpoints, pages, lipstick DB info, training guide

**Git:**
- Initialized repo at `/home/xavier/lipstick` with 140 files on `main` branch

## Decisions made

- **Backend runs local recommendation for multi-photo** — avoids extra ai-service call; duplicates 288-entry DB + euclidean distance logic in `recommendation_service.py`
- **Only first image stored** for cropped/brushed preview; additional images discarded after RGB extraction
- **Training Phase 1 only** (frozen MobileNetV2 head) — 99.5% accuracy is sufficient; Phase 2 fine-tune causes OOM
- **window.location.href for login redirect** — `router.push` inconsistently triggers in Next.js 16 App Router after async auth calls
- **No `.env` in git** — `.gitignore` blocks `.env`, commits only `.env.example` with placeholders

## Problems solved

- **Camera blank** — `onLoadedMetadata` never fires when `<video>` has no initial `src`; fixed with `useEffect` + internal `onloadedmetadata` handler
- **Backend numpy import error** — `recommendation_service.py` used `np.linalg.norm` but backend doesn't have numpy; replaced with `math.sqrt`
- **frontend/.git was nested repo** — removed to make frontend a regular directory in monorepo; amended initial commit
- **Docker build failed** — `COPY --from=builder /app/public ./public` fails when `public/` directory is empty; fixed with `RUN mkdir -p public`
- **Python 3.9 union syntax** — `np.ndarray | None` not supported; changed to `Optional[np.ndarray]`

## Current state

- **Backend:** 288 lipstick DB, multi-photo analysis, recommendation service, all endpoints working
- **Frontend:** camera works, 3-photo slots, shades browse page, login redirects properly
- **AI Service:** `mobilenetv2_lip.h5` trained (3000 female CelebA, 99.5% val_acc), rule-based fallback still available
- **Docker:** all 3 Dockerfiles fixed, `docker compose up --build -d` should work
- **Git:** 140 files committed on `main`

## Next session starts with

Deploy to production:
```bash
docker compose up --build -d
```

Or if user reports bugs, continue fixing reported issues.

## Open questions

- None currently — user is deploying and testing

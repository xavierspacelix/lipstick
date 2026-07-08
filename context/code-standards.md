# Code Standards

Implementation rules and conventions for the entire project. The AI agent must follow these in every session without exception. These rules prevent pattern drift across sessions.

---

## Engineering Mindset

The AI agent on this project operates as a senior engineer. This means:

- **Think before implementing** — understand what is being built and why before writing a single line
- **Read context files first** — never assume, always verify against `architecture.md`, `project-overview.md`, and `PRD.md`
- **Scope is sacred** — only build what the current feature requires. MVP scope is fixed in `PRD.md` Section 6 — never build anything listed under "Excluded" (Virtual Try-On, Skin Tone Analysis, Marketplace, etc.)
- **Respect system boundaries** — `frontend/` never touches the DB or storage directly, `ai-service/` never touches the DB or storage directly and never calls `backend/`. See Invariants in `architecture.md`.
- **Every feature must be testable** — if it cannot be verified immediately after implementation, it is incomplete
- **Clean over clever** — simple readable code that a junior developer can understand is always preferred over clever abstractions
- **One thing at a time** — complete one feature fully before touching the next
- **Failures are expected** — wrap every service call and pipeline step in try/except, log failures, never let one failure crash the request or the run

---

## TypeScript (Frontend)

- Strict mode enabled in `tsconfig.json` — no exceptions
- Never use `any` — use `unknown` and narrow the type
- Never use type assertions (`as SomeType`) unless absolutely necessary and commented why
- All function parameters and return types must be explicitly typed
- Use `type` for object shapes and unions — use `interface` only for extendable component props
- All async functions must have proper error handling — never let promises float unhandled
- Use `const` by default — only use `let` when reassignment is necessary
- Shared types (`Analysis`, `Lipstick`, `User`) live in `types/index.ts` only — never redeclared locally in a component

---

## Next.js 15 Conventions

- App Router only — no Pages Router
- Components are Server Components by default
- Only add `"use client"` when the component requires:
  - `useState` / `useReducer` (e.g. `UploadDropzone.tsx`, form components)
  - `useEffect`
  - Browser APIs (drag & drop, file preview via `FileReader`)
  - Event listeners
  - Third-party client-only libraries
- Never add `"use client"` to layout files unless absolutely required
- Data fetching happens in Server Components via `lib/api-client.ts` — never fetch directly inside Client Components; pass server-fetched data down as props
- Since the JWT lives in an HttpOnly cookie, Server Components cannot read it via `document.cookie` — always forward it explicitly using `next/headers` `cookies()` when calling the backend from the server
- `middleware.ts` is the only place that checks the session cookie for route protection (`/dashboard`, `/analysis`, `/analysis/[id]`, `/history`, `/profile`, `/settings`) — never duplicate this check ad hoc inside pages
- The frontend contains **no business logic** — it calls `backend/` endpoints and renders the response. Any logic beyond formatting/display belongs in `backend/services/`
- Always read Next.js documentation before implementing a Next.js-specific feature — APIs may differ from training data

---

## Python / FastAPI Conventions (Backend & AI Service)

- Type hints are mandatory on every function signature — no untyped `def`
- All request/response shapes are Pydantic schemas in `schemas/` — never raw `dict` across a route boundary
- Never use bare `except:` — always catch a specific exception or `Exception` with logging
- Route handlers (`api/v1/*.py`) contain **no business logic** — they validate input, call a service function, and return the result. All logic lives in `services/`
- Only the service layer talks to the database — no raw SQLAlchemy queries from route handlers (see Invariants in `architecture.md`)
- Every route under `/analysis`, `/history`, and `/profile` depends on `get_current_user`, and every query is scoped with `WHERE user_id = current_user_id` — never query without a user filter
- `ai-service/` never imports from `backend/` and never touches PostgreSQL or Object Storage — it only receives an image and returns pipeline output over HTTP
- Async everywhere: FastAPI routes, service functions, and the `httpx` call from `backend/` to `ai-service/` are all `async def`
- Passwords are always hashed with bcrypt before persistence — never logged, never stored in plaintext

---

## File and Folder Naming

**Frontend**

- Folders: kebab-case — `analysis`, `history`
- Component files: PascalCase — `RecommendationCard.tsx`, `AnalysisProgress.tsx`
- Utility files: camelCase — `apiClient.ts` (as `api-client.ts` per `architecture.md`), `authHelpers.ts`
- Type files: camelCase — `index.ts`
- One component per file — never export multiple components from one file
- Index files only in `components/ui/` (shadcn/ui) — never barrel export from other folders

**Backend & AI Service**

- Folders and files: snake_case — `analysis_service.py`, `lip_segmentation.py`
- Route files: match the resource name — `auth.py`, `analysis.py`, `history.py`, `profile.py`
- Service files: always suffixed `_service.py` — `storage_service.py`, `recommendation_service.py`
- Model files (SQLAlchemy): singular, snake_case — `user.py`, `analysis.py`, `lipstick.py`
- Pipeline step files (AI service): named after the step — `face_detection.py`, `rgb_extraction.py`, `classifier.py`, `recommender.py`

---

## Component Structure (Frontend)

Every component follows this exact order:

```typescript
"use client"; // only if needed

// 1. External imports
import { useState } from "react";
import { Button } from "@/components/ui/button";

// 2. Internal imports
import { ColorSwatch } from "@/components/analysis/ColorSwatch";

// 3. Type definitions
type Props = {
  shadeName: string;
  category: string;
  score: number;
  rgb: { r: number; g: number; b: number };
};

// 4. Component
export function RecommendationCard({ shadeName, category, score, rgb }: Props) {
  // state
  // derived values
  // handlers
  // return JSX
}
```

- Never use default exports for components — always named exports
- Props type defined directly above the component — not in a separate types file unless shared
- No inline styles and no raw hex values — all styling via Tailwind classes referencing the CSS variables defined in `ui-tokens.md`, following `ui-rules.md` component patterns

---

## Backend API Route Handlers

```python
# app/api/v1/analysis.py

from fastapi import APIRouter, Depends, HTTPException, UploadFile
from app.core.security import get_current_user
from app.services import analysis_service
from app.services.analysis_service import AnalysisError

router = APIRouter()

@router.post("/analysis")
async def create_analysis(
    image: UploadFile,
    user_id: str = Depends(get_current_user),
):
    try:
        image_bytes = await image.read()
        result = await analysis_service.run_analysis(user_id, image_bytes)
        return result
    except AnalysisError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"[analysis] {e}")
        raise HTTPException(status_code=500, detail="Analysis failed")
```

- Every route handler wraps its service call in try/except
- Domain errors (e.g. `AnalysisError("No face detected")`) map to `400` with a human-readable `detail`
- Unexpected errors are logged with the route path as prefix — `[analysis]` — and return a generic `500` message, never the raw exception
- File validation (type, size ≤10MB per `PRD.md` Section 8) happens before any pipeline call, inside `utils/validators.py`

---

## AI Pipeline Functions

```python
# ai-service/app/pipeline/recommender.py

def get_top3(lip_type: str, lip_rgb: tuple, lipsticks: list) -> list:
    try:
        candidates = rule_based_candidates(lip_type, lipsticks)
        scored = [
            {**ls, "score": content_based_score(lip_rgb, (ls["rgb_r"], ls["rgb_g"], ls["rgb_b"]))}
            for ls in candidates
        ]
        return sorted(scored, key=lambda x: x["score"], reverse=True)[:3]
    except Exception as e:
        print(f"[pipeline/recommender] {e}")
        raise
```

- Every pipeline step (`face_detection`, `lip_segmentation`, `rgb_extraction`, `classifier`, `recommender`) is a pure function: image/data in, typed result out — no side effects, no DB, no storage
- The top-level orchestrator in `ai-service/app/main.py` is the single place that catches pipeline failures and turns them into the `{ face_detected, cropped_lip, rgb, lip_type, confidence, recommendations }` response consumed by `backend/`
- If face detection fails, the pipeline stops immediately and returns `face_detected: false` — no partial result is ever computed or returned
- The classifier only ever outputs one of the three supported labels: `Pinkish`, `Brownish`, `Dark`
- A completed analysis always returns exactly three recommendations — never more, never fewer, never zero

---

## API Client Usage (Frontend)

```typescript
// Client Components — browser fetch, cookie sent automatically
import { apiClient } from "@/lib/api-client";
const result = await apiClient<Analysis>("/analysis", {
  method: "POST",
  body: formData,
});

// Server Components — must forward the HttpOnly cookie manually
import { cookies } from "next/headers";
const cookieHeader = (await cookies()).toString();
const result = await apiClient<Analysis[]>("/history", {
  headers: { Cookie: cookieHeader },
});
```

- Never use the browser-style call (relying on automatic cookie attachment) inside a Server Component — it has no browser cookie jar
- Always set `credentials: "include"` in `lib/api-client.ts` so the HttpOnly cookie is sent from the browser
- Every backend call goes through `lib/api-client.ts` — never a raw `fetch` scattered across components

---

## Error Handling

- Never use empty catch/except blocks — always log or handle
- Backend and AI service logs always include a context prefix: `[module/function]`
- User-facing errors must be human-readable — never expose raw exception text or stack traces (see `ui-rules.md` Do Nots)
- API route errors return the appropriate HTTP status with a generic `detail` message — never expose internals
- Uploaded images and raw pipeline output are never written to application logs — logs may reference `analysis_id` / `user_id`, never image bytes or PII

---

## Logging & Monitoring

Per the Reliability requirements in `PRD.md` Section 15:

- Every request to `backend/` and `ai-service/` is logged with method, path, status, and duration
- Upload failures trigger a retry path on the frontend before surfacing an error to the user
- AI service pipeline failures are logged per step (`face_detection`, `lip_segmentation`, `classifier`, `recommender`) so a failed analysis can be traced to the exact stage
- Monitoring must be able to answer: current API availability, average analysis time, and classification confidence distribution — these map directly to the Success Metrics in `PRD.md` Section 14

---

## Environment Variables

All environment variables are defined in `.env.local` (frontend) and `.env` (backend / ai-service). Never hardcode any key, URL, or secret anywhere in the codebase.

| Variable                          | Used In                                    |
| --------------------------------- | ------------------------------------------ |
| `NEXT_PUBLIC_API_URL`             | `frontend/lib/api-client.ts`               |
| `DATABASE_URL`                    | `backend/app/db/session.py`                |
| `JWT_SECRET_KEY`                  | `backend/app/core/security.py`             |
| `JWT_ALGORITHM`                   | `backend/app/core/security.py`             |
| `S3_ENDPOINT` / `S3_BUCKET`       | `backend/app/services/storage_service.py`  |
| `S3_ACCESS_KEY` / `S3_SECRET_KEY` | `backend/app/services/storage_service.py`  |
| `AI_SERVICE_URL`                  | `backend/app/services/analysis_service.py` |
| `CORS_ALLOWED_ORIGINS`            | `backend/app/main.py`                      |

`NEXT_PUBLIC_` prefix means the variable is exposed to the browser. Never add `NEXT_PUBLIC_` to any secret key, credential, or DB connection string.

---

## Constants

These values are defined once and imported everywhere — never hardcoded inline.

```python
# backend/app/core/config.py
MAX_UPLOAD_SIZE_MB = 10
SUPPORTED_IMAGE_TYPES = ["image/jpeg", "image/png"]
TOP_N_RECOMMENDATIONS = 3
```

```python
# ai-service/app/pipeline/classifier.py
MODEL_INPUT_SIZE = (224, 224)
LIP_TYPE_LABELS = ["Pinkish", "Brownish", "Dark"]
```

These correspond directly to the constraints in `PRD.md` Sections 8, 9, 16, and 18 (upload limits, model input size, supported labels, one-face-per-image, always-three-recommendations). Never change these values without updating `PRD.md` first.

---

## Import Aliases

**Frontend** — always use the `@/` alias, never a relative import that goes up more than one level:

```typescript
// Correct
import { Button } from "@/components/ui/button";
import { apiClient } from "@/lib/api-client";

// Never
import { Button } from "../../../components/ui/button";
```

**Backend / AI Service** — always import with the full package path from `app`, never a relative import crossing a service boundary:

```python
# Correct
from app.services import analysis_service
from app.core.security import get_current_user

# Never — ai-service must never import backend code, and vice versa
from backend.app.services import analysis_service
```

---

## Comments

- No comments explaining what the code does — code must be self-explanatory
- Comments only for why — explaining a non-obvious decision
- AI pipeline functions may include a brief comment explaining a non-obvious computer-vision or model choice (e.g. why a specific MediaPipe landmark index is used for lip cropping)
- Never leave TODO comments in committed code

---

## Dependencies

Never install a new package without a clear reason. Before installing anything check:

1. Does shadcn/ui already have this component?
2. Does Next.js or FastAPI already provide this functionality?
3. Is there a simpler native solution?

Approved dependencies for this project, per the stack defined in `architecture.md`:

**Frontend**

- `next` — framework (App Router)
- `tailwindcss` — styling
- `shadcn/ui` components — UI primitives
- `lucide-react` — icons
- `zod` — form/response validation

**Backend**

- `fastapi` — API framework
- `uvicorn` — ASGI server
- `sqlalchemy` — ORM
- `alembic` — DB migrations
- `pydantic` — schemas
- `python-jose` — JWT encode/decode
- `passlib[bcrypt]` — password hashing
- `httpx` — async HTTP client (calls to `ai-service`)
- `boto3` / S3-compatible client — object storage

**AI Service**

- `fastapi` / `uvicorn` — internal REST endpoint
- `mediapipe` — face and lip landmark detection
- `tensorflow` / `keras` — MobileNetV2 inference
- `numpy` — RGB feature extraction, Euclidean distance scoring
- `pillow` — image resize/crop/normalize

Do not install any other packages without updating this list first.

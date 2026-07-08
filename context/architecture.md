# Architecture

## Stack

| Layer                  | Tool                                | Purpose                                                      |
| ----------------------- | ------------------------------------ | -------------------------------------------------------------- |
| Frontend Framework      | Next.js 15 (App Router)             | Web application UI                                            |
| Backend API             | FastAPI (Python)                    | Business logic, auth, history, orchestrates AI service        |
| AI Inference Service    | FastAPI (Python, separate service)  | Face detection, lip segmentation, classification, recommendation |
| Face/Lip Detection      | MediaPipe Face Mesh                 | Face landmark + lip landmark detection                        |
| Lip Classification      | MobileNetV2 (TensorFlow/Keras)      | Classifies lip type: Pinkish / Brownish / Dark                |
| Recommendation Engine   | Custom Python (Rule-Based + Content-Based) | Hybrid recommendation using Euclidean Distance on RGB   |
| Database                | PostgreSQL                          | Users, analyses, lipstick knowledge base                      |
| ORM / Migrations        | SQLAlchemy + Alembic                | DB models and schema migrations                                |
| Object Storage          | S3-compatible Storage (MinIO / S3)  | Original images + cropped lip images                          |
| Authentication          | JWT + HttpOnly Cookie                | Session handling                                               |
| Password Hashing        | bcrypt                              | Password storage                                                |
| Styling                 | Tailwind CSS + shadcn/ui            | UI components and styling                                     |
| Language                | TypeScript (frontend) / Python (backend + AI) | Throughout                                            |

---

## Folder Structure

```
/
├── context/
│   ├── project-overview.md
│   ├── architecture.md
│   ├── PRD.md
│   ├── ui-tokens.md
│   ├── ui-rules.md
│   ├── code-standards.md
│   └── progress-tracker.md
├── frontend/                                  → Next.js Web Application
│   ├── app/
│   │   ├── layout.tsx                         → Root layout, providers
│   │   ├── page.tsx                           → Landing page
│   │   ├── (auth)/
│   │   │   ├── login/page.tsx                 → Login page
│   │   │   └── register/page.tsx              → Register page
│   │   ├── dashboard/
│   │   │   └── page.tsx                       → Dashboard (welcome, quick analyze, recent)
│   │   ├── analysis/
│   │   │   ├── page.tsx                       → Upload & analyze image
│   │   │   └── [id]/page.tsx                  → Analysis result detail
│   │   ├── history/
│   │   │   └── page.tsx                       → Analysis history list
│   │   ├── profile/
│   │   │   └── page.tsx                       → Profile (name, password, stats)
│   │   └── settings/
│   │       └── page.tsx                       → Account settings
│   ├── components/
│   │   ├── ui/                                → shadcn/ui components only
│   │   ├── layout/
│   │   │   ├── Navbar.tsx                     → Top nav (desktop)
│   │   │   ├── BottomNav.tsx                  → Bottom nav (mobile)
│   │   │   └── Footer.tsx
│   │   ├── landing/
│   │   │   ├── Hero.tsx
│   │   │   ├── Features.tsx
│   │   │   └── FAQ.tsx
│   │   ├── dashboard/
│   │   │   ├── QuickAnalyzeButton.tsx
│   │   │   ├── RecentAnalyses.tsx
│   │   │   └── StatsSummary.tsx
│   │   ├── analysis/
│   │   │   ├── UploadDropzone.tsx             → Upload + drag & drop + preview
│   │   │   ├── AnalysisProgress.tsx           → Pipeline loading state
│   │   │   ├── CroppedLipPreview.tsx
│   │   │   ├── LipAnalysisCard.tsx            → Lip type, confidence, RGB
│   │   │   └── RecommendationCard.tsx         → Shade, category, score, color preview
│   │   ├── history/
│   │   │   ├── HistoryList.tsx
│   │   │   └── HistoryItem.tsx
│   │   └── profile/
│   │       ├── ProfileForm.tsx
│   │       └── PasswordForm.tsx
│   ├── lib/
│   │   ├── api-client.ts                      → Fetch wrapper to FastAPI backend (credentials: include)
│   │   ├── auth.ts                            → Auth helpers (session check, redirect)
│   │   └── utils.ts                           → Shared utility functions
│   ├── types/
│   │   └── index.ts                           → Shared TypeScript types (Analysis, Lipstick, User)
│   └── middleware.ts                          → Route protection based on session cookie
│
├── backend/                                   → FastAPI Backend API
│   ├── app/
│   │   ├── main.py                            → App entrypoint, router registration, CORS
│   │   ├── core/
│   │   │   ├── config.py                      → Env vars, settings
│   │   │   └── security.py                    → JWT encode/decode, bcrypt hashing
│   │   ├── api/v1/
│   │   │   ├── auth.py                        → /register /login /logout
│   │   │   ├── analysis.py                    → /analysis (upload, trigger AI pipeline, save)
│   │   │   ├── history.py                     → /history (list, detail, delete)
│   │   │   └── profile.py                     → /profile (update, stats)
│   │   ├── models/                            → SQLAlchemy models
│   │   │   ├── user.py
│   │   │   ├── analysis.py
│   │   │   └── lipstick.py
│   │   ├── schemas/                           → Pydantic request/response schemas
│   │   ├── services/
│   │   │   ├── auth_service.py
│   │   │   ├── storage_service.py             → Object storage upload/fetch
│   │   │   ├── analysis_service.py            → Orchestrates AI service call + persistence
│   │   │   └── recommendation_service.py      → Calls AI service / applies ranking
│   │   ├── db/
│   │   │   ├── session.py
│   │   │   └── base.py
│   │   └── utils/
│   │       └── validators.py                  → File type/size validation
│   ├── alembic/                               → DB migrations
│   └── requirements.txt
│
├── ai-service/                                → AI Inference Service (internal, not public facing)
│   ├── app/
│   │   ├── main.py                            → Internal REST endpoint: /pipeline/analyze
│   │   ├── pipeline/
│   │   │   ├── face_detection.py              → MediaPipe face + face mesh
│   │   │   ├── lip_segmentation.py            → Landmark crop, mask, normalize
│   │   │   ├── rgb_extraction.py              → Average RGB from cropped lip
│   │   │   ├── classifier.py                  → MobileNetV2 inference (224x224)
│   │   │   └── recommender.py                 → Rule-Based + Content-Based hybrid ranking
│   │   ├── models/
│   │   │   └── mobilenetv2_lip.h5             → Trained classification weights
│   │   └── utils/
│   │       └── image_utils.py
│   └── requirements.txt
│
└── docs/                                      → Additional technical docs (DB, deployment, testing)
```

---

## System Boundaries

| Folder / Service | Owns                                                                                  |
| ----------------- | -------------------------------------------------------------------------------------- |
| `frontend/`       | UI, pages, client-side state. No business logic, no direct DB or storage access.       |
| `backend/api/`    | HTTP routes only. Delegates logic to `services/`.                                      |
| `backend/services/` | Business logic: auth, persistence, orchestration of AI service calls, storage I/O.  |
| `backend/models/` | Database schema definitions (SQLAlchemy) only.                                         |
| `ai-service/`     | Pure AI pipeline: face detection → segmentation → classification → recommendation. No auth, no DB, no user-facing concerns. Internal service only, called by `backend/`. |
| `lib/` (frontend) | Third-party client wrappers and shared utilities only.                                  |

---

## Data Flow

### UI Mutations (Auth & Profile)

```
User interaction in component
        ↓
API call via lib/api-client.ts
        ↓
FastAPI route in backend/app/api/v1/
        ↓
Service layer (auth_service.py / profile logic)
        ↓
PostgreSQL write via SQLAlchemy
        ↓
Response → UI updates / redirect
```

### Image Analysis (Core Pipeline)

```
User uploads face image (analysis/page.tsx)
        ↓
POST /analysis → backend/app/api/v1/analysis.py
        ↓
File validated (type, size ≤10MB) → uploaded to Object Storage (original image)
        ↓
backend calls ai-service: POST /pipeline/analyze
        ↓
MediaPipe Face Detection → face not found? → abort, return error
        ↓
Lip Landmark Detection → Lip Segmentation (crop, mask, normalize)
        ↓
Cropped lip image returned → uploaded to Object Storage
        ↓
RGB Feature Extraction (average R, G, B)
        ↓
MobileNetV2 Classification → { label, confidence }
        ↓
Recommendation Engine:
   Rule-Based Filtering (lip type → candidate shades)
        ↓
   Content-Based Filtering (Euclidean Distance on RGB → similarity score)
        ↓
   Ranking → Top-3 Recommendation
        ↓
backend saves analysis record (images, RGB, lip type, confidence, recommendations) → PostgreSQL
        ↓
Response returned to frontend → analysis/[id] result page
```

### History Retrieval

```
User opens /history
        ↓
GET /history → backend/app/api/v1/history.py
        ↓
Query scoped to current user_id only
        ↓
Returns list of past analyses (summary)
        ↓
User opens detail → GET /history/{id} → full analysis record returned
```

---

## PostgreSQL Database Schema

### `users`

| Column        | Type        | Notes                          |
| -------------- | ----------- | -------------------------------- |
| id             | uuid        | Primary key                    |
| name           | text        |                                 |
| email          | text        | Unique                         |
| password_hash  | text        | bcrypt hash                    |
| total_analyses | integer     | Denormalized count for profile |
| created_at     | timestamptz |                                 |
| updated_at     | timestamptz |                                 |

### `analyses`

| Column                 | Type        | Notes                                             |
| ----------------------- | ----------- | ---------------------------------------------------- |
| id                      | uuid        | Primary key                                       |
| user_id                 | uuid        | References users — always scoped in queries       |
| original_image_url      | text        | Object storage URL                                |
| cropped_lip_image_url   | text        | Object storage URL                                |
| rgb_r                   | integer     |                                                    |
| rgb_g                   | integer     |                                                    |
| rgb_b                   | integer     |                                                    |
| lip_type                | text        | Pinkish / Brownish / Dark                         |
| confidence              | float       | Model confidence score (0–1)                      |
| recommendations         | jsonb       | Array of Top-3 { shade_name, category, score }    |
| status                  | text        | completed / failed                                |
| created_at              | timestamptz |                                                    |

### `lipsticks` (Knowledge Base)

| Column      | Type    | Notes                                        |
| ----------- | ------- | --------------------------------------------- |
| id          | uuid    | Primary key                                  |
| shade_name  | text    | e.g. "Rose Pink"                             |
| category    | text    | e.g. Pink / Coral / Nude                     |
| rgb_r       | integer |                                               |
| rgb_g       | integer |                                               |
| rgb_b       | integer |                                               |
| lip_type_tag| text    | Pinkish / Brownish / Dark — used by rule-based step |
| metadata    | jsonb   | Optional: brand, hex code, finish            |

---

## Object Storage

| Bucket        | Path                                          | Contents                     |
| -------------- | ---------------------------------------------- | ------------------------------- |
| original-images | original-images/{user_id}/{analysis_id}.jpg | Uploaded face photo           |
| cropped-lips     | cropped-lips/{user_id}/{analysis_id}.jpg    | Segmented lip region           |

Access: authenticated users only, scoped to their own `user_id` prefix.

---

## Authentication

- Method: JWT Authentication, stored in HttpOnly Cookie
- Password hashing: bcrypt
- Protected routes (frontend): `/dashboard`, `/analysis`, `/analysis/[id]`, `/history`, `/profile`, `/settings`
- Public routes: `/`, `/login`, `/register`
- `middleware.ts` checks session cookie on every protected route
- Protected API routes (backend): all `/analysis`, `/history`, `/profile` endpoints require valid JWT — resolved via a FastAPI dependency (`get_current_user`)
- On successful login → redirect to `/dashboard`
- On logout → session cookie cleared, refresh token invalidated

---

## API Client Pattern (Frontend)

```typescript
// lib/api-client.ts
// All requests include credentials so the HttpOnly cookie is sent
export async function apiClient<T>(
  path: string,
  options: RequestInit = {}
): Promise<T> {
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}${path}`, {
    ...options,
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
      ...options.headers,
    },
  });

  if (!res.ok) {
    throw new Error(`API error: ${res.status}`);
  }

  return res.json();
}
```

---

## Auth Dependency Pattern (Backend)

```python
# app/core/security.py
from fastapi import Depends, HTTPException, Request
from jose import jwt, JWTError

async def get_current_user(request: Request) -> str:
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["sub"]  # user_id
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
```

Every route under `/analysis`, `/history`, and `/profile` depends on `get_current_user` and every query is scoped with `WHERE user_id = current_user_id`.

---

## AI Pipeline Call Pattern

```python
# backend/app/services/analysis_service.py
# backend orchestrates: upload → call ai-service → persist result

async def run_analysis(user_id: str, image_bytes: bytes):
    original_url = await storage_service.upload(
        bucket="original-images", path=f"{user_id}/{analysis_id}.jpg", data=image_bytes
    )

    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.post(
            f"{AI_SERVICE_URL}/pipeline/analyze",
            files={"image": image_bytes},
        )
        response.raise_for_status()
        result = response.json()
        # result: { cropped_lip, rgb, lip_type, confidence, recommendations }

    if result.get("face_detected") is False:
        raise AnalysisError("No face detected")

    cropped_url = await storage_service.upload(
        bucket="cropped-lips", path=f"{user_id}/{analysis_id}.jpg", data=result["cropped_lip"]
    )

    return await analysis_repo.create(
        user_id=user_id,
        original_image_url=original_url,
        cropped_lip_image_url=cropped_url,
        rgb=result["rgb"],
        lip_type=result["lip_type"],
        confidence=result["confidence"],
        recommendations=result["recommendations"],
    )
```

---

## Recommendation Engine Pattern (AI Service)

```python
# ai-service/app/pipeline/recommender.py
import numpy as np

def rule_based_candidates(lip_type: str, lipsticks: list) -> list:
    return [ls for ls in lipsticks if ls["lip_type_tag"] == lip_type]

def content_based_score(lip_rgb: tuple, lipstick_rgb: tuple) -> float:
    distance = np.linalg.norm(np.array(lip_rgb) - np.array(lipstick_rgb))
    return 1 / (1 + distance)  # normalize distance into similarity score

def get_top3(lip_type: str, lip_rgb: tuple, lipsticks: list) -> list:
    candidates = rule_based_candidates(lip_type, lipsticks)
    scored = [
        {**ls, "score": content_based_score(lip_rgb, (ls["rgb_r"], ls["rgb_g"], ls["rgb_b"]))}
        for ls in candidates
    ]
    ranked = sorted(scored, key=lambda x: x["score"], reverse=True)
    return ranked[:3]
```

---

## Invariants

Rules that must never be violated:

- Every image upload is validated for type (JPG/JPEG/PNG only) and size (≤10MB) before any processing.
- If face detection fails, the pipeline stops immediately — no partial analysis is ever saved.
- One uploaded image must contain exactly one face; multi-face images are rejected before segmentation.
- `ai-service/` never accesses PostgreSQL or Object Storage directly — it only receives an image and returns pipeline output. All persistence is owned by `backend/`.
- `backend/api/` routes contain no AI logic and no direct model inference — all of that lives in `ai-service/`.
- Every query on `analyses` and `profile` data is scoped with `WHERE user_id = current_user_id` — never queried without a user filter.
- A completed analysis always returns exactly three recommendations — never more, never fewer, never zero.
- All PostgreSQL writes from `backend/` go through the service layer — no raw queries from route handlers.
- Passwords are never stored or logged in plaintext — always bcrypt hashed before persistence.
- JWT tokens are only ever set/read via HttpOnly cookies — never exposed to client-side JavaScript or localStorage.
- Every Object Storage upload is scoped under the owning `user_id` path prefix.
- Every external call from `backend/` to `ai-service/` is wrapped in try/except; failures are logged and surfaced as a clean error response, never left to crash the request.
- The classification model only ever outputs one of the three supported labels: Pinkish, Brownish, Dark.
# Build Plan

> AI Lipstick Recommendation System — MVP
>
> Last Updated: July 2026

---

## Phase 1: Foundation

| # | Task | Complexity | Depends On |
|---|------|------------|------------|
| 1.1 | Scaffold `frontend/` — Next.js 15, Tailwind 3.4, shadcn/ui init, fonts (Fraunces, General Sans, IBM Plex Mono), CSS variables from ui-tokens.md | Medium | — |
| 1.2 | Scaffold `backend/` — FastAPI, SQLAlchemy, Alembic, CORS, Pydantic schemas, config from env | Medium | — |
| 1.3 | Scaffold `ai-service/` — FastAPI, MediaPipe, TensorFlow/Keras, Pillow, NumPy | Medium | — |
| 1.4 | Docker Compose — postgres, minio, redis (optional) | Simple | — |
| 1.5 | DB migrations — `users`, `analyses`, `lipsticks` tables per architecture.md schema | Medium | 1.2, 1.4 |
| 1.6 | Seed `lipsticks` knowledge base — shade names, categories, RGB values, lip_type_tag | Simple | 1.5 |
| 1.7 | Environment variables — `.env.local` (frontend), `.env` (backend, ai-service) per code-standards.md | Simple | 1.1, 1.2, 1.3 |

---

## Phase 2: Authentication

| # | Task | Complexity | Depends On |
|---|------|------------|------------|
| 2.1 | Backend: `POST /register`, `POST /login`, `POST /logout` routes | Medium | 1.2, 1.5 |
| 2.2 | Backend: JWT encode/decode, bcrypt hashing, `get_current_user` dependency | Medium | 2.1 |
| 2.3 | Backend: `storage_service.py` — S3/MinIO upload + presigned URL | Medium | 1.2, 1.4 |
| 2.4 | Frontend: `lib/api-client.ts` — fetch wrapper with `credentials: include` | Simple | 1.1 |
| 2.5 | Frontend: `middleware.ts` — session cookie check, route protection | Simple | 2.4 |
| 2.6 | Frontend: Register page (`/register`) with React Hook Form + Zod | Medium | 2.4 |
| 2.7 | Frontend: Login page (`/login`) with React Hook Form + Zod | Medium | 2.4 |

---

## Phase 3: Core UI Shell

| # | Task | Complexity | Depends On |
|---|------|------------|------------|
| 3.1 | Layout: `Navbar.tsx` (desktop top nav) + `BottomNav.tsx` (mobile) | Medium | 1.1 |
| 3.2 | Layout: `Footer.tsx` | Simple | 1.1 |
| 3.3 | Root layout — fonts, CSS vars, providers | Simple | 1.1 |
| 3.4 | Landing page — Hero, Features, FAQ, CTA sections | Medium | 3.1, 3.2, 3.3 |
| 3.5 | Dashboard page — welcome section, stats summary, recent analyses, quick analyze button | Medium | 2.5, 3.1 |

---

## Phase 4: Upload & Analysis UI

| # | Task | Complexity | Depends On |
|---|------|------------|------------|
| 4.1 | `UploadDropzone.tsx` — drag & drop, file validation (type, size ≤10MB), preview | High | 1.1 |
| 4.2 | `AnalysisProgress.tsx` — 4-step pipeline stepper with motion | High | 1.1 |
| 4.3 | Analysis page (`/analysis`) — upload → submit → progress → redirect to result | High | 4.1, 4.2, 2.5 |
| 4.4 | `LipAnalysisCard.tsx` — lip type badge, confidence score, RGB values | Medium | 1.1 |
| 4.5 | `RecommendationCard.tsx` — shade name, category, similarity score, color swatch chip | Medium | 1.1 |
| 4.6 | `CroppedLipPreview.tsx` — segmented lip image display | Simple | 1.1 |

---

## Phase 5: AI Pipeline (Backend + AI Service)

| # | Task | Complexity | Depends On |
|---|------|------------|------------|
| 5.1 | Backend: `POST /analysis` route — validate, upload original, call ai-service, save result | High | 2.2, 2.3 |
| 5.2 | AI Service: `face_detection.py` — MediaPipe Face Mesh, landmark detection | High | 1.3 |
| 5.3 | AI Service: `lip_segmentation.py` — crop, mask, normalize using landmarks | High | 5.2 |
| 5.4 | AI Service: `rgb_extraction.py` — average R, G, B from cropped lip | Simple | 5.3 |
| 5.5 | AI Service: `classifier.py` — MobileNetV2 inference (224×224), output label + confidence | High | 5.4 |
| 5.6 | AI Service: `recommender.py` — rule-based filtering + content-based (Euclidean distance) → top-3 | High | 5.5 |
| 5.7 | AI Service: `POST /pipeline/analyze` orchestrator — full pipeline, error handling, structured response | High | 5.2–5.6 |
| 5.8 | AI Service: Model loading at startup (not per request) | Simple | 1.3, 5.5 |

---

## Phase 6: Results & History

| # | Task | Complexity | Depends On |
|---|------|------------|------------|
| 6.1 | Analysis result page (`/analysis/[id]`) — full result display | High | 4.4, 4.5, 4.6, 5.1 |
| 6.2 | Backend: `GET /history`, `GET /history/{id}`, `DELETE /history/{id}` | Medium | 2.2, 1.5 |
| 6.3 | History page (`/history`) — list of cards, delete action | Medium | 6.2, 3.1 |
| 6.4 | `HistoryList.tsx` + `HistoryItem.tsx` — card-based list with hover state | Medium | 1.1 |
| 6.5 | Backend: `PATCH /profile`, `PATCH /profile/password`, `GET /profile/stats` | Medium | 2.2, 1.5 |
| 6.6 | Profile page (`/profile`) — `ProfileForm.tsx`, `PasswordForm.tsx`, stats | Medium | 6.5, 3.1 |

---

## Phase 7: Polish & Verification

| # | Task | Complexity | Depends On |
|---|------|------------|------------|
| 7.1 | Loading states — skeleton loaders for all data-fetching pages | Medium | All phases |
| 7.2 | Empty states — History, Recent Analyses (per ui-rules.md) | Simple | 6.3, 3.5 |
| 7.3 | Error handling — user-facing messages (never raw exceptions) | Medium | All phases |
| 7.4 | Responsive testing — desktop, tablet, mobile breakpoints | Medium | All phases |
| 7.5 | Update `ui-registry.md` — every built component with exact classes | Simple | All phases |
| 7.6 | Update `progress-tracker.md` — feature completion status | Simple | All phases |

---

## Dependency Graph

```
Phase 1 (Foundation)
  ├── Phase 2 (Auth)
  │     ├── Phase 3 (UI Shell) ──────┐
  │     │                            ├── Phase 4 (Upload & Analysis UI)
  │     │                            │
  │     └── Phase 5 (AI Pipeline) ───┤
  │                                  │
  │                                  ├── Phase 6 (Results & History)
  │                                  │
  │                                  └── Phase 7 (Polish)
```

---

## Key Constraints

- No AI inference in frontend — all AI runs in `ai-service/`
- `ai-service/` never touches DB or storage directly
- Every analysis returns exactly 3 recommendations
- Tailwind CSS 3.4 only — no v4
- No hardcoded hex values — use CSS variables from ui-tokens.md
- JWT in HttpOnly cookies only — never localStorage
- Max upload: 10MB, formats: JPG/JPEG/PNG only

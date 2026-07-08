---
description: Instructions building apps with MCP
globs: *
alwaysApply: true
---

<!-- BEGIN:nextjs-agent-rules -->

# This is NOT the Next.js you know

This version has breaking changes — APIs, conventions, and file structure may all differ from your training data. Read the relevant guide in `node_modules/next/dist/docs/` before writing any code. Heed deprecation notices.

<!-- END:nextjs-agent-rules -->

## Read Before Anything Else

Read in this exact order before any implementation:

1. PRD.md
2. context/project-overview.md
3. context/architecture.md
4. context/ui-tokens.md
5. context/ui-rules.md
6. context/ui-registry.md
7. context/code-standards.md
8. context/library-docs.md
9. context/build-plan.md
10. context/progress-tracker.md

## Rules That Never Change

- Never use hardcoded hex values or raw Tailwind color classes
- Update `progress-tracker.md` and `ui-registry.md` after every feature
- Before any third party library — load its installed skill first,
  then read `context/library-docs.md` for project-specific rules
- If the same problem persists after one corrective prompt —
  stop immediately and run /recover

## Available Skills

- `/architect` — before any complex feature. Think before building.
- `/frontend-design` — before building any frontend/UI component. Create distinctive, production-grade web UI.
- `/imprint` — after any new UI component. Capture patterns.
- `/review` — before demo or when something feels off.
- `/recover` — when something breaks after one failed correction.
- `/remember save` — when a feature spans multiple sessions.
- `/remember restore` — when returning after a multi-session feature.

---

## Project Stack

This project is a **custom full-stack application** — not a BaaS template.

| Layer | Stack |
|-------|-------|
| Frontend | Next.js 15 (App Router), TypeScript, Tailwind CSS 3.4, shadcn/ui |
| Backend API | FastAPI (Python), SQLAlchemy + Alembic, Pydantic |
| AI Inference | FastAPI (Python, separate service), MediaPipe, TensorFlow/Keras, NumPy, Pillow |
| Database | PostgreSQL |
| Object Storage | S3-compatible (MinIO) |
| Auth | JWT + HttpOnly Cookie, bcrypt |

### System Boundaries

- `frontend/` — UI only. No business logic, no direct DB/storage access.
- `backend/` — API routes + services. Owns auth, persistence, orchestration.
- `ai-service/` — Pure AI pipeline. No auth, no DB, internal only.

### Key Rules

- Tailwind CSS 3.4 only — never upgrade to v4
- Never use hardcoded hex values — use CSS variables from `context/ui-tokens.md`
- AI inference never runs in frontend
- `ai-service/` never touches DB or storage directly
- Every analysis returns exactly 3 recommendations
- JWT in HttpOnly cookies only — never localStorage
- Max upload: 10MB, formats: JPG/JPEG/PNG only
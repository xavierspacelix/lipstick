# Library Docs

Project-specific usage patterns for every third-party library used in the AI Lipstick Recommendation System.

This document defines **how each library must be used inside this project**.

Always prefer project conventions over generic documentation.

---

# Before Using Any Library

Before implementing any feature that depends on a third-party library:

1. Read `AGENTS.md`
2. Check whether an MCP Server exists for that library
3. Read this document for project-specific rules

Priority order:

```
MCP Server
↓

AGENTS.md

↓

library-docs.md

↓

Official Documentation

↓

General LLM Knowledge
```

Never rely solely on model knowledge for rapidly evolving libraries.

---

# Next.js

## Usage

Next.js is responsible only for:

- UI Rendering
- Routing
- Authentication UI
- Upload Interface
- Dashboard
- History
- Profile

Never execute AI inference inside Next.js.

---

## Routing

Use App Router only.

```
app/

login/

register/

dashboard/

analysis/

history/

profile/

settings/
```

Do not use Pages Router.

---

## Components

Prefer Server Components.

Only use Client Components when:

- State exists
- Browser API required
- Upload interaction
- Drag & Drop
- Forms

---

## Data Fetching

Always use TanStack Query.

Never fetch data directly inside components using `fetch()`.

---

# React Hook Form

Used for:

- Login
- Register
- Profile
- Upload Form

Always combine with Zod.

Example

```tsx
const form = useForm<FormSchema>({
  resolver: zodResolver(schema),
});
```

Never manually validate forms.

---

# Zod

All validation must be centralized.

Used for:

- API validation
- Form validation
- Environment variables

Never duplicate validation logic.

---

# Tailwind CSS

Only use utility classes.

Never create large custom CSS files.

Preferred

```
flex
grid
gap
rounded
shadow
```

Avoid

```
!important
inline style
```

---

# shadcn/ui

Default UI library.

Allowed

- Button
- Card
- Table
- Dialog
- Badge
- Tabs
- Form
- Dropdown
- Tooltip

Never modify library source directly.

Create wrappers if customization is needed.

---

# FastAPI

Responsible for:

- REST API
- Authentication
- AI orchestration
- Database
- Storage

Never place AI implementation inside route handlers.

Routes should remain thin.

Example

```
Router

↓

Service

↓

Repository

↓

Database
```

---

# SQLAlchemy

Database access only.

Repositories own SQLAlchemy.

Never query the database directly inside services.

Correct

```
Service

↓

Repository

↓

SQLAlchemy
```

Wrong

```
Service

↓

Session.query(...)
```

---

# PostgreSQL

Stores

- Users
- Analysis
- Recommendation
- Lipstick Dataset
- History

Never store uploaded images as BYTEA.

Images belong in MinIO.

Only store URLs.

---

# MinIO

Used for object storage.

Buckets

```
uploads

cropped

results
```

Object Path

```
uploads/{user_id}/{analysis_id}.jpg

cropped/{analysis_id}.png

results/{analysis_id}.json
```

Rules

- Never store temporary files locally.
- Always upload directly.
- Save object key in database.

---

# TensorFlow

Used only inside AI Service.

Responsible for

- Load MobileNetV2
- Prediction

Model loaded once during application startup.

Never reload model per request.

Correct

```
Application Startup

↓

Load Model

↓

Reuse Model
```

Wrong

```
Prediction

↓

Load Model

↓

Predict
```

---

# Keras

Used for

- Model loading
- Image preprocessing

Never retrain model inside API.

Training exists only in `/ai/training`.

---

# OpenCV

Used for

- Resize
- Crop
- Mask
- Color conversion
- Normalization

Never perform business logic.

Only image processing.

---

# MediaPipe

Responsible for

- Face Detection
- Face Mesh
- Lip Landmark Detection

Pipeline

```
Image

↓

Face Mesh

↓

Landmarks

↓

Lip Extraction
```

If no face detected

Return

```
422

Face Not Found
```

---

# NumPy

Used only for

- RGB calculation
- Euclidean Distance
- Matrix manipulation

Never use loops where vectorized operations exist.

---

# Recommendation Engine

Project implementation.

Pipeline

```
Prediction

↓

Rule-Based Filtering

↓

Candidate Shades

↓

Content-Based Filtering

↓

Similarity Score

↓

Ranking

↓

Top 3
```

Similarity

```
Euclidean Distance
```

Never recommend more than 3 shades.

---

# Pillow

Used only when image format conversion is required.

Supported

- JPG
- JPEG
- PNG

Reject

- GIF
- BMP
- TIFF
- HEIC

---

# JWT

Authentication

Access Token

```
15 minutes
```

Refresh Token

```
7 days
```

Stored using HttpOnly Cookie.

Never store JWT in LocalStorage.

---

# Redis

Optional.

Uses

- Cache
- Rate Limiting
- Background Queue

Never store permanent data.

---

# Docker

Each service has its own container.

```
frontend

backend

ai-service

postgres

minio

redis

nginx
```

Never combine multiple applications inside one container.

---

# Nginx

Acts as Reverse Proxy.

Routes

```
/

↓

Frontend

/api

↓

Backend

/storage

↓

MinIO
```

Never expose AI service directly.

---

# Python Logging

Always use structured logging.

Include

- request_id
- user_id
- analysis_id
- execution_time

Never use print().

---

# Pydantic

All API DTOs use Pydantic.

Example

```python
class UploadResponse(BaseModel):
    analysis_id: UUID
    recommendation: list[str]
```

Never return ORM models directly.

---

# Testing

## Frontend

- Vitest
- React Testing Library

## Backend

- Pytest

## AI

- Dedicated evaluation dataset

Coverage target

```
80%
```

---

# Environment Variables

Never access environment variables directly.

Use centralized configuration.

Example

```python
settings.MINIO_ENDPOINT
```

instead of

```python
os.getenv(...)
```

---

# File Upload Rules

Supported

```
jpg

jpeg

png
```

Maximum Size

```
10 MB
```

Minimum Resolution

```
224 × 224
```

Maximum Resolution

```
4096 × 4096
```

Always validate

- MIME Type
- Extension
- File Size

before upload.

---

# AI Inference Rules

Pipeline

```
Receive Image

↓

Validate

↓

Store Original

↓

MediaPipe

↓

Crop Lip

↓

Normalize

↓

Extract RGB

↓

Predict

↓

Recommend

↓

Store Result

↓

Return Response
```

Prediction timeout

```
5 seconds
```

If timeout exceeded

Return

```
504 Gateway Timeout
```

---

# Error Handling

Always return structured responses.

Example

```json
{
  "success": false,
  "message": "Face not detected.",
  "code": "FACE_NOT_FOUND"
}
```

Never expose Python stack traces.

---

# General Rules

- Never duplicate business logic.
- Keep AI logic isolated from API.
- Keep repositories database-only.
- Keep services business-only.
- Keep routes thin.
- Always validate input.
- Always handle exceptions.
- Never trust uploaded files.
- Never expose internal infrastructure.
- Never reload AI models per request.
- Always keep the AI pipeline deterministic.

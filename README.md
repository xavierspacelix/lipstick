# AI Lipstick Recommendation System

Upload selfies → AI detects your face → segments lips → extracts colour → classifies lip type → recommends 3 perfect shades. Up to 3 photos per analysis for better accuracy.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 16 (App Router), TypeScript, Tailwind CSS 3.4, shadcn/ui, Motion, Lenis |
| Backend API | FastAPI (Python), SQLAlchemy + Alembic, Pydantic |
| AI Inference | FastAPI (Python, separate service), MediaPipe, TensorFlow/Keras, NumPy, Pillow |
| Database | PostgreSQL |
| Object Storage | S3-compatible (MinIO) |
| Auth | JWT + HttpOnly Cookie, bcrypt |

## Project Structure

```
lipstick/
├── frontend/            Next.js web app (port 3000)
├── backend/             FastAPI REST API (port 8000)
├── ai-service/          FastAPI AI pipeline (port 8001, internal only)
├── context/             Design tokens, architecture, progress tracking
├── AGENTS.md            AI agent instructions
├── PRD.md               Product requirements
└── README.md
```

---

## Quick Start — Local Development

### Prerequisites

- Python 3.11
- Node.js 18+
- PostgreSQL (cloud or local)
- S3-compatible storage (MinIO or cloud)

### 1. Environment Variables

```bash
# Backend
cp backend/.env.example backend/.env
# Edit backend/.env with your database, S3, and JWT values

# Frontend
cp frontend/.env.local.example frontend/.env.local
```

**Key variables:**

| Variable | Service | Example |
|----------|---------|---------|
| `DATABASE_URL` | Backend | `postgresql://user:pass@host:5432/lipstick` |
| `JWT_SECRET_KEY` | Backend | (random string) |
| `S3_ENDPOINT` | Backend | `http://localhost:9000` |
| `S3_ACCESS_KEY` | Backend | MinIO access key |
| `S3_SECRET_KEY` | Backend | MinIO secret key |
| `AI_SERVICE_URL` | Backend | `http://localhost:8001` |
| `CORS_ALLOWED_ORIGINS` | Backend | `http://localhost:3000` |
| `NEXT_PUBLIC_API_URL` | Frontend | `http://localhost:8000` |

> PostgreSQL and MinIO are expected as external services. No local Docker setup provided — configure your cloud URLs in `backend/.env`. S3 buckets (`original-images`, `cropped-lips`, `brushed-lips`) are auto-created on backend startup.

### 2. Backend

```bash
cd backend
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
python seed.py                       # seeds 288 lipstick shades
uvicorn app.main:app --reload --port 8000
```

### 3. AI Service

```bash
cd ai-service
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001
```

> MediaPipe runs on CPU. The TensorFlow model (`mobilenetv2_lip.h5`) is optional — a rule-based fallback is used when absent.

### 4. Frontend

```bash
cd frontend
npm install
npm run dev              # → http://localhost:3000
```

### 5. Open three terminals

```bash
# Terminal 1 — Frontend
cd frontend && npm run dev

# Terminal 2 — Backend
cd backend && source .venv/bin/activate && uvicorn app.main:app --reload --port 8000

# Terminal 3 — AI Service
cd ai-service && source .venv/bin/activate && uvicorn app.main:app --reload --port 8001
```

---

## Docker (Production)

```bash
docker compose up --build -d
```

This starts all three services:

| Service | Port | URL |
|---------|------|-----|
| Frontend | 3000 | http://localhost:3000 |
| Backend | 8000 | http://localhost:8000 |
| AI Service | 8001 | (internal only) |

Each service has its own `Dockerfile` and `.dockerignore`. The compose file uses a bridge network (`lipstick`) so services communicate by service name.

---

## API Endpoints

### Auth (`/api/v1/`)
| Method | Path | Description |
|--------|------|-------------|
| POST | `/register` | Create account (name, email, password) |
| POST | `/login` | Sign in (sets HttpOnly JWT cookie) |
| POST | `/logout` | Sign out (clears cookie) |

### Profile (`/api/v1/`)
| Method | Path | Description |
|--------|------|-------------|
| GET | `/profile` | Get current user |
| PATCH | `/profile` | Update name |
| PATCH | `/profile/password` | Change password |
| GET | `/profile/stats` | Total analyses count |

### Analysis (`/api/v1/`)
| Method | Path | Description |
|--------|------|-------------|
| POST | `/analysis` | Upload 1–3 images (`images` field, multipart/form-data) |
| GET | `/analysis/{id}` | Get result with recommendations |

> Multi-image: RGB values are averaged across all photos, lip type is majority-voted, confidence is averaged. Only the first image's cropped lip and try-on are stored.

### History (`/api/v1/`)
| Method | Path | Description |
|--------|------|-------------|
| GET | `/history` | List all past analyses |
| GET | `/history/{id}` | Get analysis detail |
| DELETE | `/history/{id}` | Delete analysis |

### Lipsticks (`/api/v1/`)
| Method | Path | Description |
|--------|------|-------------|
| GET | `/lipsticks` | List all shades (optional `?lip_type=` & `?category=` filters) |

### AI Pipeline (`/pipeline/` on port 8001 — internal only)
| Method | Path | Description |
|--------|------|-------------|
| POST | `/pipeline/analyze` | Face detection → lip segmentation → RGB → classification → recommendation |

---

## Pages

| Route | Description |
|-------|-------------|
| `/` | Landing page (hero, features, shade showcase, FAQ) |
| `/login` | Sign in |
| `/register` | Create account |
| `/dashboard` | Overview with stats and recent analyses |
| `/analysis` | Upload/capture up to 3 selfies for AI analysis |
| `/analysis/[id]` | View analysis results + 3 shade recommendations |
| `/shades` | Browse all 288 lipstick shades with colour swatches |
| `/history` | Browse past analyses |
| `/profile` | Manage account, change password |
| `/settings` | Appearance/language/notification placeholders |

---

## Lipstick Database

The system ships with **288 lipstick shades** (18 curated + 270 sourced from [theBigDataDigest/lipsticks_detect](https://github.com/theBigDataDigest/lipsticks_detect)) across 3 lip type categories:

| Lip Type | Description | Sample Shades |
|----------|-------------|---------------|
| Pinkish | Light, bright lips | Rose Pink, Coral Glow, Bold Raspberry |
| Brownish | Medium, warm lips | Cinnamon, Terracotta, Mauve Bliss |
| Dark | Deep, dark lips | Burgundy, Plum Wine, Deep Berry |

Database available in two places:
- `backend/app/services/recommendation_service.py` — used by backend for multi-photo recommendation
- `ai-service/app/pipeline/recommender.py` — used by AI service for single-photo recommendation

Run `python seed.py` in `backend/` to populate the database table.

---

## Design System

**Glass Beauty** aesthetic — glassmorphism cards with backdrop blur, warm porcelain background (`#FBF3EF`), deep berry primary (`#8C2F45`), and editorial typography (Fraunces + Inter + IBM Plex Mono).

Design tokens and component patterns:
- `context/ui-tokens.md` — colours, typography, spacing, shadows
- `context/ui-registry.md` — every component with its exact classes

---

## Training the Classifier

Without a trained `.h5` model, the AI service falls back to average-RGB thresholds. For higher accuracy:

```bash
cd ai-service/training
pip install -r requirements.txt
```

**Option A — Labeled dataset** (folder name = label):
```
my_dataset/
  pinkish/   img1.jpg  img2.jpg  ...
  brownish/  img1.jpg  img2.jpg  ...
  dark/      img1.jpg  img2.jpg  ...
```

```bash
python prepare_custom.py --input /path/to/my_dataset --labeled
```

**Option B — Face photos (auto-label)**:
```bash
python prepare_custom.py --input /path/to/face_photos
```

**Option C — CelebA dataset**:
```bash
# Requires Kaggle API token
python download_celeba.py --output ./data/celeba
python prepare_dataset.py --input ./data/celeba/img_align_celeba --output ./data/processed --limit 50000
```

**Train:**
```bash
python train.py --data ./data/processed/metadata.pkl --output ../app/models/mobilenetv2_lip.h5 --epochs 20 --fine-tune
```

---

## License

Private — internal project.

# Memory — Docker Hybrid Deploy, Score Fix, TensorFlow Only

Last updated: July 9, 2026

## What was built

**Score percentage fix:**
- Changed scoring formula to relative normalization (best match = 100%)
- Updated `backend/app/services/recommendation_service.py`, `ai-service/app/pipeline/recommender.py`, `frontend/src/components/analysis/RecommendationCard.tsx`

**Docker hybrid deploy:**
- ai-service runs manually on host (screen/nohup), backend/frontend in Docker
- `docker-compose.yml` has extra_hosts for host.docker.internal
- `AI_SERVICE_URL=http://host.docker.internal:8001` in backend .env.example

**Pure TensorFlow mode:**
- Removed all TFLite code paths from `classifier.py`
- model loading uses `safe_mode=False, compile=False` for Keras 3 compatibility
- `requirements.txt` includes `tensorflow==2.17.0` directly
- Deleted `requirements-tflite.txt` and `requirements-tensorflow.txt`

## Decisions made

- **Score is now relative (%)** — best match always 100%, others scaled by distance ratio
- **TensorFlow only** — no dual mode, no TFLite fallback
- **Hybrid deploy** — ai-service on host (saves ~2GB CUDA packages in Docker)

## Problems solved

- **Cross-subdomain auth** — `COOKIE_DOMAIN=.spacelix.qzz.io`
- **S3 mixed-content** — proxy endpoint `/api/v1/images/{bucket}/{key}`
- **Score ranking** — relative normalization (best=100%)
- **total_analyses** — counted via query and backfilled
- **TFLite → TF regression** — Keras 3 loading fixed with `safe_mode=False`

## Current state

- **Backend/Frontend:** Docker (via docker compose up -d)
- **AI Service:** manual via `screen -S ai-service uvicorn app.main:app --host 0.0.0.0 --port 8001`
- **Classifier:** TensorFlow only, rule-based fallback if model fails

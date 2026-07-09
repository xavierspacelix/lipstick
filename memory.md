# Memory — Docker Build Fix, Score Percentage, TFLite Migration Start

Last updated: July 9, 2026

## What was built

**Score percentage fix:**
- Changed scoring formula from `1/(1+distance)` (raw RGB 0-255 Euclidean → ~3%) to `(1 - distance/441.67) * 100` (intuitive 0-100%)
- Updated `backend/app/services/recommendation_service.py` — `_similarity_pct()` function
- Updated `ai-service/app/pipeline/recommender.py` — remove `np.linalg.norm`, use pure `math.sqrt` + same formula
- Fixed `frontend/src/components/analysis/RecommendationCard.tsx` — removed double `* 100` multiplication

**Docker build fix (ai-service OOM):**
- `ai-service/Dockerfile` — split pip install into two stages: mediapipe/fastapi/etc first, then tensorflow with `--no-deps` + only CPU runtime deps (avoids ~2GB nvidia-* CUDA packages)

**TFLite migration (started):**
- Plan: convert `mobilenetv2_lip.h5` → `.tflite`, replace tensorflow with `tflite-runtime`, update `classifier.py`
- Conversion not yet completed (pip install tensorflow was aborted)

## Decisions made

- **Score is now 0-100%** — users see intuitive percentages (80-95% for good matches instead of 2-5%)
- **TFLite is the right approach** — eliminates CUDA dependency entirely, image drops from ~2GB to ~200MB

## Problems solved

- **Score showed 3%** — Euclidean distance on 0-255 RGB scale makes `1/(1+distance)` produce ~0.03 for close colors; fixed by normalizing against max possible distance (441.67)
- **Docker build OOM (No space left on device)** — `tensorflow==2.17.0` on Linux pulls all `nvidia-*` CUDA packages; fixed by installing with `--no-deps` + explicit CPU-only deps

## Current state

- **Backend:** score now 0-100% intuitive percentage
- **Frontend:** score bar and label display correct percentage
- **AI Service:** still depends on tensorflow (TFLite not yet live)
- **Docker:** ai-service Dockerfile patched but TFLite will simplify further

## Next session starts with

1. **Convert model to TFLite:**
   ```bash
   python3 -m pip install tensorflow==2.17.0
   python3 -c "
   import tensorflow as tf
   model = tf.keras.models.load_model('ai-service/app/models/mobilenetv2_lip.h5')
   converter = tf.lite.TFLiteConverter.from_keras_model(model)
   tflite_model = converter.convert()
   with open('ai-service/app/models/mobilenetv2_lip.tflite', 'wb') as f:
       f.write(tflite_model)
   "
   pip uninstall tensorflow
   ```
2. Update `classifier.py` to use `tflite.Interpreter` instead of `keras.load_model`
3. Update `requirements.txt`: `tensorflow` → `tflite-runtime`
4. Simplify `Dockerfile`: remove the --no-deps hack, just install `tflite-runtime`

## Open questions

- None — TFLite conversion is mechanical once tensorflow is installed temporarily

# Memory — Retrain Model + Rule-based Classifier + AI Service Screen

Last updated: July 10, 2026

## What was built

**Score normalization fix:**
- Min-max normalization so best=100%, worst=0% (was capped at 50%)
- Changed to soft normalization with floor=20% so worst item != 0%
- Updated `ai-service/app/pipeline/recommender.py` and `backend/app/services/recommendation_service.py`

**Delete analysis also deletes Minio images:**
- Added Minio cleanup to `backend/app/api/v1/history.py` — hapus original, cropped, brushed images

**AI service via screen (non-Docker):**
- `screen -dmS ai-service` pattern untuk manage ai-service tanpa Docker
- Setup guide untuk VPS: Python venv + uvicorn + screen

**TF SavedModel rebuild fix:**
- Weight loading di `scripts/rebuild_model.py` rusak — semua 264 weight gagal load karena nama variable mismatch (`:0` suffix, `depthwise_kernel` vs `kernel`)
- Fixed: `var.name.rstrip(":0")`, aliasing `sequential/` prefix, mapping `depthwise_kernel` → `kernel`
- Model tetap predict Pinkish 100% karena training data bias (2973 Pinkish : 13 Dark : 0 Brownish)

**Hybrid classifier:**
- `ai-service/app/pipeline/classifier.py` — TF jika confidence >85%, fallback rule-based
- Rule-based pakai RGB thresholds: Dark (brightness<0.3), Pinkish (r>0.45, g>0.3, b>0.25), sisanya Brownish
- TF direstore di requirements.txt

**Training pipeline overhaul:**
- `data_generator()` — load gambar per batch (anti OOM, sebelumnya 5349 gambar penuh ke RAM)
- `--balance` — limit samples per class (atur di load_samples, bukan load full ke memory)
- Oversampling minoritas di generator (ganti `class_weight` yang gak support generator di Keras 3)
- `model.export()` instead of `model.save()` untuk SavedModel (Keras 3)
- Plot history (accuracy/loss) + confusion matrix otomatis ke `training_plots/`
- LAB threshold fix di `prepare_dataset.py` — Brownish dapet a>5 OR l>40 (sebelumnya a<=12 terlalu strict)

**Training result:**
- Dataset: 5349 samples (Pinkish=5000, Brownish=299, Dark=50) dari CelebA female-only
- MobileNetV2, Adam LR=0.001, 50 epochs + fine-tune, batch=32
- Validation accuracy: 96.5%, loss: 0.1111
- SavedModel di `app/models/mobilenetv2_lip_best/`

## Decisions made

- **TF model optional** — classifier hybrid: TF jika confident >85%, fallback rule-based (gak perlu TF di runtime)
- **Model training di dev machine (DESKTOP-U918DRN)** — bukan di VPS (VPS mungkin OOM)
- **SavedModel di symlink** — `mobilenetv2_lip -> mobilenetv2_lip_best` biar classifier path tetap `mobilenetv2_lip/`
- **Training dependencies** di `training/requirements.txt` terpisah dari runtime `requirements.txt`

## Problems solved

- **Model selalu predict Pinkish** — root cause: dataset imbalance (2973 : 13 : 0) + weight loading broken
- **Weight loading matching** — `:0` suffix, `sequential/` prefix, `depthwise_kernel` vs `kernel`
- **class_weight with generator** — di Keras 3 gak support, ganti oversampling di generator
- **model.save() SavedModel** — di Keras 3 pake `model.export()` bukan `model.save()`
- **OOM training** — 5349 gambar 224x224 penuh di RAM kill process, solved with data generator

## Current state

- **Dev machine**: model trained, committed (`app/models/mobilenetv2_lip_best.h5` + SavedModel)
- **VPS**: perlu `git pull` + symlink `mobilenetv2_lip -> mobilenetv2_lip_best` + restart ai-service
- **Classifier**: TF loaded kalo ada SavedModel, fallback rule-based
- **Score**: soft normalization, best=100, worst=20

## Next session starts with

Deploy model ke VPS + verify hasil recommendation (cek apakah TF model aktif dengan confidence > cukup).

## Open questions

- Apakah akurasi 96.5% real atau overfit (Dark cuma 50 samples)?
- Brownish cuma 299 samples — perlu lebih banyak data biar seimbang
- Perlu fine-tuning lebih lanjut? Atau tambah data augmentation?

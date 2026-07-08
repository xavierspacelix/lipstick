# Product Requirements Document (PRD)

> Version: 1.0.0
>
> Status: Draft
>
> Product: AI Lipstick Recommendation System
>
> Platform: Web Application
>
> Last Updated: July 2026

---

# 1. Product Overview

## Background

Banyak pengguna mengalami kesulitan dalam memilih warna lipstik yang sesuai dengan warna alami bibir. Sebagian besar pembelian lipstik masih dilakukan berdasarkan tren, rekomendasi orang lain, maupun trial-and-error sehingga sering menghasilkan warna yang kurang sesuai.

Aplikasi ini bertujuan membantu pengguna menemukan warna lipstik yang paling sesuai menggunakan Artificial Intelligence (AI). Pengguna cukup mengunggah foto wajah melalui browser, kemudian sistem akan menganalisis warna alami bibir dan memberikan tiga rekomendasi warna lipstik terbaik.

Sistem menggunakan kombinasi Computer Vision, Deep Learning, dan Hybrid Recommendation System untuk menghasilkan rekomendasi yang lebih akurat.

---

# 2. Goals

## Business Goals

- Membantu pengguna memilih warna lipstik dengan lebih percaya diri.
- Mengurangi trial-and-error saat membeli lipstik.
- Memberikan pengalaman konsultasi makeup berbasis AI.
- Menjadi fondasi pengembangan Beauty Recommendation Platform.

## Product Goals

- Mengidentifikasi tipe bibir pengguna secara otomatis.
- Memberikan rekomendasi Top-3 warna lipstik.
- Menyimpan riwayat analisis.
- Memberikan hasil analisis dalam waktu kurang dari 5 detik.

---

# 3. Target Users

## Primary Users

Wanita usia 17–40 tahun yang:

- Menggunakan produk kosmetik.
- Membeli lipstik secara online maupun offline.
- Ingin mengetahui warna lipstik yang cocok.

## Secondary Users

- Makeup Artist
- Beauty Consultant
- Beauty Content Creator

---

# 4. Problem Statement

Pengguna sering mengalami masalah berikut:

- Sulit menentukan warna lipstik yang cocok.
- Tidak mengetahui karakteristik warna bibir alami.
- Tidak memiliki referensi shade yang sesuai.
- Membeli lipstik yang akhirnya jarang digunakan.

Aplikasi ini bertujuan menyelesaikan masalah tersebut melalui analisis otomatis.

---

# 5. Solution

Aplikasi menerima foto wajah pengguna.

Selanjutnya sistem melakukan:

1. Face Detection
2. Lip Detection
3. Lip Segmentation
4. RGB Feature Extraction
5. Lip Classification menggunakan MobileNetV2
6. Hybrid Recommendation
7. Menampilkan Top-3 warna lipstik

---

# 6. MVP Scope

## Included

- User Registration
- User Login
- User Logout
- Upload foto wajah
- Face Detection
- Lip Detection
- Lip Segmentation
- RGB Feature Extraction
- MobileNetV2 Classification
- Hybrid Recommendation
- Top-3 Recommendation
- Analysis History
- User Profile

## Excluded

- Virtual Try-On
- Skin Tone Analysis
- Foundation Recommendation
- Blush Recommendation
- Marketplace Integration
- AI Beauty Assistant
- Social Features

---

# 7. Functional Requirements

## Authentication

### Register

User dapat membuat akun menggunakan:

- Nama
- Email
- Password

Acceptance Criteria

- Email harus unik.
- Password minimal 8 karakter.
- Password harus di-hash.

---

### Login

User dapat login menggunakan:

- Email
- Password

Acceptance Criteria

- Menggunakan JWT Authentication.
- Session tersimpan menggunakan HttpOnly Cookie.

---

### Logout

User dapat mengakhiri sesi login.

Acceptance Criteria

- Session dihapus.
- Refresh Token dinonaktifkan.

---

# 8. Analysis Module

## Upload Image

User dapat:

- Upload dari komputer
- Drag & Drop gambar

Supported Format

- JPG
- JPEG
- PNG

Maximum Size

10 MB

Acceptance Criteria

- Hanya menerima gambar.
- Menampilkan preview.
- Validasi ukuran file.

---

## Face Detection

Sistem mendeteksi wajah menggunakan MediaPipe.

Output

- Face Landmark
- Lip Landmark

Jika wajah tidak ditemukan maka proses dihentikan.

---

## Lip Segmentation

Tahapan

- Resize
- Landmark Detection
- Cropping
- Masking
- Normalization

Output

- Cropped Lip Image

---

## RGB Feature Extraction

Menghasilkan nilai rata-rata:

- Red
- Green
- Blue

Output

```json
{
    "r": 176,
    "g": 108,
    "b": 114
}
```

---

# 9. AI Classification

## Model

MobileNetV2

Input

224x224 Lip Image

Output

```json
{
    "label": "Pinkish",
    "confidence": 0.96
}
```

Supported Labels

- Pinkish
- Brownish
- Dark

---

# 10. Recommendation Engine

Menggunakan Hybrid Recommendation System.

## Rule-Based Filtering

Input

Lip Type

Output

Candidate Lipsticks

Contoh

Pinkish

↓

Rose Pink

↓

Warm Pink

↓

Soft Nude

---

## Content-Based Filtering

Input

- RGB Bibir
- RGB Lipstick

Metode

Euclidean Distance

Output

Similarity Score

---

## Ranking

Menghasilkan

Top-3 Recommendation

Output

| Rank | Shade | Score |
|------|---------|----------|
| 1 | Rose Pink | 0.962 |
| 2 | Coral Glow | 0.941 |
| 3 | Warm Nude | 0.917 |

---

# 11. Analysis History

Setiap analisis disimpan.

Data

- Original Image
- Cropped Lip
- RGB
- Lip Type
- Confidence
- Recommendation
- Analysis Date

User hanya dapat melihat data miliknya sendiri.

---

# 12. User Profile

User dapat

- Mengubah nama
- Mengubah password
- Melihat jumlah analisis
- Logout

---

# 13. User Flow

```
Landing Page

↓

Register

↓

Login

↓

Dashboard

↓

Upload Image

↓

Face Detection

↓

Lip Detection

↓

RGB Extraction

↓

Classification

↓

Recommendation

↓

Save History

↓

History Detail
```

---

# 14. Success Metrics

| Metric | Target |
|---------|---------|
| Classification Accuracy | ≥90% |
| Recommendation Success Rate | 100% |
| Upload Success Rate | >98% |
| Average Analysis Time | <5 seconds |
| API Availability | 99% |
| Crash Rate | <1% |

---

# 15. Non Functional Requirements

## Performance

- Response API <500 ms
- AI Inference <3 detik
- Total Analysis <5 detik

---

## Security

- HTTPS Only
- JWT Authentication
- HttpOnly Cookie
- Password Hash (bcrypt)
- CSRF Protection
- CORS Protection
- File Validation

---

## Scalability

Sistem harus mendukung:

- Horizontal Scaling
- AI Service terpisah
- Object Storage
- Database Migration

---

## Reliability

- Logging
- Retry Upload
- Error Handling
- Monitoring

---

# 16. Business Rules

- Satu gambar hanya boleh berisi satu wajah.
- Bibir tidak boleh tertutup masker.
- Gambar harus memiliki pencahayaan cukup.
- Hasil rekomendasi selalu berjumlah tiga.
- Riwayat hanya dapat diakses pemilik akun.

---

# 17. Assumptions

- Pengguna mengunggah foto tanpa lipstik tebal.
- Kamera memiliki kualitas yang cukup.
- Wajah menghadap kamera.

---

# 18. Constraints

Model saat ini hanya mengenali:

- Pinkish
- Brownish
- Dark

Input model:

- 224 × 224 pixel

---

# 19. Future Enhancements

Phase 2

- Skin Tone Detection
- Undertone Detection
- Favorite Shades
- Brand Recommendation

Phase 3

- Virtual Try-On
- AI Beauty Assistant
- Live Camera Recommendation
- Marketplace Integration

---

# 20. Acceptance Criteria

## Authentication

- User dapat register.
- User dapat login.
- User dapat logout.

## Analysis

- Upload berhasil.
- Face berhasil dideteksi.
- Lip berhasil dideteksi.
- RGB berhasil diekstraksi.
- Model menghasilkan klasifikasi.
- Recommendation berhasil dibuat.

## History

- Riwayat tersimpan otomatis.
- User dapat membuka kembali hasil analisis.

---

# 21. Technical Assumptions

Dokumen ini hanya mendefinisikan kebutuhan produk.

Detail implementasi mengenai:

- Arsitektur
- Database
- API
- AI Pipeline
- Deployment
- Security
- Testing

akan dijelaskan pada dokumen lain di dalam folder `/docs`.

---

# 22. Deliverables

Versi MVP harus mencakup:

- Web Frontend
- Backend API
- AI Inference Service
- Database
- Object Storage
- Authentication
- Recommendation Engine
- History Module

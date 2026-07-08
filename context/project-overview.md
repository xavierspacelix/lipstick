# Project Overview

## About the Project

AI Lipstick Recommendation System is a full-stack AI-powered web application that helps users discover lipstick shades that best match their natural lip color.

Users upload a face photo through the web application, and the AI pipeline automatically detects the face, extracts the lip region, analyzes its color characteristics, classifies the lip type using a trained MobileNetV2 model, and generates the three most suitable lipstick recommendations using a Hybrid Recommendation System.

The recommendation engine combines Deep Learning, Rule-Based Filtering, and Content-Based Filtering to provide personalized lipstick suggestions based on the user's natural lip color.

Every analysis is stored in the user's personal history, allowing them to revisit previous recommendations without repeating the analysis.

The application is built using a modern service-oriented architecture consisting of a Next.js frontend, FastAPI backend, AI inference service, PostgreSQL database, and object storage.

---

# The Problem It Solves

Choosing the right lipstick shade is difficult for many people.

Most users purchase lipstick based on:

- Social media trends
- Brand recommendations
- Trial and error
- Guesswork

Unfortunately, the same lipstick color can look very different depending on the user's natural lip color.

This application eliminates the guesswork by automatically analyzing the user's lips and recommending lipstick shades that best complement their natural lip characteristics.

Instead of browsing hundreds of shades manually, users simply upload a photo and receive personalized recommendations within seconds.

---

# Pages

```
/                       → Landing Page
/login                  → User Login
/register               → User Registration
/dashboard              → User Dashboard
/analysis               → Upload & Analyze Image
/analysis/[id]          → Analysis Result
/history                → Analysis History
/profile                → User Profile
/settings               → Account Settings
```

---

# Navigation

Top navigation bar.

```
Dashboard
Analyze
History
Profile
```

Desktop

- Fixed top navigation
- Responsive layout
- No sidebar

Mobile

- Bottom navigation
- Responsive design

---

# Core User Flow

## Landing Page

- Hero section
- Product introduction
- Features
- FAQ
- Call To Action
- Login/Register button

---

## Authentication

User creates an account using:

- Name
- Email
- Password

After authentication:

```
Login

↓

Dashboard
```

---

## Dashboard

Dashboard displays:

- Welcome section
- Quick Analyze button
- Recent analyses
- Total analyses
- Latest recommendations

---

## Image Analysis

User opens the Analyze page.

The workflow:

- Upload face image
- Preview image
- Submit analysis

Backend processing:

```
Image Upload

↓

Face Detection

↓

Lip Detection

↓

Lip Segmentation

↓

Image Normalization

↓

RGB Feature Extraction

↓

MobileNetV2 Classification

↓

Hybrid Recommendation

↓

Top 3 Recommendation

↓

Save Analysis

↓

Return Result
```

---

## Recommendation Result

Displays:

### Uploaded Image

Original uploaded image.

### Cropped Lip

Segmented lip region used by the AI model.

### Lip Analysis

- Lip Type
- Confidence Score
- RGB Values

### Recommended Lipsticks

Three lipstick recommendations.

Each recommendation displays:

- Shade Name
- Category
- Similarity Score
- Color Preview

---

## Analysis History

Displays all previous analyses.

Each history item contains:

- Upload Date
- Lip Type
- Recommendation Summary

User can:

- Open details
- Delete history

---

## Profile

User can:

- Update profile
- Change password
- View statistics
- Logout

---

# AI Pipeline

```
Upload Face Image

↓

MediaPipe Face Detection

↓

Face Mesh

↓

Lip Landmark Detection

↓

Lip Segmentation

↓

Crop Lip

↓

Resize Image

↓

Normalize Image

↓

RGB Feature Extraction

↓

MobileNetV2 Classification

↓

Lip Type Prediction

↓

Rule-Based Filtering

↓

Candidate Lipsticks

↓

Content-Based Filtering

↓

Euclidean Distance Similarity

↓

Top 3 Recommendation

↓

Save Analysis
```

---

# System Architecture

```
                Browser

                   │

                   ▼

           Next.js Frontend

                   │

             REST API

                   │

                   ▼

            FastAPI Backend

        ┌──────────────┴──────────────┐

        ▼                             ▼

 PostgreSQL                     Object Storage

        │                             │

        └──────────────┬──────────────┘

                       ▼

               AI Inference Service

                       │

        ┌──────────────┴──────────────┐

        ▼                             ▼

     MediaPipe                 MobileNetV2

                       │

                       ▼

         Hybrid Recommendation Engine
```

---

# Data Architecture

## User Data

Stores:

- Account information
- Authentication
- User preferences

---

## Analysis Data

Stores:

- Uploaded image
- Cropped lip image
- RGB values
- Lip type
- Confidence
- Recommendation results
- Analysis timestamp

---

## Lipstick Knowledge Base

Stores:

- Shade name
- Category
- RGB values
- Metadata

Used by the recommendation engine.

---

# Features In Scope

## Authentication

- Register
- Login
- Logout

## User Management

- Profile
- Password update

## AI Analysis

- Face upload
- Face detection
- Lip detection
- Lip segmentation
- RGB extraction
- Lip classification

## Recommendation

- Rule-Based Filtering
- Content-Based Filtering
- Top-3 Recommendation

## History

- Analysis history
- Detail page
- Delete history

## General

- Responsive UI
- Error handling
- Loading states
- Empty states

---

# Features Out of Scope

- Virtual Try-On (AR)
- Skin Tone Detection
- Undertone Analysis
- Foundation Recommendation
- Blush Recommendation
- Beauty Chatbot
- Marketplace Integration
- Product Reviews
- Social Features
- Mobile Application
- Push Notifications
- Multi-user Organizations
- Subscription System
- Admin Dashboard

---

# Target User

The ideal user is someone who:

- Uses lipstick regularly
- Has difficulty selecting lipstick shades
- Shops for cosmetics online
- Wants personalized recommendations
- Prefers quick and easy beauty tools

---

# Success Criteria

- User can create an account in under one minute.
- Image upload completes successfully for supported formats.
- AI analysis finishes in under five seconds.
- Every successful analysis returns exactly three recommendations.
- Recommendation history is automatically stored.
- The application is fully responsive on desktop, tablet, and mobile browsers.
- The AI model provides consistent and reliable classifications.
- The recommendation engine returns shades relevant to the detected lip type.
- Users can revisit previous analyses without reprocessing the original image.

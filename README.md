# MyRhythm Desktop Prototype

MyRhythm is an academic desktop prototype for emotion-aware music recommendation. It combines a PyQt interface, local user preferences, music metadata, webcam-based facial emotion recognition modules, and BLE heart-rate input modules to explore how detected mood and preferences can influence song recommendations.

This public copy is intentionally sanitized for portfolio review. It does not include the original bulk music library, trained model artifacts, datasets, generated reports, local databases, or runtime outputs.

## Current Scope

- PyQt desktop interface for agreement, login, preferences, recognition, and dashboard flows
- Local SQLite database schema for users, preferences, songs, and extracted audio features
- Recommendation engine that ranks songs using detected emotion labels and stored preferences
- Facial emotion recognition scripts and webcam pipeline code
- BLE heart-rate reader and heart-rate emotion-classification scripts
- Music metadata, feature extraction, scanner, and recommendation modules
- Lightweight UI assets needed to understand the prototype

## Not Included

- MP3 files and cover-image library
- Trained FER, heart-rate, or music-classifier model artifacts
- Training datasets and generated evaluation reports
- Runtime SQLite databases
- Raw webcam captures, face images, heart-rate logs, or emotion logs
- Cloud credentials or third-party auth secrets

See [docs/local-assets.md](docs/local-assets.md), [docs/model-artifacts.md](docs/model-artifacts.md), and [docs/storage-plan.md](docs/storage-plan.md) for the intended asset strategy.

## Tech Stack

- Python
- PyQt5 / Qt Designer
- SQLAlchemy
- SQLite by default, with `DATABASE_URL` support for future database adapters
- OpenCV, TensorFlow/Keras, DeepFace, Librosa, scikit-learn, NumPy, Pandas
- Bleak for BLE heart-rate device scanning
- python-vlc for local music playback

## Project Structure

```text
myrhythm-desktop-prototype/
  app/
    auth/                  # Local prototype auth logic
    database/              # SQLAlchemy schema and models
    fer/                   # Facial emotion recognition scripts
    gui/                   # PyQt UI windows and Qt Designer files
    hr/                    # BLE heart-rate and HR model scripts
    logic/                 # User session and preference logic
    music/                 # Metadata, feature extraction, and recommendation logic
  docs/
    architecture.md
    asset-policy.md
    local-assets.md
    model-artifacts.md
    storage-plan.md
  media/                   # Lightweight UI icons/logos only
  sample_data/
    song_manifest.example.csv
  tests/
  .env.example
  requirements.txt
  run.py
```

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
python run.py
```

The application creates `instance/myrhythm.db` locally. That database is ignored by Git.

## Local Assets

This repository does not ship audio or trained model files. To exercise the full app locally, provide your own licensed local music files and model artifacts, then point the app to them through environment variables or future configuration adapters.

Minimum local asset categories:

- Music library directory
- Song metadata manifest
- FER model artifact
- Optional heart-rate model artifact
- Optional music-classifier artifacts

Use [sample_data/song_manifest.example.csv](sample_data/song_manifest.example.csv) as the metadata shape for future ingestion.

## Cloud Rebuild Direction

The intended rebuild path is local-first, then optional cloud sync:

- Keep the PyQt desktop app as the main client.
- Add a FastAPI backend only after the sanitized local app is stable.
- Use Supabase Auth/Postgres if real cloud accounts and relational metadata are needed.
- Use Cloudflare R2 or another S3-compatible object store for large licensed media and model artifacts.
- Generate signed object URLs from the backend only. Do not put storage secrets in the desktop app.

See [docs/prd-cloud-migration.md](docs/prd-cloud-migration.md) for the staged migration plan.

## Privacy Guardrails

Emotion and heart-rate signals are sensitive, health-adjacent data. This prototype should not upload raw webcam frames, face images, raw heart-rate streams, or emotion logs by default. Do not frame this project as a medical, therapy, stress-reduction, or production wearable product.

## Verification Status

Local verification completed on the sanitized copy:

- No heavy media, model, dataset, database, or secret files were found in the release scan.
- `python -m compileall -q app tests` passed.
- `python -m pytest tests` passed with 3 tests passing and 2 optional dependency suites skipped in the bare local environment.

Before public release, capture screenshots or demo media from the sanitized copy and re-run the same checks after any asset or model changes.

## Portfolio Framing

Safe wording:

> Built an academic PyQt desktop prototype for emotion-aware music recommendation using webcam facial-emotion modules, BLE heart-rate input modules, SQLite-backed preferences, and local music metadata.

Avoid claiming production deployment, guaranteed emotional outcomes, medical use, or support for specific commercial wearable brands unless separately verified.

# MyRhythm Desktop Prototype

<p>
  <img alt="Python" src="https://img.shields.io/badge/-Python-3776AB?style=flat&logo=python&logoColor=white">
  <img alt="PyQt5" src="https://img.shields.io/badge/-PyQt5-41CD52?style=flat&logo=qt&logoColor=white">
  <img alt="SQLite" src="https://img.shields.io/badge/-SQLite-003B57?style=flat&logo=sqlite&logoColor=white">
  <img alt="OpenCV" src="https://img.shields.io/badge/-OpenCV-5C3EE8?style=flat&logo=opencv&logoColor=white">
  <img alt="TensorFlow" src="https://img.shields.io/badge/-TensorFlow-FF6F00?style=flat&logo=tensorflow&logoColor=white">
</p>

MyRhythm is an academic desktop prototype for emotion-aware music recommendation. It combines a PyQt interface, local preferences, music metadata, webcam-based facial emotion recognition modules, and BLE heart-rate modules to explore how mood signals could influence song recommendations.

This public copy is sanitized for portfolio review. It keeps the application structure and documentation, but excludes private datasets, model artifacts, generated outputs, local databases, and music files.

## What It Demonstrates

- PyQt screens for agreement, login, preferences, recognition, and dashboard flows
- SQLAlchemy models for users, preferences, songs, and audio features
- Recommendation logic that ranks songs using detected emotion labels and stored preferences
- Facial emotion recognition pipeline code for webcam-based FER experiments
- BLE heart-rate reader and heart-rate emotion-classification scripts
- Asset, model, and storage documentation for a safer public rebuild

## Run Locally

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
python run.py
```

The app creates `instance/myrhythm.db` locally. That database is ignored by Git.

## Project Map

```text
myrhythm-desktop-prototype/
  app/
    auth/       # Prototype auth logic
    database/   # SQLAlchemy schema and models
    fer/        # Facial emotion recognition scripts
    gui/        # PyQt windows and Qt Designer files
    hr/         # BLE heart-rate and HR model scripts
    logic/      # User session and preferences
    music/      # Metadata, features, scanner, and recommendation logic
  docs/         # Architecture, asset policy, model notes, and storage plan
  media/        # Lightweight UI icons and logos
  sample_data/  # Example song manifest shape
  tests/
```

## Not Included

- MP3 files, cover art, and bulk local music libraries
- Trained FER, heart-rate, or music-classifier model files
- Training datasets, generated reports, runtime logs, or local databases
- Raw webcam captures, face images, raw heart-rate streams, or emotion logs
- Cloud credentials or third-party auth secrets

Use [docs/local-assets.md](docs/local-assets.md), [docs/model-artifacts.md](docs/model-artifacts.md), and [sample_data/song_manifest.example.csv](sample_data/song_manifest.example.csv) when rebuilding local assets.

## Team Notes

Emotion and heart-rate signals are sensitive, health-adjacent data. Keep this prototype local-first unless a backend, consent flow, and storage policy are ready. Do not frame the project as medical software, therapy, stress reduction, or a production wearable product.

The staged cloud direction is documented in [docs/prd-cloud-migration.md](docs/prd-cloud-migration.md): keep PyQt as the client, add a backend before cloud storage, and keep object-storage/database secrets server-side.

## Verification

- Release scan found no committed heavy media, model, dataset, database, or secret files
- `python -m compileall -q app tests` passed
- `python -m pytest tests` passed with 3 tests passing and 2 optional dependency suites skipped in the bare local environment

## Future Improvements

- Add screenshots or a short demo clip from the sanitized copy
- Add clearer dependency groups for base app, FER, HR, and audio features
- Add more unit tests around recommendation and database behavior
- Build a backend only after the local prototype and privacy boundaries are stable

## Portfolio Framing

Built an academic PyQt desktop prototype for emotion-aware music recommendation using webcam facial-emotion modules, BLE heart-rate input modules, SQLite-backed preferences, and local music metadata.

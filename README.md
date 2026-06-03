# MyRhythm Desktop Prototype

<p>
  <a href="https://skillicons.dev">
    <img alt="MyRhythm stack" src="https://skillicons.dev/icons?i=python,qt,sqlite,opencv,tensorflow,scikitlearn&theme=light&perline=6">
  </a>
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

### Supabase Auth

The Sign In and Sign Up screens use Supabase email/password authentication. Copy `.env.example` to `.env` before running the app, then keep only the Supabase project URL and publishable key in that file. Do not add service-role keys, object-storage secrets, or database passwords to the desktop client.

After a successful account creation, the app opens the Sign In screen with the new email already filled in. If email confirmation is enabled in Supabase, confirm the account from the email inbox before signing in.

### Cloud Asset Backend

Curated tracks, cover art, and model binaries are stored in private Cloudflare R2 buckets. The desktop app does not contain R2 credentials; it uses the Cloudflare Worker at `MYRHYTHM_ASSET_API_BASE_URL` with the signed-in user's Supabase access token.

Live demo buckets:

- `myrhythm-music-assets`: 236 tracks and 233 matched cover images
- `myrhythm-ml-models`: 4 model/scaler artifacts

The Worker is deployed at `https://myrhythm-assets-api.zctrl7801.workers.dev`. Its Supabase publishable key is stored as a Wrangler secret, not in source control.

### Demo Reviewer Data

To populate a local SQLite database with generated demo tracks and generated cover art:

```powershell
python scripts/seed_demo_assets.py
```

The generated audio, covers, and database stay under `instance/` and are ignored by Git. This seed script does not create a Supabase Auth account; create a reviewer account from the Sign Up screen or Supabase dashboard.

### Optional Real-Device Features

To run webcam FER and BLE heart-rate recognition, keep model artifacts outside Git and set:

```powershell
$env:MYRHYTHM_FER_MODEL_PATH="C:/path/to/models/myrhythm_fer.h5"
$env:MYRHYTHM_HR_MODEL_PATH="C:/path/to/models/lstm_model.keras"
$env:MYRHYTHM_HR_LABEL_ENCODER_PATH="C:/path/to/models/label_encoder.pkl"
```

Use a local webcam and a BLE heart-rate monitor that exposes the standard Heart Rate Measurement characteristic. The app keeps raw webcam frames and raw heart-rate streams local by default and uses only summary mood labels for recommendations.

## Project Map

```text
myrhythm-desktop-prototype/
  app/
    auth/       # Supabase Auth adapter and auth logic
    cloud/      # Supabase Data API and Cloudflare asset API clients
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
- `python -m pytest tests` passed in the local development environment

## Future Improvements

- Add screenshots or a short demo clip from the sanitized copy
- Add clearer dependency groups for base app, FER, HR, and audio features
- Add more unit tests around recommendation and database behavior
- Build a backend only after the local prototype and privacy boundaries are stable

## Portfolio Framing

Built an academic PyQt desktop prototype for emotion-aware music recommendation using webcam facial-emotion modules, BLE heart-rate input modules, SQLite-backed preferences, and local music metadata.

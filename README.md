# MyRhythm Desktop Prototype

MyRhythm is a PyQt desktop prototype for emotion-aware music recommendation.
The reviewer application uses Supabase Auth and metadata, then securely streams
private tracks, covers, and runtime models from Cloudflare R2 through an
authenticated Cloudflare Worker.

## Reviewer Setup

Prerequisites:

- Python 3.10
- [VLC media player 3.x, 64-bit](https://www.videolan.org/vlc/) installed for
  native libVLC playback
- Internet access
- A webcam or BLE heart-rate monitor only when testing those optional inputs

Run:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python run.py
```

No `.env` file, local database, seed script, external media folder, manual model
download, or cloud credential is required. Create an account or sign in, choose
preferences, and the existing cloud catalog appears in the dashboard.

`requirements.txt` contains only the reviewer runtime. Maintainers working with
the retained legacy SQLite development schema can install
`requirements-offline.txt` instead.

If the live Supabase project has email confirmation enabled, confirm the
account from the Supabase email before signing in. This is a provider setting,
not a reviewer configuration step.

The app checks native VLC before login and explains the prerequisite if it is
missing. `python-vlc` is only the Python binding; installing it does not install
native libVLC.

## Cloud Reviewer Flow

1. Supabase Auth signs the reviewer in.
2. Supabase returns the active song catalog and the reviewer's preferences.
3. Real artists from that catalog populate onboarding preferences.
4. Visible covers load in the background, selected tracks load on demand, and
   required FER/heart-rate models load when the reviewer opens recognition.
5. Every downloaded asset is SHA-256 verified and cached outside the repository.
6. VLC plays the verified local cache file.

The signed-in reviewer flow does not initialize or read SQLite. SQLite modules
remain only for local development, and `scripts/seed_demo_assets.py` remains
the cloud asset-ingestion utility.

## Security Boundary

Desktop applications are public clients. Reviewers can inspect the Supabase
project URL, publishable key, Worker URL, and request shapes, so none of those
values are treated as secrets.

Sensitive credentials are not shipped:

- no Supabase service-role key
- no R2 access key or secret
- no database password
- no Cloudflare API token

The Worker owns private R2 bindings, verifies each Supabase session, checks
asset metadata authorization, rejects unknown keys and oversized objects, and
enforces IP and per-user rate limits. Downloads are byte-size and checksum
verified before the runtime can use them. See
[Production Security](docs/production-security.md).

## Cloud Assets

- `myrhythm-music-assets`: 236 tracks and 233 matched covers
- `myrhythm-ml-models`: FER and heart-rate runtime models
- Worker: `https://myrhythm-assets-api.zctrl7801.workers.dev`

Cloud assets are cached under the operating system's user cache directory, not
inside the clone. Deleting the cache is safe; the app will fetch and verify
assets again.

## Optional Device Features

Webcam FER and BLE heart-rate recognition remain optional. Required runtime
models are provisioned automatically when recognition opens. Raw webcam frames
and raw heart-rate streams stay local by default; the recommender consumes
summary mood labels.

## Project Map

```text
app/
  auth/       Supabase Auth client
  cloud/      Supabase metadata, Worker client, and verified asset cache
  database/   Offline/local development schema and models
  fer/        Facial-emotion recognition
  gui/        PyQt application windows
  hr/         BLE heart-rate recognition
  music/      Catalog and recommendation logic
cloudflare/
  worker/     Authenticated, authorized, rate-limited R2 gateway
docs/         Architecture, security, and asset documentation
tests/        Unit and integration-contract tests
```

## Verification

```powershell
python -m compileall -q app tests run.py
python -m pytest -q
```

The repository intentionally excludes bulk media, model binaries, training
datasets, generated reports, runtime logs, local databases, and all sensitive
credentials.

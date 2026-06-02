# Real-Device Emotion And Music Experience Design

Date: 2026-06-02

## Context

MyRhythm is a sanitized PyQt desktop prototype for emotion-aware music recommendation. The public repository keeps source code, documentation, lightweight UI assets, and sample metadata, but excludes private model artifacts, music files, cover libraries, datasets, generated outputs, local databases, and secrets.

Remote issue #1, "PRD: Cloud Migration for MyRhythm", keeps the PyQt app as the main client, preserves local-first development, and requires a backend-mediated cloud layer before real cloud services are connected. It also requires webcam emotion labels and heart-rate derived labels to be treated as sensitive signals, with raw webcam frames and raw heart-rate streams kept local by default.

The approved direction for this slice is real-device local behavior first, with cloud-ready seams for later Supabase/Postgres metadata and Cloudflare R2 or another S3-compatible object store.

References:

- GitHub issue: https://github.com/J0v1t/myrhythm-desktop-prototype/issues/1
- Supabase Auth docs: https://supabase.com/docs/guides/auth/
- Cloudflare R2 S3-compatible storage docs: https://developers.cloudflare.com/r2/api/s3/

## Goals

- Let a viewer use the real webcam-based facial emotion recognition flow when local model artifacts are configured.
- Let a viewer use the real BLE heart-rate flow when a supported heart-rate monitor and local HR model artifacts are configured.
- Show the current FER label, HR-derived label, BPM, and fused mood inside the Recognition window.
- Use summary emotion labels to drive music recommendations.
- Update the Dashboard with recommended songs, placeholder or configured covers, current song details, and a short recommendation reason.
- Keep the implementation local-first while making later Supabase and R2 integration natural.
- Keep sensitive raw inputs and excluded artifacts out of Git.

## Non-Goals

- Do not build the cloud backend in this slice.
- Do not upload music, cover libraries, model artifacts, datasets, or generated reports.
- Do not restore removed private artifacts into Git.
- Do not store raw webcam frames, face crops, raw heart-rate streams, local databases, `.env` files, model binaries, audio files, or cover libraries in the public repository.
- Do not frame MyRhythm as medical software, therapy, diagnosis, or stress detection.
- Do not add missing-cover reports. Missing covers should quietly use `media/default_cover.png`.

## Architecture

The current Recognition window directly owns hardware setup, model loading, signal state, mood selection, and recommendation triggering. That module is shallow: callers and tests must understand too much implementation detail to exercise the core behavior.

The deeper shape is an **Emotion Signal Session** Module. Its interface is small:

- start and stop FER
- start and stop heart-rate monitoring
- expose FER status, FER label, and confidence
- expose HR status, BPM, and HR-derived label
- expose fused mood
- emit status changes suitable for the PyQt UI

Behind that seam, concrete adapters own device and model details:

- `WebcamFerAdapter` opens the webcam, loads the FER model from configured local paths, runs inference, and emits label/confidence/status summaries.
- `BleHeartRateAdapter` scans for BLE heart-rate devices, loads HR model artifacts from configured local paths, parses BPM, runs HR emotion logic, and emits BPM/label/status summaries.
- A lightweight model-artifact adapter resolves local artifact paths now and can later be replaced by a backend-backed model manifest adapter.

The Dashboard should depend on a **Song Catalog** Module instead of querying songs and covers directly. Its interface returns usable song records with title, artist, genre, duration, local playback path or future signed object URL, and cover path or placeholder. For now, the catalog can read SQLite and local manifests. Later, another adapter can read Supabase/Postgres metadata through a backend interface and use R2 object references for signed cover/audio URLs.

The recommendation Module should receive summary labels and catalog/user context. It should not receive raw frames or raw HR streams. It can return ranked song records plus a short reason such as `Recommended for fused mood: Happy`.

## Runtime Flow

1. The Dashboard opens and loads songs through the Song Catalog Module.
2. The viewer clicks the emotion/heart-rate entry button.
3. The Recognition window opens an Emotion Signal Session.
4. If FER is enabled, the session loads the configured FER model, opens the webcam, and emits facial emotion labels plus confidence.
5. If heart rate is enabled, the session loads the configured HR model artifacts, scans for a BLE heart-rate monitor, and emits BPM plus HR-derived emotion labels.
6. The session fuses FER and HR labels into one summary mood: `happy`, `neutral`, `sad`, or `angry`.
7. When the viewer proceeds, the recommendation Module receives FER label, HR label, fused mood, and user/catalog context.
8. The Dashboard updates playlist order, cover placeholders or configured covers, current song panel, up-next list, and recommendation reason.

## Data And Artifacts

Local runtime configuration should use environment variables or an ignored local config file:

- `MYRHYTHM_FER_MODEL_PATH`
- `MYRHYTHM_HR_MODEL_PATH`
- `MYRHYTHM_HR_LABEL_ENCODER_PATH`
- `MYRHYTHM_SONG_MANIFEST`
- `MYRHYTHM_MUSIC_DIR`
- optional local cover directory variables

The local Song Catalog should accept song records with:

- title
- artist
- genre
- duration
- local audio path
- cover path
- license status
- source notes

If a cover path is absent or invalid, the Dashboard uses `media/default_cover.png` without producing a report.

The future cloud shape maps the same concepts to Supabase/Postgres metadata and object storage:

- `profiles`
- `user_preferences`
- `songs`
- `audio_features`
- `storage_objects`
- `model_artifacts`
- `recommendation_runs`
- `recommendation_items`
- optional `emotion_events`

Cloudflare R2 or another S3-compatible object store should hold binary objects only: licensed audio, cover art, model artifacts, and large reports. Supabase/Postgres should hold metadata, checksums, license status, object keys, lifecycle status, and user/recommendation relationships. The desktop app should eventually receive short-lived signed URLs from a backend interface, not object-storage credentials.

Sensitive signal records should be summaries only:

- FER label
- FER confidence/status
- HR-derived label
- current BPM summary when needed for display
- fused mood
- timestamp
- recommendation run identifier

Raw webcam frames, face crops, raw BPM streams, generated final-emotion logs, and local secrets are not persisted by default.

## UI And Status Handling

The Recognition window should show device and model status in the app instead of relying on terminal output.

FER statuses:

- `Off`
- `Loading model`
- `Camera active`
- `No webcam detected`
- `Model missing`
- `Error`

Heart-rate statuses:

- `Off`
- `Loading model`
- `Scanning BLE`
- `Connected`
- `Device not found`
- `Model missing`
- `Error`

The mood display should show:

- FER label and confidence when available
- HR-derived label when available
- current BPM when available
- fused mood

The Dashboard should show:

- recommended playlist
- current song title and artist
- placeholder or configured cover
- up-next list
- short recommendation reason

## Testing

Tests should target the interfaces where behavior crosses seams:

- Emotion fusion from FER and HR summary labels.
- Emotion Signal Session state transitions without real hardware.
- Missing model path resolution for FER and HR.
- BLE heart-rate measurement parsing.
- Recommendation input/output using summary mood labels.
- Song Catalog cover fallback to `media/default_cover.png`.
- Dashboard conversion of recommendation results into playable song records.
- Privacy regression scans for raw webcam frames, face crops, raw BPM streams, `.env`, databases, model binaries, audio files, and cover libraries.

Optional dependency tests can skip cleanly when local ML/audio dependencies, model artifacts, heart-rate hardware, webcam access, or licensed assets are absent. The main test suite should still pass in a bare reviewer environment.

## Implementation Notes

The first implementation plan should start with tests around the deepened interfaces before editing production code. A narrow order is:

1. Add model path resolution tests and implementation.
2. Add Emotion Signal Session state tests and implementation.
3. Add FER and HR adapters behind the session seam.
4. Add Song Catalog cover fallback tests and implementation.
5. Wire the Recognition window to the session interface.
6. Wire Dashboard recommendation display to catalog-normalized song records.
7. Update README/local asset docs with the new real-device setup path.

This keeps the first slice focused on real local hardware while preserving the later Supabase/R2 direction from issue #1.

# Storage Plan

## Phase 1: Local-First

- SQLite remains the default database.
- `DATABASE_URL` can override the database URI for future adapters.
- Music and model files stay local and outside Git.
- Tests that require audio use `MYRHYTHM_SAMPLE_AUDIO`.

## Phase 2: Supabase Auth And Metadata

Supabase is now the identity and metadata system for the cloud-backed demo.
The desktop app uses Supabase Auth for sign-up/sign-in and stores user
preferences in Supabase when the signed-in user has a Supabase access token.

Current Supabase tables:

- `profiles`: one profile row per Supabase Auth user
- `user_preferences`: user-owned favorite genres, favorite artists, and mood mappings
- `songs`: catalog metadata for curated tracks
- `song_emotion_labels`: curated or model-generated song emotion labels
- `asset_objects`: object-storage metadata for tracks, covers, and models
- `model_artifacts`: versioned ML model metadata

All public tables have row-level security enabled. User-owned tables are scoped
to `auth.uid()`. Catalog and active model metadata are readable by authenticated
users, but binary media and model files are not stored in Supabase Postgres.

## Phase 3: Cloudflare R2 Asset Backend

Cloudflare R2 stores binaries only:

- `myrhythm-music-assets`
  - `tracks/{song-slug}.mp3`
  - `covers/{song-slug}.webp`
- `myrhythm-ml-models`
  - `fer/{version}/myrhythm_fer.h5`
  - `heart-rate/{version}/lstm_model.keras`
  - `heart-rate/{version}/label_encoder.pkl`
  - `music/{version}/scaler.pkl`

The live demo catalog has 236 track objects, 233 matched cover objects, and 4
model/scaler objects. Supabase stores the searchable metadata in `songs`,
`asset_objects`, and `model_artifacts`; R2 stores only the private binary
objects.

The desktop client must never receive R2 API tokens. The Cloudflare Worker
`myrhythm-assets-api` owns the R2 bindings and validates the Supabase access
token before streaming private objects.

Deployed Worker:

- `https://myrhythm-assets-api.zctrl7801.workers.dev`
- routes: `/health`, `/assets/music/{object_key}`, `/assets/models/{object_key}`
- secret: `SUPABASE_PUBLIC_KEY` stored with Wrangler, not committed

Recommended runtime flow:

```text
PyQt desktop app
  -> Supabase Auth sign-in
  -> Supabase Postgres metadata read
  -> Cloudflare Worker with Supabase access token
  -> Cloudflare R2 object stream or short-lived asset URL
```

Wrangler is the deployment path for R2 buckets and Workers. Authenticate it with
`npx wrangler login` or a scoped Cloudflare API token before creating buckets or
deploying. Keep all Cloudflare tokens in local environment variables or Wrangler
secrets; never commit them.

R2 bucket access is private. Requests without a valid Supabase bearer token
return `401`, and malformed object keys return `400`.

## Phase 4: Backend API

Add FastAPI only after the local desktop app is stable.

Backend responsibilities:

- verify auth tokens
- manage user profiles and preferences
- manage song metadata and feature records
- issue signed URLs for private object storage
- expose model manifests
- avoid raw biometric or media-data logging

## Cloud Services

Recommended first cloud stack:

- Supabase Auth for managed user identity
- Supabase Postgres for relational metadata
- Cloudflare R2 for curated media and model artifacts

Cloudflare R2 should store objects only. Keep metadata in Supabase Postgres or
SQLite.

Never put object-storage secrets, Supabase service-role keys, or database passwords in the desktop client.

# Storage Plan

## Phase 1: Local-First

- SQLite remains the default database.
- `DATABASE_URL` can override the database URI for future adapters.
- Music and model files stay local and outside Git.
- Tests that require audio use `MYRHYTHM_SAMPLE_AUDIO`.

## Phase 2: Backend API

Add FastAPI only after the local desktop app is stable.

Backend responsibilities:

- verify auth tokens
- manage user profiles and preferences
- manage song metadata and feature records
- issue signed URLs for private object storage
- expose model manifests
- avoid raw biometric or media-data logging

## Phase 3: Cloud Services

Recommended first cloud stack:

- Supabase Auth for managed user identity
- Supabase Postgres for relational metadata
- Supabase Storage for small curated assets, or Cloudflare R2 for larger licensed media/model artifacts

Cloudflare R2 should store objects only. Keep metadata in Postgres or SQLite.

Never put object-storage secrets, Supabase service-role keys, or database passwords in the desktop client.

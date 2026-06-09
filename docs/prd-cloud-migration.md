# PRD: Cloud Migration for MyRhythm

> Historical planning document. The signed-in reviewer runtime described here
> has since been implemented with Supabase metadata and an authenticated
> Cloudflare R2 Worker. See `docs/cloud-reviewer-experience.md`.

## Problem Statement

MyRhythm is currently a sanitized academic desktop prototype. It can show the application structure, local preferences, recommendation logic, and emotion/heart-rate integration modules, but it is not ready for real cloud-backed users or shared music/model assets.

The original project artifacts were removed from the public repository because they included bulky local media, trained models, datasets, generated reports, and private runtime outputs. Those removed artifacts should not be restored directly into Git. The product needs a safe architecture for real accounts, database-backed metadata, licensed media storage, model artifact storage, and privacy-sensitive emotion/heart-rate handling.

## Solution

Build a backend-mediated cloud layer while keeping the PyQt desktop app as the main client. The backend owns authentication integration, database access, object-storage signing, ingestion workflows, and privacy controls. The desktop app talks to backend APIs and never stores service-role database credentials, object-storage keys, or third-party auth secrets.

Use the database for structured records and relationships. Use object storage for large files. Specifically:

- Store users, preferences, song metadata, audio features, model versions, recommendation runs, and asset references in Postgres.
- Store licensed audio files, cover images, trained model artifacts, and generated large reports in Cloudflare R2 or another S3-compatible object store.
- Store object keys, checksums, MIME types, ownership, license status, and version metadata in the database.
- Generate short-lived signed URLs through the backend when the desktop client needs an object.

## User Stories

1. As a new user, I want to sign up securely, so that my preferences and recommendation history are tied to my account.
2. As a returning user, I want to sign in from the desktop app, so that I can access my saved preferences.
3. As a user, I want my favorite genres and artist preference categories saved remotely, so that my setup persists across devices.
4. As a user, I want the app to recommend songs from a licensed catalog, so that recommendations are based on real metadata without bundling files in Git.
5. As a user, I want cover art and audio playback assets to load only when needed, so that the desktop app stays lightweight.
6. As a user, I want the app to avoid uploading raw webcam frames by default, so that sensitive local signals stay private.
7. As a user, I want raw heart-rate streams to stay local unless I explicitly enable syncing, so that sensitive health-adjacent data is protected.
8. As a user, I want recommendation history stored as summary records, so that the app can improve continuity without storing unnecessary sensitive raw inputs.
9. As an administrator, I want to upload licensed songs and cover art through a controlled ingestion workflow, so that only approved assets enter storage.
10. As an administrator, I want to register a model artifact with version, checksum, and compatibility metadata, so that desktop clients can use the correct model safely.
11. As an administrator, I want to mark assets as active, archived, or blocked, so that the catalog can be maintained without deleting audit history.
12. As an administrator, I want to rotate model artifacts without changing the desktop code, so that model updates can be managed through metadata.
13. As a developer, I want the backend to own storage signing, so that R2/S3 credentials never ship in the desktop client.
14. As a developer, I want database access isolated behind backend modules, so that desktop code does not depend on cloud database internals.
15. As a developer, I want local development to keep working with SQLite or local fixtures, so that the prototype remains easy to run without cloud accounts.
16. As a developer, I want clear environment variable documentation, so that cloud configuration can be set up safely.
17. As a reviewer, I want the public repository to stay free of private media, models, datasets, and secrets, so that the project remains safe to inspect.
18. As a hiring reviewer, I want the README to explain what is included and excluded, so that the project is credible without overclaiming production readiness.
19. As a privacy reviewer, I want explicit guardrails around webcam, emotion, and heart-rate data, so that the project is not framed as medical or therapeutic software.
20. As a future maintainer, I want database migrations and API contracts documented, so that the cloud migration can be implemented in small, reviewable steps.
21. As a future maintainer, I want storage object keys tied to database records, so that orphaned assets and broken references can be detected.
22. As a future maintainer, I want tests around backend authorization, asset signing, and recommendation metadata, so that cloud behavior can be changed safely.

## Implementation Decisions

- Keep the PyQt desktop app as the main client.
- Add a backend API before connecting the desktop app to real cloud services.
- Prefer Supabase Auth and Supabase Postgres for the first cloud-backed version because the project needs authentication and relational metadata.
- Use Cloudflare R2 or another S3-compatible object store for large licensed media and model artifacts.
- The desktop app must not contain R2 keys, S3 keys, Supabase service-role keys, or direct production database credentials.
- The backend will issue short-lived signed URLs for audio, cover art, model artifact, and report downloads.
- The database stores metadata, not the binary objects themselves.
- The public repository must continue excluding bundled music, cover libraries, trained model binaries, local datasets, generated reports, local databases, and `.env` files.
- Preserve local-first development with SQLite and sample manifests for reviewers who do not have cloud credentials.
- Introduce a backend module for authentication, profile lookup, and session validation.
- Introduce a catalog module for song records, artist/genre metadata, asset status, and audio feature lookup.
- Introduce an asset registry module for object keys, checksums, MIME types, byte sizes, storage provider, license status, and lifecycle status.
- Introduce a model registry module for model artifact type, version, checksum, compatibility, activation state, and storage object reference.
- Introduce a recommendation history module for runs and ranked recommendation items.
- Treat webcam emotion labels and heart-rate derived labels as sensitive signals. Store only summary records needed for product behavior, not raw frames or raw biometric streams.
- Recommended initial tables: `profiles`, `user_preferences`, `songs`, `audio_features`, `storage_objects`, `model_artifacts`, `recommendation_runs`, `recommendation_items`, and optional `emotion_events`.
- Use row-level ownership rules for user-owned records and backend-only permissions for catalog/model administration.
- Use a controlled ingestion path for music and models. Do not let arbitrary desktop clients upload directly to public buckets.
- Keep unlicensed third-party media and datasets out of the cloud migration. Only upload assets Jason has the right to use.
- Document any future third-party auth provider change before implementation. Clerk, Auth0, and Descope are possible alternatives, but they add complexity if Supabase already handles auth and database needs.

## Testing Decisions

- Test external behavior through backend API responses and database side effects, not internal implementation details.
- Add auth tests for sign-up, sign-in, invalid credentials, expired sessions, and unauthorized access.
- Add profile/preference tests for creating, reading, updating, and isolating user preferences.
- Add catalog tests for song metadata ingestion, duplicate detection, inactive assets, and missing object references.
- Add asset registry tests for checksum validation, MIME type handling, signed URL generation, and expired URL behavior.
- Add model registry tests for active model selection, version changes, checksum matching, and missing artifact behavior.
- Add recommendation tests for storing a recommendation run and ranked items without storing raw webcam frames or raw heart-rate streams.
- Add privacy regression tests to ensure raw webcam frames, face crops, raw heart-rate streams, and local secrets are not persisted by default.
- Add local-mode tests to ensure the desktop prototype still works with SQLite/sample fixtures when cloud credentials are absent.
- Existing test precedent: optional dependency tests can skip cleanly when local ML/audio dependencies or licensed assets are absent.

## Out of Scope

- Building a production music-streaming platform.
- Uploading copyrighted songs, scraped cover art, or datasets without rights.
- Medical, therapy, diagnosis, stress-detection, or health-product claims.
- Storing raw webcam frames, face images, or raw heart-rate streams by default.
- Direct desktop access to production database credentials or object-storage credentials.
- Migrating original private Git history into the public repository.
- Implementing payments, subscriptions, social sharing, mobile apps, or production analytics.
- Replacing the PyQt client with a web app in this migration phase.

## Further Notes

The immediate next implementation should be a small backend skeleton with local development configuration, database migrations, and one vertical slice: authenticated user profile plus preference sync. Only after that should the project add catalog ingestion, R2 object storage, model artifact registry, and signed-download flows.

The public repository should keep presenting MyRhythm as a sanitized academic prototype until the cloud-backed implementation is actually built, tested, and documented.

# Cloud Reviewer Experience

## Goal

A reviewer can clone the repository, install the documented system and Python
dependencies, create an account, and immediately browse and play the existing
cloud catalog. Reviewers do not seed demo assets, configure local media paths,
or populate a local SQLite database.

## Source Of Truth

The signed-in application is cloud-first:

- Supabase Auth manages reviewer accounts.
- Supabase Postgres stores preferences, song metadata, emotion labels, R2
  object keys, checksums, and model manifests.
- Cloudflare R2 stores private track, cover, and model binaries.
- The Cloudflare Worker authenticates, authorizes, and rate-limits asset
  downloads.

SQLite remains available only to offline ingestion and development scripts. It
is not part of the signed-in reviewer flow.

## Runtime Flow

```text
Sign in
  -> create authenticated Supabase and Cloudflare clients
  -> load active song catalog from Supabase
  -> show catalog immediately with built-in placeholders
  -> lazily fetch and checksum-verify visible covers into the local cache
  -> download and checksum-verify a selected track into the local cache
  -> play the cached local track with libVLC
```

When recognition opens, FER and heart-rate recognition use the same
authenticated cache mechanism for their versioned model artifacts.
Music-classifier artifacts remain offline ingestion tools and are not required
by the reviewer application.

## Local Storage

The application may create an automatic cache outside the repository. The cache
contains only reproducible cloud assets and can be deleted at any time.

The cache:

- uses stable object-key and checksum-derived paths;
- writes downloads atomically;
- verifies registered byte size and SHA-256 before exposing a file to the runtime;
- never stores Supabase, Cloudflare, or R2 credentials;
- does not require reviewer configuration.

## VLC

The source-clone experience keeps `python-vlc` because the current dashboard and
playback controls are built around libVLC. `python-vlc` is only a Python binding;
a matching native VLC/libVLC installation is also required.

The app performs a startup readiness check and displays a clear installation
message if libVLC is unavailable. A future Windows one-folder release can bundle
the libVLC runtime and plugins so release reviewers do not install VLC
separately.

## Failure Behavior

- Catalog failure: show a useful cloud-service error instead of an empty SQLite
  dashboard.
- Cover failure: keep the built-in placeholder and allow the rest of the catalog
  to work.
- Track failure: keep the UI responsive and report that playback could not be
  prepared.
- Model failure: keep music browsing/playback available and disable only the
  affected recognition mode.
- Missing VLC: stop before opening the dashboard and show the exact prerequisite.

## Security Boundary

The Supabase project URL, publishable key, Worker URL, and API shapes are public
client configuration. Security is enforced through Supabase RLS, authenticated
Worker authorization, private R2 bindings, checksums, and rate limits. No
service-role key, R2 credential, database password, or Cloudflare API token is
shipped to reviewers.

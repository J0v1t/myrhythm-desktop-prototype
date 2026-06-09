# MyRhythm Architecture

## Signed-In Reviewer Runtime

```mermaid
flowchart LR
  User["Reviewer"] --> Desktop["PyQt Desktop App"]
  Desktop --> Auth["Supabase Auth"]
  Desktop --> Metadata["Supabase Postgres Metadata"]
  Desktop --> Worker["Cloudflare Worker"]
  Worker --> R2["Private Cloudflare R2"]
  R2 --> Cache["Verified User Asset Cache"]
  Cache --> VLC["Native libVLC Playback"]
  Cache --> Models["FER and Heart-Rate Runtime Models"]
```

Supabase is the source of truth for reviewer identity, preferences, song
metadata, asset object keys, checksums, and model manifests. Cloudflare R2
stores private binary assets. The Worker validates Supabase sessions,
authorizes object metadata, rate-limits requests, and streams R2 objects.

The signed-in runtime does not initialize or query SQLite. Local SQLAlchemy
modules and sample-ingestion scripts remain for offline development only.

## Client Security Boundary

The desktop app contains only public client configuration. It never contains
R2 credentials, a Supabase service-role key, a database password, or a
Cloudflare API token. Raw webcam frames and raw heart-rate streams remain local
by default.

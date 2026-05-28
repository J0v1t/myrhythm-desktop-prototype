# Local Assets

The original project used a local music library, cover images, trained models, and generated outputs. This public copy removes those files.

## Expected Local Paths

Use environment variables or future config adapters to point to local assets:

- `MYRHYTHM_MUSIC_DIR`
- `MYRHYTHM_SONG_MANIFEST`
- `MYRHYTHM_SAMPLE_AUDIO`

## Song Manifest

Use `sample_data/song_manifest.example.csv` as the starting shape for local ingestion.

Required fields:

- `title`
- `artist`
- `genre`
- `duration_seconds`
- `local_file_path`
- `cover_path`
- `license_status`
- `source_notes`

## Runtime Files

Runtime databases and generated outputs belong under ignored local paths such as `instance/`, `datasets/`, `models/`, or `artifacts/`.

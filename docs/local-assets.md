# Local Assets

The reviewer application automatically downloads and verifies cloud assets.
Local paths are supported only for maintainer development and controlled asset
ingestion. Install `requirements-offline.txt` only when working with the
retained local SQLite schema.

## Expected Local Paths

Maintainers may use environment variables to point offline tools to local assets:

- `MYRHYTHM_MUSIC_DIR`
- `MYRHYTHM_SONG_MANIFEST`
- `MYRHYTHM_SAMPLE_AUDIO`
- `MYRHYTHM_FER_MODEL_PATH`
- `MYRHYTHM_HR_MODEL_PATH`

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

The signed-in app provisions FER and heart-rate runtime models automatically.
It reports missing camera or BLE device status in the Recognition window and
does not persist raw webcam frames, face crops, or raw heart-rate streams.

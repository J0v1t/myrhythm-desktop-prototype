# Local Assets

The original project used a local music library, cover images, trained models, and generated outputs. This public copy removes those files.

## Expected Local Paths

Use environment variables or future config adapters to point to local assets:

- `MYRHYTHM_MUSIC_DIR`
- `MYRHYTHM_SONG_MANIFEST`
- `MYRHYTHM_SAMPLE_AUDIO`
- `MYRHYTHM_FER_MODEL_PATH`
- `MYRHYTHM_HR_MODEL_PATH`
- `MYRHYTHM_HR_LABEL_ENCODER_PATH`

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

## Real-Device Local Setup

For webcam FER and BLE heart-rate testing, keep model artifacts outside Git and point the app to them with:

- `MYRHYTHM_FER_MODEL_PATH`
- `MYRHYTHM_HR_MODEL_PATH`
- `MYRHYTHM_HR_LABEL_ENCODER_PATH`

The desktop app should show missing model, missing camera, or missing BLE device status in the Recognition window. It should not persist raw webcam frames, face crops, or raw heart-rate streams by default.

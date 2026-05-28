# Asset Policy

This public repository must not contain bulk audio, cover libraries, trained model binaries, datasets, generated reports, local databases, or runtime biometric/emotion output.

## Allowed

- Source code
- Lightweight UI icons and logos
- README and architecture docs
- Example metadata files with placeholder paths
- Tests that skip when local assets are absent

## Not Allowed

- MP3, WAV, FLAC, OGG, or M4A files
- Full cover-image libraries
- `.h5`, `.keras`, `.pkl`, or other trained model binaries
- Training datasets and exported features
- Runtime SQLite databases
- Raw webcam frames or face images
- Raw heart-rate streams
- Emotion logs or generated final-emotion files
- Cloud credentials, tokens, service-role keys, R2 secrets, or database passwords

## License Rule

Only include or host media after the asset license is documented. Until then, keep audio and cover art local and outside Git.

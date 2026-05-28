# Model Artifacts

Trained models are intentionally excluded from this public repository.

## Excluded Artifacts

- FER model: `app/fer/trained_models/myrhythm_fer.h5`
- Heart-rate model: `app/hr/trained_hr_models/lstm_model.keras`
- Heart-rate label encoder: `app/hr/trained_hr_models/label_encoder.pkl`
- Music classifier/scaler artifacts under `app/music/trained_models/`

## Future Handling

For local development, keep model files outside Git and point the application to them through configuration.

For a cloud-backed rebuild, store model artifacts in private object storage and expose them through backend-issued signed URLs. Each model should have:

- artifact type
- version
- SHA256 checksum
- framework/runtime version
- label list
- training-data note
- storage object key

Do not claim model performance until the training data, evaluation split, and generated reports are verified.

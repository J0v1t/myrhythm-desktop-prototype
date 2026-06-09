# Model Artifacts

Trained models are intentionally excluded from this public repository.

## Excluded Artifacts

- FER model: `app/fer/trained_models/myrhythm_fer.h5`
- Heart-rate model: `app/hr/trained_hr_models/lstm_model.keras`
- Music classifier/scaler artifacts under `app/music/trained_models/`

## Cloud Handling

Runtime model artifacts are stored in private R2 and exposed through the
authenticated Cloudflare Worker. Supabase stores each active model manifest:

- artifact type
- version
- SHA256 checksum
- framework/runtime version
- label list
- training-data note
- storage object key

Do not claim model performance until the training data, evaluation split, and generated reports are verified.

## Runtime Resolution

After sign-in, the app automatically downloads and verifies the active FER and
heart-rate models into the user cache. The heart-rate output label order is
fixed in source, so the public runtime does not deserialize a label-encoder
artifact. Maintainers can still override the model paths for offline testing:

- `MYRHYTHM_FER_MODEL_PATH`
- `MYRHYTHM_HR_MODEL_PATH`

Missing artifacts disable only the affected recognition mode; music browsing
and playback remain available.

"""Provision reviewer-runtime model artifacts into an injected cache."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping, Optional, Union


ModelArtifact = object
ModelManifest = Union[Mapping[str, ModelArtifact], Iterable[ModelArtifact]]

RUNTIME_ASSET_ENV_NAMES = {
    "fer_model": "MYRHYTHM_FER_MODEL_PATH",
    "hr_model": "MYRHYTHM_HR_MODEL_PATH",
}

ARTIFACT_TYPE_ALIASES = {
    "fer": "fer_model",
    "fer_model": "fer_model",
    "heart_rate": "hr_model",
    "heart_rate_model": "hr_model",
    "hr": "hr_model",
    "hr_model": "hr_model",
    "heart_rate_label_encoder": "hr_label_encoder",
    "hr_label_encoder": "hr_label_encoder",
}


@dataclass(frozen=True)
class ModelProvisioningResult:
    provisioned: Mapping[str, Path]
    failures: Mapping[str, str]
    runtime_asset_overrides: Mapping[str, str]


def _manifest_entries(model_manifest: ModelManifest) -> Iterable[ModelArtifact]:
    if isinstance(model_manifest, Mapping):
        for artifact_type, artifact in model_manifest.items():
            if isinstance(artifact, Mapping):
                entry = dict(artifact)
                entry.setdefault("artifact_type", artifact_type)
                yield entry
            else:
                yield artifact
        return
    yield from model_manifest


def _artifact_value(artifact: ModelArtifact, field: str) -> object:
    if isinstance(artifact, Mapping):
        return artifact.get(field)
    return getattr(artifact, field, None)


def _canonical_artifact_type(artifact: ModelArtifact) -> str:
    artifact_type = (
        str(_artifact_value(artifact, "artifact_type") or "")
        .strip()
        .lower()
        .replace("-", "_")
    )
    return ARTIFACT_TYPE_ALIASES.get(artifact_type, artifact_type)


def _ensure_cached_model(
    model_cache: object,
    artifact: ModelArtifact,
    asset_client: Optional[object],
) -> Union[str, Path]:
    ensure_model = getattr(model_cache, "ensure_model", None)
    if callable(ensure_model):
        return ensure_model(artifact)

    get_model_asset = getattr(model_cache, "get_model_asset", None)
    if not callable(get_model_asset):
        raise TypeError("Model cache must provide ensure_model() or get_model_asset().")
    if asset_client is None:
        raise ValueError("An asset client is required by this model cache.")

    object_key = str(_artifact_value(artifact, "object_key") or "")
    checksum = str(_artifact_value(artifact, "checksum_sha256") or "")
    expected_size = _artifact_value(artifact, "byte_size")
    if not object_key or not checksum:
        raise ValueError("Model manifest entry is missing object key or SHA-256 checksum.")
    return get_model_asset(
        asset_client,
        object_key,
        checksum,
        expected_size=expected_size,
    )


def provision_models(
    model_manifest: ModelManifest,
    model_cache: object,
    asset_client: Optional[object] = None,
) -> ModelProvisioningResult:
    """Provision required reviewer models while isolating per-artifact failures."""
    provisioned: dict[str, Path] = {}
    failures: dict[str, str] = {}
    overrides: dict[str, str] = {}
    found_artifact_types: set[str] = set()

    for artifact in _manifest_entries(model_manifest):
        artifact_type = _canonical_artifact_type(artifact)
        env_name = RUNTIME_ASSET_ENV_NAMES.get(artifact_type)
        if env_name is None or artifact_type in found_artifact_types:
            continue

        found_artifact_types.add(artifact_type)
        try:
            path = Path(
                _ensure_cached_model(model_cache, artifact, asset_client)
            ).expanduser().resolve()
            if not path.is_file():
                raise FileNotFoundError(f"Cache did not provide a file: {path}")
        except Exception as exc:
            failures[artifact_type] = str(exc)
            continue

        provisioned[artifact_type] = path
        overrides[env_name] = str(path)

    for artifact_type in RUNTIME_ASSET_ENV_NAMES:
        if artifact_type not in found_artifact_types:
            failures[artifact_type] = (
                f"Model manifest does not include required artifact: {artifact_type}"
            )

    return ModelProvisioningResult(
        provisioned=provisioned,
        failures=failures,
        runtime_asset_overrides=overrides,
    )


def provision_runtime_models(
    model_manifest: ModelManifest,
    model_cache: object,
    asset_client: Optional[object] = None,
) -> ModelProvisioningResult:
    """Compatibility name describing the intended reviewer-runtime use."""
    return provision_models(model_manifest, model_cache, asset_client)

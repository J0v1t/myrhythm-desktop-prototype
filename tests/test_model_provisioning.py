from pathlib import Path
from types import SimpleNamespace

from app.cloud.model_provisioning import provision_models


MODEL_MANIFEST = [
    {"artifact_type": "fer_model", "object_key": "fer/v1/myrhythm_fer.h5"},
    {"artifact_type": "hr_model", "object_key": "heart-rate/v1/lstm_model.keras"},
    {
        "artifact_type": "hr_label_encoder",
        "object_key": "heart-rate/v1/label_encoder.pkl",
    },
    {"artifact_type": "music_scaler", "object_key": "music/v1/scaler.pkl"},
]


class FakeModelCache:
    def __init__(self, cache_dir: Path, failing_artifacts=()):
        self.cache_dir = cache_dir
        self.failing_artifacts = set(failing_artifacts)
        self.requested = []

    def ensure_model(self, artifact):
        artifact_type = artifact["artifact_type"]
        self.requested.append(artifact_type)
        if artifact_type in self.failing_artifacts:
            raise RuntimeError(f"{artifact_type} download failed")
        path = self.cache_dir / Path(artifact["object_key"]).name
        path.write_text(artifact_type, encoding="utf-8")
        return path


def test_provision_models_exposes_runtime_overrides_and_ignores_music_scaler(tmp_path):
    cache = FakeModelCache(tmp_path)

    result = provision_models(MODEL_MANIFEST, cache)

    assert result.runtime_asset_overrides == {
        "MYRHYTHM_FER_MODEL_PATH": str(tmp_path / "myrhythm_fer.h5"),
        "MYRHYTHM_HR_MODEL_PATH": str(tmp_path / "lstm_model.keras"),
    }
    assert result.failures == {}
    assert cache.requested == ["fer_model", "hr_model"]


def test_provision_models_isolates_each_model_failure(tmp_path):
    cache = FakeModelCache(tmp_path, failing_artifacts={"hr_model"})

    result = provision_models(MODEL_MANIFEST, cache)

    assert set(result.provisioned) == {"fer_model"}
    assert result.failures == {"hr_model": "hr_model download failed"}
    assert "MYRHYTHM_HR_MODEL_PATH" not in result.runtime_asset_overrides
    assert result.runtime_asset_overrides["MYRHYTHM_FER_MODEL_PATH"].endswith(
        "myrhythm_fer.h5"
    )


def test_provision_models_accepts_manifest_mapping(tmp_path):
    manifest = {entry["artifact_type"]: entry for entry in MODEL_MANIFEST}
    cache = FakeModelCache(tmp_path)

    result = provision_models(manifest, cache)

    assert set(result.provisioned) == {
        "fer_model",
        "hr_model",
    }


def test_provision_models_supports_cloud_manifest_records_and_asset_cache(tmp_path):
    client = object()
    manifest = [
        SimpleNamespace(
            artifact_type="fer",
            object_key="fer/v1/myrhythm_fer.h5",
            checksum_sha256="a" * 64,
            byte_size=101,
        ),
        SimpleNamespace(
            artifact_type="heart_rate_model",
            object_key="heart-rate/v1/lstm_model.keras",
            checksum_sha256="b" * 64,
            byte_size=202,
        ),
        SimpleNamespace(
            artifact_type="heart_rate_label_encoder",
            object_key="heart-rate/v1/label_encoder.pkl",
            checksum_sha256="c" * 64,
        ),
        SimpleNamespace(
            artifact_type="music_scaler",
            object_key="music/v1/scaler.pkl",
            checksum_sha256="d" * 64,
        ),
    ]

    class AssetCache:
        def __init__(self):
            self.requested = []

        def get_model_asset(
            self,
            requested_client,
            object_key,
            checksum,
            expected_size=None,
        ):
            self.requested.append(
                (requested_client, object_key, checksum, expected_size)
            )
            path = tmp_path / Path(object_key).name
            path.write_text(object_key, encoding="utf-8")
            return path

    cache = AssetCache()

    result = provision_models(manifest, cache, asset_client=client)

    assert set(result.provisioned) == {
        "fer_model",
        "hr_model",
    }
    assert [request[1] for request in cache.requested] == [
        "fer/v1/myrhythm_fer.h5",
        "heart-rate/v1/lstm_model.keras",
    ]
    assert all(request[0] is client for request in cache.requested)
    assert [request[3] for request in cache.requested] == [101, 202]


def test_provision_models_reports_missing_required_manifest_entries(tmp_path):
    cache = FakeModelCache(tmp_path)

    result = provision_models([MODEL_MANIFEST[0]], cache)

    assert set(result.provisioned) == {"fer_model"}
    assert set(result.failures) == {"hr_model"}


def test_provision_models_normalizes_runtime_artifact_type_aliases(tmp_path):
    manifest = [
        {"artifact_type": "FER", "object_key": "fer/v1/myrhythm_fer.h5"},
        {"artifact_type": "hr", "object_key": "heart-rate/v1/lstm_model.keras"},
        {
            "artifact_type": "hr-label-encoder",
            "object_key": "heart-rate/v1/label_encoder.pkl",
        },
    ]
    cache = FakeModelCache(tmp_path)

    result = provision_models(manifest, cache)

    assert set(result.provisioned) == {
        "fer_model",
        "hr_model",
    }

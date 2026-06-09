from pathlib import Path

from app.config.runtime_assets import (
    PROJECT_ROOT,
    RuntimeAssets,
    resolve_cover_path,
    resolve_runtime_assets,
)


def test_resolve_runtime_assets_uses_environment_paths(monkeypatch, tmp_path):
    fer_model = tmp_path / "fer.h5"
    hr_model = tmp_path / "hr.keras"
    manifest = tmp_path / "songs.csv"
    music_dir = tmp_path / "music"

    for path in [fer_model, hr_model, manifest]:
        path.write_text("local artifact", encoding="utf-8")
    music_dir.mkdir()

    monkeypatch.setenv("MYRHYTHM_FER_MODEL_PATH", str(fer_model))
    monkeypatch.setenv("MYRHYTHM_HR_MODEL_PATH", str(hr_model))
    monkeypatch.setenv("MYRHYTHM_SONG_MANIFEST", str(manifest))
    monkeypatch.setenv("MYRHYTHM_MUSIC_DIR", str(music_dir))

    assets = resolve_runtime_assets()

    assert isinstance(assets, RuntimeAssets)
    assert assets.fer_model.path == fer_model
    assert assets.fer_model.exists is True
    assert assets.hr_model.path == hr_model
    assert assets.hr_model.exists is True
    assert not hasattr(assets, "hr_label_encoder")
    assert assets.song_manifest.path == manifest
    assert assets.song_manifest.exists is True
    assert assets.music_dir.path == music_dir
    assert assets.music_dir.exists is True


def test_resolve_runtime_assets_uses_default_paths_when_env_is_empty():
    assets = resolve_runtime_assets(env={})

    assert assets.fer_model.path.name == "myrhythm_fer.h5"
    assert assets.hr_model.path.name == "lstm_model.keras"
    assert assets.fer_model.source == "default"
    assert assets.hr_model.source == "default"


def test_resolve_runtime_assets_resolves_relative_env_paths_under_project_root():
    assets = resolve_runtime_assets(
        env={
            "MYRHYTHM_FER_MODEL_PATH": "local_models/fer.h5",
            "MYRHYTHM_HR_MODEL_PATH": "local_models/hr.keras",
            "MYRHYTHM_SONG_MANIFEST": "sample_data/songs.csv",
            "MYRHYTHM_MUSIC_DIR": "tracks/local",
        }
    )

    assert assets.fer_model.path == PROJECT_ROOT / "local_models" / "fer.h5"
    assert assets.hr_model.path == PROJECT_ROOT / "local_models" / "hr.keras"
    assert assets.song_manifest.path == PROJECT_ROOT / "sample_data" / "songs.csv"
    assert assets.music_dir.path == PROJECT_ROOT / "tracks" / "local"


def test_resolve_runtime_assets_prefers_provisioned_overrides(tmp_path):
    provisioned_fer = tmp_path / "cached-fer.h5"
    provisioned_fer.write_text("model", encoding="utf-8")

    assets = resolve_runtime_assets(
        env={"MYRHYTHM_FER_MODEL_PATH": "local_models/fer.h5"},
        overrides={"MYRHYTHM_FER_MODEL_PATH": provisioned_fer},
    )

    assert assets.fer_model.path == provisioned_fer
    assert assets.fer_model.exists is True
    assert assets.fer_model.source == "runtime_override"


def test_resolve_cover_path_resolves_relative_default_cover_under_project_root(
    monkeypatch,
    tmp_path,
):
    monkeypatch.chdir(tmp_path)

    resolved = resolve_cover_path(None, "media/default_cover.png")

    assert resolved == PROJECT_ROOT / "media" / "default_cover.png"


def test_resolve_cover_path_returns_default_cover_for_missing_file(tmp_path):
    default_cover = tmp_path / "default_cover.png"
    default_cover.write_bytes(b"png")

    resolved = resolve_cover_path(tmp_path / "missing.png", default_cover)

    assert resolved == default_cover


def test_resolve_cover_path_keeps_existing_cover(tmp_path):
    default_cover = tmp_path / "default_cover.png"
    cover = tmp_path / "cover.png"
    default_cover.write_bytes(b"default")
    cover.write_bytes(b"cover")

    resolved = resolve_cover_path(cover, default_cover)

    assert resolved == cover

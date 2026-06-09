from pathlib import Path

import pytest


def test_fer_model_reports_missing_model_before_loading_keras(tmp_path):
    from app.fer.scripts.fer_inference import FERModel

    missing_model = tmp_path / "missing_fer.h5"

    with pytest.raises(FileNotFoundError, match="FER model missing"):
        FERModel(model_path=missing_model)


def test_fer_model_uses_runtime_asset_path_when_no_path_is_provided(monkeypatch, tmp_path):
    from app.fer.scripts.fer_inference import FERModel

    missing_model = tmp_path / "missing_from_env.h5"
    monkeypatch.setenv("MYRHYTHM_FER_MODEL_PATH", str(missing_model))

    with pytest.raises(FileNotFoundError) as exc_info:
        FERModel()

    assert str(Path(missing_model)) in str(exc_info.value)


def test_fer_loader_thread_emits_missing_model_status(monkeypatch):
    pytest.importorskip("PyQt5")
    from app.fer.scripts import model_loader

    class MissingFERModel:
        def __init__(self):
            raise FileNotFoundError("missing fer model")

    monkeypatch.setattr(model_loader, "FERModel", MissingFERModel)
    thread = model_loader.FERLoaderThread()
    statuses = []
    errors = []
    thread.status.connect(statuses.append)
    thread.error.connect(errors.append)

    thread.run()

    assert statuses == ["Loading model", "Model missing"]
    assert errors == ["missing fer model"]


def test_fer_loader_thread_emits_loaded_model(monkeypatch):
    pytest.importorskip("PyQt5")
    from app.fer.scripts import model_loader

    model = object()

    class FakeFERModel:
        def __new__(cls):
            return model

    monkeypatch.setattr(model_loader, "FERModel", FakeFERModel)
    thread = model_loader.FERLoaderThread()
    statuses = []
    loaded = []
    thread.status.connect(statuses.append)
    thread.loaded.connect(loaded.append)

    thread.run()

    assert statuses == ["Loading model"]
    assert loaded == [model]

import importlib
import sys

from app.hr.trained_hr_models import classifier


def test_pipeline_import_does_not_load_hr_model(monkeypatch):
    def fail_if_called():
        raise RuntimeError("model load should be lazy")

    monkeypatch.setattr(classifier, "load_model_components", fail_if_called)
    sys.modules.pop("app.hr.scripts.pipeline", None)

    pipeline = importlib.import_module("app.hr.scripts.pipeline")

    assert callable(pipeline.predict_emotions_live)

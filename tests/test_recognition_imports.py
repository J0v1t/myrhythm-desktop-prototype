import importlib
import sys


def test_recognition_import_does_not_import_hr_pipeline():
    sys.modules.pop("app.gui.recognition", None)
    sys.modules.pop("app.hr.scripts.pipeline", None)

    importlib.import_module("app.gui.recognition")

    assert "app.hr.scripts.pipeline" not in sys.modules

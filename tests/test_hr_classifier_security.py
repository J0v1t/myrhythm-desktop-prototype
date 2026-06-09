from pathlib import Path
import subprocess
import sys

from app.hr.trained_hr_models import classifier


def test_hr_classifier_decodes_with_fixed_safe_label_order():
    assert classifier.decode_emotion_index(0) == "High Va"
    assert classifier.decode_emotion_index(1) == "High V Low A"
    assert classifier.decode_emotion_index(2) == "Low Va"
    assert classifier.decode_emotion_index(3) == "Low V High A"


def test_hr_classifier_does_not_deserialize_joblib_artifact():
    source = Path(classifier.__file__).read_text(encoding="utf-8")

    assert "joblib.load" not in source
    assert "label_encoder.pkl" not in source


def test_hr_runtime_import_does_not_load_training_dependencies():
    command = (
        "import sys; import app.hr.scripts.pipeline; "
        "print(','.join(name for name in "
        "['pandas','sklearn','imblearn','joblib'] if name in sys.modules))"
    )

    result = subprocess.run(
        [sys.executable, "-c", command],
        check=True,
        capture_output=True,
        text=True,
    )

    assert result.stdout.strip() == ""

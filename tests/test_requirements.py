from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _requirements(filename: str) -> set[str]:
    return {
        line.strip().split("==", 1)[0].lower()
        for line in (ROOT / filename).read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith(("#", "-r "))
    }


def test_reviewer_requirements_exclude_legacy_sqlite_tooling():
    reviewer = _requirements("requirements.txt")

    assert reviewer == {
        "bleak",
        "keras",
        "numpy",
        "opencv-python",
        "pyqt5",
        "python-vlc",
        "tensorflow",
    }


def test_offline_requirements_include_reviewer_runtime_and_tooling():
    offline_text = (ROOT / "requirements-offline.txt").read_text(encoding="utf-8")
    offline = _requirements("requirements-offline.txt")

    assert "-r requirements.txt" in offline_text
    assert offline == {"sqlalchemy", "werkzeug"}

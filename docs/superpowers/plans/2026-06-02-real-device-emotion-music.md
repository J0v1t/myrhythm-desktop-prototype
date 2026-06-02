# Real-Device Emotion And Music Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make MyRhythm's local PyQt desktop app use real webcam FER and BLE heart-rate hardware through testable seams, then pass summary mood labels into recommendations and dashboard playback.

**Architecture:** Introduce small, deep modules for runtime artifact paths, emotion signal state, and song catalog normalization. Keep FER, HR, recommendation, and dashboard behavior local-first today, while preserving later Supabase/Postgres metadata and Cloudflare R2 signed-object adapters.

**Tech Stack:** Python 3, PyQt5, OpenCV, TensorFlow/Keras, bleak, SQLAlchemy/SQLite, python-vlc, pytest.

---

## File Structure

- Create `app/config/__init__.py`: package marker for config helpers.
- Create `app/config/runtime_assets.py`: resolves local model, song, and cover paths from environment variables with safe defaults.
- Create `tests/test_runtime_assets.py`: tests runtime path resolution and cover fallback.
- Create `app/emotion/__init__.py`: package exports for emotion signal modules.
- Create `app/emotion/signal_session.py`: owns FER/HR summary state, fused mood, and recommendation input creation.
- Create `tests/test_emotion_signal_session.py`: tests emotion state transitions without hardware.
- Modify `app/fer/scripts/fer_inference.py`: use configured FER model path and report missing model as a Python exception.
- Modify `app/fer/scripts/model_loader.py`: emit model-loading status and error signals for the Recognition window.
- Modify `app/hr/trained_hr_models/classifier.py`: resolve HR model and label encoder through runtime assets.
- Modify `app/hr/scripts/ble_reader.py`: expose public `parse_hr_measurement` while preserving the existing private call.
- Create `tests/test_heart_rate_adapter.py`: tests HR BLE byte parsing and missing artifact status.
- Create `app/music/catalog.py`: normalizes SQLite/local song records and cover fallback for dashboard/recommendation display.
- Create `tests/test_song_catalog.py`: tests cover fallback and manifest record normalization.
- Modify `app/music/recommendation/recommendation_engine.py`: include fused mood and recommendation reason in returned entries.
- Create `tests/test_recommendation_engine.py`: tests recommendation reasons and cover fallback without real audio.
- Modify `app/gui/recognition.py`: bind UI labels/statuses to Emotion Signal Session and model/HR status signals.
- Modify `app/gui/dashboard2.py`: use catalog-normalized song records and show recommendation reason.
- Modify `.env.example`: document FER/HR model path variables.
- Modify `docs/local-assets.md`: document real-device local setup.
- Modify `docs/model-artifacts.md`: document configured model path behavior.
- Modify `README.md`: document real-device local run path and skipped optional tests.

## Task 1: Runtime Asset Path Module

**Files:**
- Create: `app/config/__init__.py`
- Create: `app/config/runtime_assets.py`
- Test: `tests/test_runtime_assets.py`

- [ ] **Step 1: Write the failing tests**

Create `tests/test_runtime_assets.py`:

```python
from pathlib import Path

from app.config.runtime_assets import (
    RuntimeAssets,
    resolve_cover_path,
    resolve_runtime_assets,
)


def test_resolve_runtime_assets_uses_environment_paths(monkeypatch, tmp_path):
    fer_model = tmp_path / "fer.h5"
    hr_model = tmp_path / "hr.keras"
    hr_encoder = tmp_path / "labels.pkl"
    manifest = tmp_path / "songs.csv"
    music_dir = tmp_path / "music"

    for path in [fer_model, hr_model, hr_encoder, manifest]:
        path.write_text("local artifact", encoding="utf-8")
    music_dir.mkdir()

    monkeypatch.setenv("MYRHYTHM_FER_MODEL_PATH", str(fer_model))
    monkeypatch.setenv("MYRHYTHM_HR_MODEL_PATH", str(hr_model))
    monkeypatch.setenv("MYRHYTHM_HR_LABEL_ENCODER_PATH", str(hr_encoder))
    monkeypatch.setenv("MYRHYTHM_SONG_MANIFEST", str(manifest))
    monkeypatch.setenv("MYRHYTHM_MUSIC_DIR", str(music_dir))

    assets = resolve_runtime_assets()

    assert isinstance(assets, RuntimeAssets)
    assert assets.fer_model.path == fer_model
    assert assets.fer_model.exists is True
    assert assets.hr_model.path == hr_model
    assert assets.hr_model.exists is True
    assert assets.hr_label_encoder.path == hr_encoder
    assert assets.hr_label_encoder.exists is True
    assert assets.song_manifest.path == manifest
    assert assets.song_manifest.exists is True
    assert assets.music_dir.path == music_dir
    assert assets.music_dir.exists is True


def test_resolve_runtime_assets_uses_default_paths_when_env_is_empty():
    assets = resolve_runtime_assets(env={})

    assert assets.fer_model.path.name == "myrhythm_fer.h5"
    assert assets.hr_model.path.name == "lstm_model.keras"
    assert assets.hr_label_encoder.path.name == "label_encoder.pkl"
    assert assets.fer_model.source == "default"
    assert assets.hr_model.source == "default"
    assert assets.hr_label_encoder.source == "default"


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
```

- [ ] **Step 2: Run tests to verify they fail**

Run:

```powershell
python -m pytest tests/test_runtime_assets.py -v
```

Expected: FAIL during import because `app.config.runtime_assets` does not exist.

- [ ] **Step 3: Implement runtime asset resolution**

Create `app/config/__init__.py`:

```python
"""Runtime configuration helpers for MyRhythm."""
```

Create `app/config/runtime_assets.py`:

```python
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping, Optional, Union
import os


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_FER_MODEL = PROJECT_ROOT / "app" / "fer" / "trained_models" / "myrhythm_fer.h5"
DEFAULT_HR_MODEL = PROJECT_ROOT / "app" / "hr" / "trained_hr_models" / "lstm_model.keras"
DEFAULT_HR_LABEL_ENCODER = PROJECT_ROOT / "app" / "hr" / "trained_hr_models" / "label_encoder.pkl"
DEFAULT_SONG_MANIFEST = PROJECT_ROOT / "sample_data" / "song_manifest.example.csv"
DEFAULT_MUSIC_DIR = PROJECT_ROOT / "tracks"
DEFAULT_COVER = PROJECT_ROOT / "media" / "default_cover.png"


@dataclass(frozen=True)
class ResolvedPath:
    path: Path
    exists: bool
    source: str


@dataclass(frozen=True)
class RuntimeAssets:
    fer_model: ResolvedPath
    hr_model: ResolvedPath
    hr_label_encoder: ResolvedPath
    song_manifest: ResolvedPath
    music_dir: ResolvedPath
    default_cover: Path


def _path_from_env(
    env_name: str,
    default_path: Path,
    env: Mapping[str, str],
) -> ResolvedPath:
    raw_value = env.get(env_name)
    source = env_name if raw_value else "default"
    candidate = Path(raw_value) if raw_value else default_path
    if not candidate.is_absolute():
        candidate = PROJECT_ROOT / candidate
    candidate = candidate.resolve()
    return ResolvedPath(path=candidate, exists=candidate.exists(), source=source)


def resolve_runtime_assets(env: Optional[Mapping[str, str]] = None) -> RuntimeAssets:
    active_env = os.environ if env is None else env
    return RuntimeAssets(
        fer_model=_path_from_env("MYRHYTHM_FER_MODEL_PATH", DEFAULT_FER_MODEL, active_env),
        hr_model=_path_from_env("MYRHYTHM_HR_MODEL_PATH", DEFAULT_HR_MODEL, active_env),
        hr_label_encoder=_path_from_env(
            "MYRHYTHM_HR_LABEL_ENCODER_PATH",
            DEFAULT_HR_LABEL_ENCODER,
            active_env,
        ),
        song_manifest=_path_from_env("MYRHYTHM_SONG_MANIFEST", DEFAULT_SONG_MANIFEST, active_env),
        music_dir=_path_from_env("MYRHYTHM_MUSIC_DIR", DEFAULT_MUSIC_DIR, active_env),
        default_cover=DEFAULT_COVER,
    )


def resolve_cover_path(
    cover_path: Optional[Union[str, Path]],
    default_cover: Union[str, Path] = DEFAULT_COVER,
) -> Path:
    fallback = Path(default_cover).resolve()
    if not cover_path:
        return fallback

    candidate = Path(cover_path)
    if not candidate.is_absolute():
        candidate = (PROJECT_ROOT / candidate).resolve()
    else:
        candidate = candidate.resolve()

    return candidate if candidate.exists() else fallback
```

- [ ] **Step 4: Run tests to verify they pass**

Run:

```powershell
python -m pytest tests/test_runtime_assets.py -v
```

Expected: 4 tests PASS.

- [ ] **Step 5: Commit**

Run:

```powershell
git add app/config/__init__.py app/config/runtime_assets.py tests/test_runtime_assets.py
git commit -m "Add runtime asset path resolution"
```

## Task 2: Emotion Signal Session Module

**Files:**
- Create: `app/emotion/__init__.py`
- Create: `app/emotion/signal_session.py`
- Test: `tests/test_emotion_signal_session.py`

- [ ] **Step 1: Write the failing tests**

Create `tests/test_emotion_signal_session.py`:

```python
from app.emotion.signal_session import EmotionSignalSession


def test_initial_session_state_is_off_and_neutral():
    session = EmotionSignalSession()

    assert session.state.fer_status == "Off"
    assert session.state.hr_status == "Off"
    assert session.state.fused_mood == "neutral"
    assert session.recommendation_inputs() == {
        "fer_emotion": None,
        "hr_emotion": None,
        "combined_mode": False,
        "fused_mood": "neutral",
    }


def test_fer_update_normalizes_label_and_fuses_mood():
    session = EmotionSignalSession()

    session.update_fer(status="Camera active", label="Joy", confidence=0.91)

    assert session.state.fer_status == "Camera active"
    assert session.state.fer_label == "happy"
    assert session.state.fer_confidence == 0.91
    assert session.state.fused_mood == "happy"


def test_hr_update_tracks_bpm_and_label():
    session = EmotionSignalSession()

    session.update_hr(status="Connected", bpm=82, label="Calm")

    assert session.state.hr_status == "Connected"
    assert session.state.bpm == 82
    assert session.state.hr_label == "neutral"
    assert session.state.fused_mood == "neutral"


def test_combined_inputs_mark_combined_mode_when_both_signals_exist():
    session = EmotionSignalSession()

    session.update_fer(status="Camera active", label="happy", confidence=0.8)
    session.update_hr(status="Connected", bpm=126, label="angry")

    assert session.state.fused_mood == "angry"
    assert session.recommendation_inputs() == {
        "fer_emotion": "happy",
        "hr_emotion": "angry",
        "combined_mode": True,
        "fused_mood": "angry",
    }


def test_reset_signal_clears_labels_without_changing_other_signal():
    session = EmotionSignalSession()
    session.update_fer(status="Camera active", label="sad", confidence=0.75)
    session.update_hr(status="Connected", bpm=74, label="neutral")

    session.reset_fer(status="Off")

    assert session.state.fer_status == "Off"
    assert session.state.fer_label is None
    assert session.state.hr_label == "neutral"
    assert session.state.fused_mood == "neutral"
```

- [ ] **Step 2: Run tests to verify they fail**

Run:

```powershell
python -m pytest tests/test_emotion_signal_session.py -v
```

Expected: FAIL during import because `app.emotion.signal_session` does not exist.

- [ ] **Step 3: Implement signal session**

Create `app/emotion/__init__.py`:

```python
from app.emotion.signal_session import EmotionSignalSession, EmotionSignalState

__all__ = ["EmotionSignalSession", "EmotionSignalState"]
```

Create `app/emotion/signal_session.py`:

```python
from dataclasses import dataclass, replace
from typing import Optional

from app.music.mood.mood_router import fuse_emotions, normalize_emotion


VALID_STATUSES = {
    "Off",
    "Loading model",
    "Camera active",
    "No webcam detected",
    "Model missing",
    "Scanning BLE",
    "Connected",
    "Device not found",
    "Error",
}


@dataclass(frozen=True)
class EmotionSignalState:
    fer_status: str = "Off"
    hr_status: str = "Off"
    fer_label: Optional[str] = None
    fer_confidence: Optional[float] = None
    bpm: Optional[int] = None
    hr_label: Optional[str] = None
    fused_mood: str = "neutral"


class EmotionSignalSession:
    def __init__(self) -> None:
        self.state = EmotionSignalState()

    def update_fer(
        self,
        status: Optional[str] = None,
        label: Optional[str] = None,
        confidence: Optional[float] = None,
    ) -> EmotionSignalState:
        normalized_label = normalize_emotion(label) if label else self.state.fer_label
        next_state = replace(
            self.state,
            fer_status=self._status_or_current(status, self.state.fer_status),
            fer_label=normalized_label,
            fer_confidence=confidence if confidence is not None else self.state.fer_confidence,
        )
        self.state = self._with_fused_mood(next_state)
        return self.state

    def update_hr(
        self,
        status: Optional[str] = None,
        bpm: Optional[int] = None,
        label: Optional[str] = None,
    ) -> EmotionSignalState:
        normalized_label = normalize_emotion(label) if label else self.state.hr_label
        next_state = replace(
            self.state,
            hr_status=self._status_or_current(status, self.state.hr_status),
            bpm=bpm if bpm is not None else self.state.bpm,
            hr_label=normalized_label,
        )
        self.state = self._with_fused_mood(next_state)
        return self.state

    def reset_fer(self, status: str = "Off") -> EmotionSignalState:
        next_state = replace(
            self.state,
            fer_status=self._status_or_current(status, self.state.fer_status),
            fer_label=None,
            fer_confidence=None,
        )
        self.state = self._with_fused_mood(next_state)
        return self.state

    def reset_hr(self, status: str = "Off") -> EmotionSignalState:
        next_state = replace(
            self.state,
            hr_status=self._status_or_current(status, self.state.hr_status),
            bpm=None,
            hr_label=None,
        )
        self.state = self._with_fused_mood(next_state)
        return self.state

    def recommendation_inputs(self) -> dict:
        return {
            "fer_emotion": self.state.fer_label,
            "hr_emotion": self.state.hr_label,
            "combined_mode": bool(self.state.fer_label and self.state.hr_label),
            "fused_mood": self.state.fused_mood,
        }

    def _with_fused_mood(self, state: EmotionSignalState) -> EmotionSignalState:
        fused = fuse_emotions(state.fer_label, state.hr_label) or "neutral"
        normalized = normalize_emotion(fused) or "neutral"
        return replace(state, fused_mood=normalized)

    def _status_or_current(self, status: Optional[str], current: str) -> str:
        if status is None:
            return current
        if status not in VALID_STATUSES:
            return "Error"
        return status
```

- [ ] **Step 4: Run tests to verify they pass**

Run:

```powershell
python -m pytest tests/test_emotion_signal_session.py -v
```

Expected: 5 tests PASS.

- [ ] **Step 5: Commit**

Run:

```powershell
git add app/emotion/__init__.py app/emotion/signal_session.py tests/test_emotion_signal_session.py
git commit -m "Add emotion signal session state"
```

## Task 3: Model Artifact Status And Heart-Rate Parsing

**Files:**
- Modify: `app/fer/scripts/fer_inference.py`
- Modify: `app/fer/scripts/model_loader.py`
- Modify: `app/hr/trained_hr_models/classifier.py`
- Modify: `app/hr/scripts/ble_reader.py`
- Test: `tests/test_heart_rate_adapter.py`

- [ ] **Step 1: Write failing tests for public HR parser and artifact paths**

Create `tests/test_heart_rate_adapter.py`:

```python
from app.hr.scripts.ble_reader import parse_hr_measurement
from app.hr.trained_hr_models.classifier import get_model_artifact_status


def test_parse_hr_measurement_reads_uint8_payload():
    assert parse_hr_measurement(bytearray([0x00, 72])) == 72


def test_parse_hr_measurement_reads_uint16_payload():
    assert parse_hr_measurement(bytearray([0x01, 0x2C, 0x01])) == 300


def test_parse_hr_measurement_returns_none_for_empty_payload():
    assert parse_hr_measurement(bytearray()) is None


def test_hr_model_artifact_status_uses_runtime_assets(monkeypatch, tmp_path):
    model = tmp_path / "lstm_model.keras"
    encoder = tmp_path / "label_encoder.pkl"
    model.write_text("model", encoding="utf-8")
    encoder.write_text("encoder", encoding="utf-8")
    monkeypatch.setenv("MYRHYTHM_HR_MODEL_PATH", str(model))
    monkeypatch.setenv("MYRHYTHM_HR_LABEL_ENCODER_PATH", str(encoder))

    status = get_model_artifact_status()

    assert status["model_path"] == str(model)
    assert status["label_encoder_path"] == str(encoder)
    assert status["ready"] is True
```

- [ ] **Step 2: Run tests to verify they fail**

Run:

```powershell
python -m pytest tests/test_heart_rate_adapter.py -v
```

Expected: FAIL because `parse_hr_measurement` and `get_model_artifact_status` are not public.

- [ ] **Step 3: Expose heart-rate parser**

In `app/hr/scripts/ble_reader.py`, rename `_parse_hr_measurement` to `parse_hr_measurement`, then keep this compatibility alias below it:

```python
def _parse_hr_measurement(data: bytearray) -> Optional[int]:
    return parse_hr_measurement(data)
```

Update the notification handler in `read_heart_rate_live`:

```python
bpm = parse_hr_measurement(data)
```

The public parser body should be:

```python
def parse_hr_measurement(data: bytearray) -> Optional[int]:
    """Parses the Heart Rate Measurement characteristic data."""
    if not data:
        return None

    flags = data[0]
    hr_format = flags & 0x01

    if hr_format == 0:
        return data[1] if len(data) > 1 else None

    if len(data) > 2:
        return (data[2] << 8) | data[1]
    return None
```

- [ ] **Step 4: Add HR artifact status, lazy ML imports, and path-aware loading**

In `app/hr/trained_hr_models/classifier.py`, keep only lightweight imports at module import time:

```python
from typing import Optional, Any
import os
import numpy as np

from app.config.runtime_assets import resolve_runtime_assets
```

Remove these top-level imports:

```python
import joblib
import tensorflow as tf
from tensorflow.keras.optimizers import Adam
```

Change the cached model annotation to avoid importing TensorFlow for type checking:

```python
_lstm_model: Optional[Any] = None
_label_encoder: Optional[Any] = None
```

Add this function near the path constants:

```python
def get_model_artifact_status() -> dict:
    assets = resolve_runtime_assets()
    return {
        "model_path": str(assets.hr_model.path),
        "label_encoder_path": str(assets.hr_label_encoder.path),
        "model_exists": assets.hr_model.exists,
        "label_encoder_exists": assets.hr_label_encoder.exists,
        "ready": assets.hr_model.exists and assets.hr_label_encoder.exists,
    }
```

Change `load_model_components` to resolve active paths before checking existence:

```python
def load_model_components() -> bool:
    global _lstm_model, _label_encoder

    if _lstm_model and _label_encoder:
        return True

    status = get_model_artifact_status()
    model_path = status["model_path"]
    label_encoder_path = status["label_encoder_path"]

    if not status["ready"]:
        print("\nFATAL ERROR: Model files not found.")
        print(f"  Missing: {model_path} or {label_encoder_path}")
        return False

    try:
        import joblib
        import tensorflow as tf
        from tensorflow.keras.optimizers import Adam

        _lstm_model = tf.keras.models.load_model(model_path, compile=False)
        num_classes = _lstm_model.output_shape[-1]
        _lstm_model.compile(
            optimizer=Adam(learning_rate=0.001),
            loss="sparse_categorical_crossentropy",
            metrics=["accuracy"],
        )
        _label_encoder = joblib.load(label_encoder_path)
        print(f"HR LSTM model loaded from {model_path}")
        return True
    except Exception as e:
        print(f"\nFATAL ERROR: Could not load HR model artifacts: {e}")
        return False
```

- [ ] **Step 5: Add FER model path behavior**

In `app/fer/scripts/fer_inference.py`, import runtime assets:

```python
from app.config.runtime_assets import resolve_runtime_assets
```

Change the constructor start to:

```python
def __init__(self, model_path=None, class_labels=None):
    self.target_size = (48, 48)
    self.class_labels = class_labels if class_labels else ["angry", "happy", "neutral", "sad"]

    active_model_path = model_path or str(resolve_runtime_assets().fer_model.path)
    if not os.path.exists(active_model_path):
        raise FileNotFoundError(f"FER model missing: {active_model_path}")

    print("Loading FER model...")
    self.model = load_model(active_model_path)
    print("FER model loaded successfully.")
```

In `app/fer/scripts/model_loader.py`, replace the class with:

```python
from PyQt5.QtCore import QThread, pyqtSignal
from .fer_inference import FERModel


class FERLoaderThread(QThread):
    loaded = pyqtSignal(object)
    status = pyqtSignal(str)
    error = pyqtSignal(str)

    def run(self):
        try:
            self.status.emit("Loading model")
            model = FERModel()
            self.loaded.emit(model)
        except FileNotFoundError:
            self.error.emit("Model missing")
        except Exception:
            self.error.emit("Error")
```

- [ ] **Step 6: Run focused tests**

Run:

```powershell
python -m pytest tests/test_runtime_assets.py tests/test_heart_rate_adapter.py -v
```

Expected: all focused tests PASS.

- [ ] **Step 7: Commit**

Run:

```powershell
git add app/fer/scripts/fer_inference.py app/fer/scripts/model_loader.py app/hr/trained_hr_models/classifier.py app/hr/scripts/ble_reader.py tests/test_heart_rate_adapter.py
git commit -m "Add real-device artifact status hooks"
```

## Task 4: Song Catalog Normalization

**Files:**
- Create: `app/music/catalog.py`
- Test: `tests/test_song_catalog.py`

- [ ] **Step 1: Write the failing tests**

Create `tests/test_song_catalog.py`:

```python
from types import SimpleNamespace

from app.music.catalog import SongCatalogRecord, normalize_song_record


def test_normalize_song_record_uses_default_cover_for_missing_cover(tmp_path):
    default_cover = tmp_path / "default_cover.png"
    default_cover.write_bytes(b"default")
    song = SimpleNamespace(
        id=7,
        title="Track A",
        artist="Artist A",
        genre="Pop",
        duration=180,
        file_path=str(tmp_path / "track.mp3"),
        cover_path=str(tmp_path / "missing.png"),
    )

    record = normalize_song_record(song, default_cover=default_cover)

    assert isinstance(record, SongCatalogRecord)
    assert record.id == 7
    assert record.title == "Track A"
    assert record.artist == "Artist A"
    assert record.genre == "Pop"
    assert record.duration == 180
    assert record.file_path.endswith("track.mp3")
    assert record.cover_path == str(default_cover)


def test_normalize_song_record_fills_unknown_text_fields(tmp_path):
    default_cover = tmp_path / "default_cover.png"
    default_cover.write_bytes(b"default")
    song = SimpleNamespace(id=None, title=None, artist=None, genre=None, duration=None, file_path="", cover_path=None)

    record = normalize_song_record(song, default_cover=default_cover)

    assert record.title == "Unknown Title"
    assert record.artist == "Unknown Artist"
    assert record.genre == "Unknown Genre"
    assert record.duration is None
    assert record.cover_path == str(default_cover)


def test_catalog_record_can_be_converted_for_legacy_dashboard(tmp_path):
    default_cover = tmp_path / "default_cover.png"
    default_cover.write_bytes(b"default")
    record = SongCatalogRecord(
        id=1,
        title="Track B",
        artist="Artist B",
        genre="Rock",
        duration=210,
        file_path="C:/music/track-b.mp3",
        cover_path=str(default_cover),
        license_status="verified-local",
        source_notes="local test",
    )

    legacy = record.to_simple_namespace()

    assert legacy.id == 1
    assert legacy.title == "Track B"
    assert legacy.artist == "Artist B"
    assert legacy.file_path == "C:/music/track-b.mp3"
    assert legacy.cover_path == str(default_cover)
```

- [ ] **Step 2: Run tests to verify they fail**

Run:

```powershell
python -m pytest tests/test_song_catalog.py -v
```

Expected: FAIL because `app.music.catalog` does not exist.

- [ ] **Step 3: Implement catalog normalization**

Create `app/music/catalog.py`:

```python
from dataclasses import dataclass
from pathlib import Path
from types import SimpleNamespace
from typing import Optional

from app.config.runtime_assets import DEFAULT_COVER, resolve_cover_path


@dataclass(frozen=True)
class SongCatalogRecord:
    id: Optional[int]
    title: str
    artist: str
    genre: str
    duration: Optional[float]
    file_path: str
    cover_path: str
    license_status: str = "local"
    source_notes: str = ""
    recommendation_reason: str = ""

    def to_simple_namespace(self) -> SimpleNamespace:
        return SimpleNamespace(
            id=self.id,
            title=self.title,
            artist=self.artist,
            genre=self.genre,
            duration=self.duration,
            file_path=self.file_path,
            cover_path=self.cover_path,
            recommendation_reason=self.recommendation_reason,
        )


def normalize_song_record(song, default_cover: Path = DEFAULT_COVER) -> SongCatalogRecord:
    cover = resolve_cover_path(getattr(song, "cover_path", None), default_cover)
    return SongCatalogRecord(
        id=getattr(song, "id", None),
        title=getattr(song, "title", None) or "Unknown Title",
        artist=getattr(song, "artist", None) or "Unknown Artist",
        genre=getattr(song, "genre", None) or "Unknown Genre",
        duration=getattr(song, "duration", None),
        file_path=getattr(song, "file_path", None) or "",
        cover_path=str(cover),
        license_status=getattr(song, "license_status", "local") or "local",
        source_notes=getattr(song, "source_notes", "") or "",
        recommendation_reason=getattr(song, "recommendation_reason", "") or "",
    )
```

- [ ] **Step 4: Run tests to verify they pass**

Run:

```powershell
python -m pytest tests/test_song_catalog.py -v
```

Expected: 3 tests PASS.

- [ ] **Step 5: Commit**

Run:

```powershell
git add app/music/catalog.py tests/test_song_catalog.py
git commit -m "Add song catalog normalization"
```

## Task 5: Recommendation Reasons And Catalog Fallback

**Files:**
- Modify: `app/music/recommendation/recommendation_engine.py`
- Test: `tests/test_recommendation_engine.py`

- [ ] **Step 1: Write failing recommendation tests**

Create `tests/test_recommendation_engine.py`:

```python
from types import SimpleNamespace

from app.music.recommendation.recommendation_engine import RecommendationEngine


class FakeQuery:
    def __init__(self, rows):
        self.rows = rows

    def filter_by(self, **kwargs):
        self.kwargs = kwargs
        return self

    def first(self):
        return self.rows[0] if self.rows else None

    def limit(self, value):
        return self

    def all(self):
        return self.rows


class FakeDb:
    def __init__(self, songs, prefs):
        self.songs = songs
        self.prefs = prefs

    def query(self, model):
        if model.__name__ == "Song":
            return FakeQuery(self.songs)
        return FakeQuery(self.prefs)


def test_recommendation_includes_fused_mood_reason_and_default_cover(tmp_path):
    song = SimpleNamespace(
        id=1,
        title="Bright Local Track",
        artist="Local Artist",
        genre="pop",
        file_path="C:/music/bright.mp3",
        cover_path=None,
    )
    prefs = SimpleNamespace(favorite_genres="pop", favorite_artists="", mood_mapping="{}")
    engine = RecommendationEngine(db=FakeDb([song], [prefs]))

    results = engine.recommend(
        user_id=1,
        fer_emotion="happy",
        hr_emotion="neutral",
        combined_mode=True,
        top_k=1,
    )

    assert results[0]["title"] == "Bright Local Track"
    assert results[0]["fused_mood"] == "happy"
    assert results[0]["recommendation_reason"] == "Recommended for fused mood: Happy"
    assert results[0]["cover_path"].endswith("default_cover.png")
```

- [ ] **Step 2: Run test to verify it fails**

Run:

```powershell
python -m pytest tests/test_recommendation_engine.py -v
```

Expected: FAIL because returned recommendations do not include `fused_mood` and `recommendation_reason`.

- [ ] **Step 3: Update recommendation result shape**

In `app/music/recommendation/recommendation_engine.py`, import catalog fallback:

```python
from app.config.runtime_assets import DEFAULT_COVER, resolve_cover_path
```

Replace the existing `default_cover` assignment with:

```python
default_cover = DEFAULT_COVER
reason = f"Recommended for fused mood: {user_emotion.capitalize()}"
```

Inside the scored append block, set:

```python
"cover_path": str(resolve_cover_path(s.cover_path, default_cover)),
"fused_mood": user_emotion,
"recommendation_reason": reason,
```

The full append block should contain:

```python
scored.append({
    "song_id": s.id,
    "title": s.title,
    "artist": s.artist,
    "genre": s.genre,
    "file_path": s.file_path,
    "cover_path": str(resolve_cover_path(s.cover_path, default_cover)),
    "score": score,
    "breakdown": breakdown,
    "fused_mood": user_emotion,
    "recommendation_reason": reason,
})
```

- [ ] **Step 4: Run recommendation tests**

Run:

```powershell
python -m pytest tests/test_recommendation_engine.py -v
```

Expected: PASS.

- [ ] **Step 5: Run existing recommendation-adjacent tests**

Run:

```powershell
python -m pytest tests/test_song_catalog.py tests/test_recommendation_engine.py -v
```

Expected: all tests PASS.

- [ ] **Step 6: Commit**

Run:

```powershell
git add app/music/recommendation/recommendation_engine.py tests/test_recommendation_engine.py
git commit -m "Add recommendation reasons"
```

## Task 6: Recognition Window Wiring

**Files:**
- Modify: `app/gui/recognition.py`
- Test: `tests/test_emotion_signal_session.py`

- [ ] **Step 1: Add a regression test for recommendation input shape**

Append this test to `tests/test_emotion_signal_session.py`:

```python
def test_recommendation_inputs_ignore_unavailable_signals():
    session = EmotionSignalSession()

    session.update_fer(status="Model missing")
    session.update_hr(status="Device not found")

    assert session.recommendation_inputs() == {
        "fer_emotion": None,
        "hr_emotion": None,
        "combined_mode": False,
        "fused_mood": "neutral",
    }
```

- [ ] **Step 2: Run test to verify it passes before GUI wiring**

Run:

```powershell
python -m pytest tests/test_emotion_signal_session.py -v
```

Expected: all signal-session tests PASS. This guards the behavior the GUI will call.

- [ ] **Step 3: Import and initialize Emotion Signal Session**

In `app/gui/recognition.py`, add the import:

```python
from app.emotion.signal_session import EmotionSignalSession
```

In `Recognition.__init__`, after `self.current_hr_emotion = "neutral"`, add:

```python
self.signal_session = EmotionSignalSession()
self.last_hr_status = "Off"
```

- [ ] **Step 4: Add session-backed status helpers**

Add these methods to `Recognition`:

```python
def set_fer_status(self, status):
    state = self.signal_session.update_fer(status=status)
    self.label_3.setText(f"Fused mood: {state.fused_mood.capitalize()}")
    self.label_6.setText("" if status == "Camera active" else status)


def set_hr_status(self, status):
    self.last_hr_status = status
    state = self.signal_session.update_hr(status=status)
    self.label_16.setText(status)
    self.label_3.setText(f"Fused mood: {state.fused_mood.capitalize()}")
```

- [ ] **Step 5: Wire FER loader status and error**

In `start_camera`, replace:

```python
self.label_6.setText("Loading FER model... Please wait")
```

with:

```python
self.set_fer_status("Loading model")
```

After `self.loader.loaded.connect(self.on_model_loaded)`, add:

```python
self.loader.status.connect(self.set_fer_status)
self.loader.error.connect(self.on_fer_loader_error)
```

Add this method:

```python
def on_fer_loader_error(self, status):
    self.set_fer_status(status)
    if self.checkBox.isChecked():
        self.checkBox.blockSignals(True)
        self.checkBox.setChecked(False)
        self.checkBox.blockSignals(False)
        self.update_frame_border()
```

In `on_model_loaded`, after `self.fer_model = model`, add:

```python
self.set_fer_status("Camera active")
```

When camera is unavailable, replace `self.label_6.setText("No webcam detected")` with:

```python
self.set_fer_status("No webcam detected")
```

- [ ] **Step 6: Update FER emotion state in one place**

In `update_emotion`, after `self.current_emotion = smoothed`, add:

```python
self.signal_session.update_fer(status="Camera active", label=smoothed)
```

Replace:

```python
self.label_3.setText(f"Your current mood is: {smoothed.capitalize()}")
```

with:

```python
self.label_3.setText(f"Fused mood: {self.signal_session.state.fused_mood.capitalize()}")
```

In the camera-off branch of `toggle_camera`, after resetting `self.label_3`, add:

```python
self.signal_session.reset_fer("Off")
```

- [ ] **Step 7: Wire HR status through session**

In `start_hr_monitor`, replace `self.label_16.setText("Connecting...")` with:

```python
self.set_hr_status("Loading model")
```

In `update_hr_display`, after `self.label_15.setText(f"{raw_bpm}")`, replace `self.label_16.setText(f"{emotion}")` with:

```python
state = self.signal_session.update_hr(status="Connected", bpm=raw_bpm, label=emotion)
self.label_16.setText(f"{emotion}")
self.label_3.setText(f"Fused mood: {state.fused_mood.capitalize()}")
```

In `update_hr_status`, replace the first line with:

```python
self.set_hr_status(status_msg)
```

Then keep:

```python
if status_msg == "Device not found":
    self.label_15.setText("--")
```

Change the emitted string in `HeartRateWorker.async_main` from `"Device Not Found"` to `"Device not found"` to match the approved UI status list.

In `on_hr_worker_finished`, after `self.current_hr_emotion = "neutral"`, add:

```python
self.signal_session.reset_hr("Off")
if self.last_hr_status in {"Device not found", "Model missing", "Error"}:
    self.label_16.setText(self.last_hr_status)
```

In `HeartRateWorker.run`, replace the worker status strings with the approved UI statuses:

```python
self.status_update.emit("Loading model")
```

```python
self.status_update.emit("Scanning BLE")
```

```python
self.status_update.emit("Model missing")
```

Keep the existing `"Error"` status for unexpected exceptions.

- [ ] **Step 8: Use session recommendation inputs**

In `open_recommendations`, replace the `fer_active`, `hr_active`, `fer_emotion`, `hr_emotion`, and `combined` block with:

```python
inputs = self.signal_session.recommendation_inputs()
```

Then call:

```python
recommendations = engine.recommend(
    user_id=self.user_id,
    fer_emotion=inputs["fer_emotion"],
    hr_emotion=inputs["hr_emotion"],
    combined_mode=inputs["combined_mode"],
    top_k=10,
)
```

- [ ] **Step 9: Run focused non-GUI tests**

Run:

```powershell
python -m pytest tests/test_emotion_signal_session.py tests/test_heart_rate_adapter.py tests/test_recommendation_engine.py -v
```

Expected: all focused tests PASS.

- [ ] **Step 10: Run compile check**

Run:

```powershell
python -m compileall -q app tests
```

Expected: exit code 0.

- [ ] **Step 11: Commit**

Run:

```powershell
git add app/gui/recognition.py tests/test_emotion_signal_session.py
git commit -m "Wire recognition UI to signal session"
```

## Task 7: Dashboard Catalog And Recommendation Display

**Files:**
- Modify: `app/gui/dashboard2.py`
- Test: `tests/test_song_catalog.py`

- [ ] **Step 1: Add dashboard conversion test through catalog record**

Append this test to `tests/test_song_catalog.py`:

```python
def test_catalog_record_preserves_recommendation_reason_for_dashboard(tmp_path):
    default_cover = tmp_path / "default_cover.png"
    default_cover.write_bytes(b"default")
    record = SongCatalogRecord(
        id=2,
        title="Mood Track",
        artist="Mood Artist",
        genre="Pop",
        duration=120,
        file_path="C:/music/mood.mp3",
        cover_path=str(default_cover),
        recommendation_reason="Recommended for fused mood: Happy",
    )

    legacy = record.to_simple_namespace()

    assert legacy.recommendation_reason == "Recommended for fused mood: Happy"
```

- [ ] **Step 2: Run test to verify it passes before GUI wiring**

Run:

```powershell
python -m pytest tests/test_song_catalog.py -v
```

Expected: all catalog tests PASS.

- [ ] **Step 3: Import catalog helpers**

In `app/gui/dashboard2.py`, add:

```python
from app.music.catalog import SongCatalogRecord, normalize_song_record
```

- [ ] **Step 4: Normalize songs loaded from DB**

In `load_playlist_from_db`, replace:

```python
self.playlist = db.query(Song).all()
```

with:

```python
self.playlist = [
    normalize_song_record(song).to_simple_namespace()
    for song in db.query(Song).all()
]
```

- [ ] **Step 5: Preserve recommendation reason on converted recommendations**

In `load_recommended_songs`, add `recommendation_reason` to the `SimpleNamespace`:

```python
recommendation_reason=s.get("recommendation_reason", ""),
```

The full namespace should be:

```python
temp_song = SimpleNamespace(
    id=s.get("song_id"),
    title=s.get("title") or "Unknown Title",
    artist=s.get("artist") or "Unknown Artist",
    genre=s.get("genre") or "Unknown Genre",
    file_path=s.get("file_path") or "",
    cover_path=s.get("cover_path") or os.path.join(self.ui.media_path, "default_cover.png"),
    recommendation_reason=s.get("recommendation_reason", ""),
)
```

- [ ] **Step 6: Show recommendation reason in the player panel**

In `load_song`, after:

```python
self.ui.label_54.setText(song.artist or "Unknown Artist")
```

add:

```python
reason = getattr(song, "recommendation_reason", "")
if reason:
    self.ui.label_53.setText(reason)
else:
    self.ui.label_53.setText(song.title or "Unknown Title")
```

- [ ] **Step 7: Run catalog and recommendation tests**

Run:

```powershell
python -m pytest tests/test_song_catalog.py tests/test_recommendation_engine.py -v
```

Expected: all tests PASS.

- [ ] **Step 8: Run compile check**

Run:

```powershell
python -m compileall -q app tests
```

Expected: exit code 0.

- [ ] **Step 9: Commit**

Run:

```powershell
git add app/gui/dashboard2.py tests/test_song_catalog.py
git commit -m "Wire dashboard to catalog records"
```

## Task 8: Documentation And Environment Variables

**Files:**
- Modify: `.env.example`
- Modify: `docs/local-assets.md`
- Modify: `docs/model-artifacts.md`
- Modify: `README.md`

- [ ] **Step 1: Update `.env.example`**

Add these lines under the existing local assets section:

```text
MYRHYTHM_FER_MODEL_PATH=C:/path/to/models/myrhythm_fer.h5
MYRHYTHM_HR_MODEL_PATH=C:/path/to/models/lstm_model.keras
MYRHYTHM_HR_LABEL_ENCODER_PATH=C:/path/to/models/label_encoder.pkl
```

- [ ] **Step 2: Update `docs/local-assets.md`**

Add this section:

```markdown
## Real-Device Local Setup

For webcam FER and BLE heart-rate testing, keep model artifacts outside Git and point the app to them with:

- `MYRHYTHM_FER_MODEL_PATH`
- `MYRHYTHM_HR_MODEL_PATH`
- `MYRHYTHM_HR_LABEL_ENCODER_PATH`

The desktop app should show missing model, missing camera, or missing BLE device status in the Recognition window. It should not persist raw webcam frames, face crops, or raw heart-rate streams by default.
```

- [ ] **Step 3: Update `docs/model-artifacts.md`**

Add this section:

```markdown
## Local Runtime Configuration

The app resolves model artifacts through environment variables first:

- `MYRHYTHM_FER_MODEL_PATH`
- `MYRHYTHM_HR_MODEL_PATH`
- `MYRHYTHM_HR_LABEL_ENCODER_PATH`

If these variables are unset, the app uses the original local default paths under `app/fer/trained_models/` and `app/hr/trained_hr_models/`. Those paths are ignored by Git. Missing artifacts should be reported inside the Recognition window instead of requiring a terminal log.
```

- [ ] **Step 4: Update `README.md`**

Add this subsection under "Run Locally":

````markdown
### Optional Real-Device Features

To run webcam FER and BLE heart-rate recognition, keep model artifacts outside Git and set:

```powershell
$env:MYRHYTHM_FER_MODEL_PATH="C:/path/to/models/myrhythm_fer.h5"
$env:MYRHYTHM_HR_MODEL_PATH="C:/path/to/models/lstm_model.keras"
$env:MYRHYTHM_HR_LABEL_ENCODER_PATH="C:/path/to/models/label_encoder.pkl"
```

Use a local webcam and a BLE heart-rate monitor that exposes the standard Heart Rate Measurement characteristic. The app keeps raw webcam frames and raw heart-rate streams local by default and uses only summary mood labels for recommendations.
````

- [ ] **Step 5: Run documentation grep checks**

Run:

```powershell
rg -n "MYRHYTHM_FER_MODEL_PATH|MYRHYTHM_HR_MODEL_PATH|MYRHYTHM_HR_LABEL_ENCODER_PATH" .env.example README.md docs
```

Expected: each variable appears in `.env.example`, `README.md`, `docs/local-assets.md`, `docs/model-artifacts.md`, and the design spec.

- [ ] **Step 6: Commit**

Run:

```powershell
git add .env.example docs/local-assets.md docs/model-artifacts.md README.md
git commit -m "Document real-device local setup"
```

## Task 9: Final Verification And Privacy Scan

**Files:**
- No planned source edits.

- [ ] **Step 1: Run full available tests**

Run:

```powershell
python -m pytest tests -v
```

Expected: all non-optional tests PASS. Optional dependency tests may SKIP when local audio/ML dependencies or licensed assets are absent.

- [ ] **Step 2: Run compile check**

Run:

```powershell
python -m compileall -q app tests
```

Expected: exit code 0.

- [ ] **Step 3: Run artifact privacy scan**

Run:

```powershell
git ls-files | rg -i "\.(mp3|wav|flac|ogg|m4a|h5|keras|pkl|joblib|onnx|pt|pth|db|sqlite|sqlite3)$"
```

Expected: no output.

- [ ] **Step 4: Run environment privacy scan**

Run:

```powershell
git ls-files | rg -i "(^|/)\.env$|secret|service-role|r2_access|supabase_service"
```

Expected: no output.

- [ ] **Step 5: Inspect final diff**

Run:

```powershell
git status --short --branch
git log --oneline -10
```

Expected: branch contains the task commits and no unstaged source changes.

## Spec Coverage Review

- Real webcam FER: covered by Tasks 1, 3, and 6.
- Real BLE heart rate: covered by Tasks 1, 3, and 6.
- Visible FER/HR/BPM/fused mood state: covered by Tasks 2 and 6.
- Summary labels into recommendations: covered by Tasks 2, 5, and 6.
- Dashboard recommendations, covers, and reason: covered by Tasks 4, 5, and 7.
- Missing covers use `media/default_cover.png` without reports: covered by Tasks 1, 4, 5, and 7.
- Future Supabase/R2 compatibility: covered by the Song Catalog and runtime artifact seams in Tasks 1, 4, and 8.
- Sensitive raw data and artifact safety: covered by Tasks 8 and 9.

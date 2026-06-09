from dataclasses import dataclass
from pathlib import Path
from typing import Mapping, Optional, Union
import os


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_FER_MODEL = PROJECT_ROOT / "app" / "fer" / "trained_models" / "myrhythm_fer.h5"
DEFAULT_HR_MODEL = PROJECT_ROOT / "app" / "hr" / "trained_hr_models" / "lstm_model.keras"
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
    song_manifest: ResolvedPath
    music_dir: ResolvedPath
    default_cover: Path


def _path_from_env(
    env_name: str,
    default_path: Path,
    env: Mapping[str, str],
    overrides: Mapping[str, Union[str, Path]],
) -> ResolvedPath:
    override_value = overrides.get(env_name)
    raw_value = override_value or env.get(env_name)
    if override_value:
        source = "runtime_override"
    else:
        source = env_name if raw_value else "default"
    candidate = Path(raw_value) if raw_value else default_path
    if not candidate.is_absolute():
        candidate = PROJECT_ROOT / candidate
    candidate = candidate.resolve()
    return ResolvedPath(path=candidate, exists=candidate.exists(), source=source)


def resolve_runtime_assets(
    env: Optional[Mapping[str, str]] = None,
    overrides: Optional[Mapping[str, Union[str, Path]]] = None,
) -> RuntimeAssets:
    active_env = os.environ if env is None else env
    active_overrides = {} if overrides is None else overrides
    return RuntimeAssets(
        fer_model=_path_from_env(
            "MYRHYTHM_FER_MODEL_PATH",
            DEFAULT_FER_MODEL,
            active_env,
            active_overrides,
        ),
        hr_model=_path_from_env(
            "MYRHYTHM_HR_MODEL_PATH",
            DEFAULT_HR_MODEL,
            active_env,
            active_overrides,
        ),
        song_manifest=_path_from_env(
            "MYRHYTHM_SONG_MANIFEST",
            DEFAULT_SONG_MANIFEST,
            active_env,
            active_overrides,
        ),
        music_dir=_path_from_env(
            "MYRHYTHM_MUSIC_DIR",
            DEFAULT_MUSIC_DIR,
            active_env,
            active_overrides,
        ),
        default_cover=DEFAULT_COVER,
    )


def resolve_cover_path(
    cover_path: Optional[Union[str, Path]],
    default_cover: Union[str, Path] = DEFAULT_COVER,
) -> Path:
    fallback = Path(default_cover)
    if not fallback.is_absolute():
        fallback = PROJECT_ROOT / fallback
    fallback = fallback.resolve()
    if not cover_path:
        return fallback

    candidate = Path(cover_path)
    if not candidate.is_absolute():
        candidate = (PROJECT_ROOT / candidate).resolve()
    else:
        candidate = candidate.resolve()

    return candidate if candidate.exists() else fallback

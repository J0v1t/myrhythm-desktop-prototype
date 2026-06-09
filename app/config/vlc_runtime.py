"""Readiness checks for the native VLC runtime."""

from __future__ import annotations

import importlib
from dataclasses import dataclass
from typing import Callable, Optional


VLC_PREREQUISITE_MESSAGE = (
    "Install VLC media player with native libVLC matching your Python architecture, "
    "then restart MyRhythm."
)


@dataclass(frozen=True)
class VlcReadiness:
    ready: bool
    message: str
    error: Optional[str] = None


def check_vlc_readiness(
    vlc_module: Optional[object] = None,
    import_module: Callable[[str], object] = importlib.import_module,
) -> VlcReadiness:
    """Verify that python-vlc can create an instance backed by native libVLC."""
    try:
        active_vlc = vlc_module if vlc_module is not None else import_module("vlc")
    except Exception as exc:
        return VlcReadiness(
            ready=False,
            message=VLC_PREREQUISITE_MESSAGE,
            error=f"python-vlc is unavailable: {exc}",
        )

    try:
        instance = active_vlc.Instance("--no-plugins-cache")
        if instance is None:
            raise RuntimeError("python-vlc did not create a native libVLC instance")
    except Exception as exc:
        return VlcReadiness(
            ready=False,
            message=VLC_PREREQUISITE_MESSAGE,
            error=f"native libVLC is unavailable: {exc}",
        )

    release = getattr(instance, "release", None)
    if callable(release):
        try:
            release()
        except Exception:
            pass

    return VlcReadiness(ready=True, message="VLC playback is ready.")

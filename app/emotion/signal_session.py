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
            fer_confidence=confidence
            if confidence is not None
            else self.state.fer_confidence,
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

from typing import Optional

VALID_EMOTIONS = {"happy", "sad", "neutral", "angry"}

_FUSION_TABLE = {
    "happy": {"happy": "happy", "sad": "neutral", "neutral": "happy", "angry": "angry"},
    "sad": {"happy": "neutral", "sad": "sad", "neutral": "sad", "angry": "angry"},
    "neutral": {"happy": "happy", "sad": "sad", "neutral": "neutral", "angry": "angry"},
    "angry": {"happy": "angry", "sad": "sad", "neutral": "angry", "angry": "angry"},
}


def normalize_emotion(label: str) -> Optional[str]:
    if label is None:
        return None
    l = label.strip().lower()
    if l in VALID_EMOTIONS:
        return l
    # common synonyms
    if l in {"joy", "joyful", "pleased", "glad", "content"}:
        return "happy"
    if l in {"depressed", "down", "unhappy", "sadness", "lonely", "tired"}:
        return "sad"
    if l in {"angry", "rage", "irritated", "frustrated", "annoyed"}:
        return "angry"
    if l in {"calm", "okay", "ok", "neutral", "meh", "indifferent", "relaxed"}:
        return "neutral"
    # fallback None
    return None


def fuse_emotions(fer: Optional[str], hr: Optional[str]) -> Optional[str]:
    fer_n = normalize_emotion(fer) if fer else None
    hr_n = normalize_emotion(hr) if hr else None

    if fer_n is None and hr_n is None:
        return None
    if fer_n is None:
        return hr_n
    if hr_n is None:
        return fer_n
    if fer_n == hr_n:
        return fer_n

    return _FUSION_TABLE.get(fer_n, {}).get(hr_n, "neutral")
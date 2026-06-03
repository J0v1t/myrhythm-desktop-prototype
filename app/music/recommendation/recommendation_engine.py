"""
recommender_engine.py

Core recommendation logic for MyRhythm:
- Accepts user id + optional mood inputs (fer, hr, or combined)
- Scores candidate songs using genre->emotion mapping and user preferences
- Returns ranked list of songs (with reason / score breakdown)
"""

import os
import sys
import json
import random
from collections import defaultdict
from typing import Any, List, Optional, Dict, Tuple

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, PROJECT_ROOT)

try:
    from app.database.schema import SessionLocal
    from app.database.models import Song, UserPreferences
except ModuleNotFoundError:
    SessionLocal = None

    class Song:
        pass

    class UserPreferences:
        pass

from app.music.mood.mood_router import fuse_emotions, normalize_emotion
from app.config.runtime_assets import DEFAULT_COVER, resolve_cover_path

MODEL_DIR = os.path.join(PROJECT_ROOT, "app", "music", "recommendation")
GENRE_MAP_PATH = os.path.join(MODEL_DIR, "genre_mapping.json")
ARTIST_MAP_PATH = os.path.join(MODEL_DIR, "artist_mapping.json")

# weights for scoring
DEFAULT_WEIGHTS = {
    "emotion_match": 0.60,
    "genre_preference": 0.25,
    "artist_preference": 0.15
}

with open(GENRE_MAP_PATH, "r", encoding="utf-8") as f:
    GENRE_TO_EMOTION = json.load(f)

with open(ARTIST_MAP_PATH, "r", encoding="utf-8") as f:
    ARTIST_TO_EMOTION = json.load(f)

def map_genre_to_emotion(genre: str) -> str:
    if not genre:
        return "neutral"
    g = genre.strip().lower()
    return GENRE_TO_EMOTION.get(g, "neutral")

def map_artist_to_emotion(artist: str) -> str:
    if not artist:
        return "neutral"
    a = artist.strip().lower()
    return ARTIST_TO_EMOTION.get(a, "neutral")


class RecommendationEngine:
    def __init__(self, db: Optional[Any] = None, weights: Dict = None):
        if db is not None:
            self.db = db
        elif SessionLocal is not None:
            self.db = SessionLocal()
        else:
            raise RuntimeError("SQLAlchemy is required when no database adapter is provided.")
        self.weights = weights or DEFAULT_WEIGHTS

    # -------------------------
    # User preference helpers
    # -------------------------
    def _get_user_prefs(self, user_id: int) -> Dict:
        prefs = {"favorite_genres": set(), "favorite_artists": set()}
        try:
            up = self.db.query(UserPreferences).filter_by(user_id=user_id).first()
            if not up:
                return prefs
            prefs["favorite_genres"] = {g.strip().lower() for g in up.favorite_genres.split(",") if g.strip()}
            prefs["favorite_artists"] = {a.strip().lower() for a in up.favorite_artists.split(",") if a.strip()}
        except Exception:
            pass
        return prefs
    
    # -------------------------
    # Candidate retrieval
    # -------------------------
    def _get_candidate_songs(self, limit=500) -> List[Any]:
        """
        Return candidate Song rows.
        You can refine this to prefer songs in user's preferred genres to reduce scoring cost.
        """
        return self.db.query(Song).limit(limit).all()

    # -------------------------
    # Score calculation
    # -------------------------
    def _score_song(self, user_emotion: str, prefs: Dict, target_song: Any) -> Tuple[float, Dict]:
        """
        Compute composite score and return (score, breakdown)
        - Emotion match (genre → emotion)
        - Genre preference
        - Artist preference based on user's preferred artists mapped to emotions
        """
        weights = self.weights
        breakdown = {"emotion_match": 0.0, "genre_preference": 0.0, "artist_preference": 0.0}

        song_genre = (target_song.genre or "").strip().lower()

        # ----- Emotion match (GENRE → emotion) -----
        song_emotion = map_genre_to_emotion(song_genre)
        breakdown["emotion_match"] = 1.0 if song_emotion == user_emotion else 0.0

        # ----- Genre preference -----
        favorite_genres = prefs.get("favorite_genres", set())
        breakdown["genre_preference"] = 1.0 if song_genre in favorite_genres else 0.0

        # ----- Artist preference based on user's preferred artists mapped to emotions -----
        preferred_artists = prefs.get("favorite_artists", set())
        user_artist_emotions = {map_artist_to_emotion(a) for a in preferred_artists}
        breakdown["artist_preference"] = 1.0 if user_emotion in user_artist_emotions else 0.0

        # ----- FINAL WEIGHTED SCORE -----
        score = (
            weights["emotion_match"] * breakdown["emotion_match"] +
            weights["genre_preference"] * breakdown["genre_preference"] +
            weights["artist_preference"] * breakdown["artist_preference"]
        )

        return float(score), breakdown
    
    def determine_emotion(self, fer_emotion: Optional[str], hr_emotion: Optional[str], combined_mode: bool) -> str:
        """
        Calculates the final user emotion based on the inputs and mode.
        This logic is shared between the core recommend method and the GUI for the title.
        """
        # 1) determine user emotion
        fer_n = normalize_emotion(fer_emotion) if fer_emotion else None
        hr_n = normalize_emotion(hr_emotion) if hr_emotion else None

        if combined_mode:
            user_emotion = fuse_emotions(fer_n, hr_n)
        else:
            # priority: explicit FER/HR provided > neutral fallback
            user_emotion = fer_n or hr_n or "neutral"

        # Ensure the emotion is one of the four main categories and normalized
        user_emotion = user_emotion.lower() if user_emotion else "neutral"
        return user_emotion if user_emotion in {"happy", "sad", "neutral", "angry"} else "neutral"
    
    # -------------------------
    # Public API
    # -------------------------
    def recommend(
            self,
            user_id: int,
            fer_emotion: Optional[str] = None,
            hr_emotion: Optional[str] = None,
            combined_mode: bool = False,
            candidate_limit: int = 500,
            top_k: int = 10) -> List[Dict]:

        """
        Main entrypoint.

        - user_id: for preferences/history
        - fer_emotion: categorical string or None
        - hr_emotion: categorical string or None
        - combined_mode: if True will fuse FER+HR via mood_router.fuse_emotions
        - candidate_limit: how many songs to consider before ranking
        - top_k: how many songs to return
        """

        # 1) determine user emotion
        fer_n = normalize_emotion(fer_emotion) if fer_emotion else None
        hr_n = normalize_emotion(hr_emotion) if hr_emotion else None

        if combined_mode:
            user_emotion = fuse_emotions(fer_n, hr_n)
        else:
            user_emotion = fer_n or hr_n or "neutral"

        user_emotion = user_emotion if user_emotion in {"happy", "sad", "neutral", "angry"} else "neutral"

        # 2) get user preferences
        prefs = self._get_user_prefs(user_id)

        # 3) get candidate songs
        songs = self._get_candidate_songs(limit=candidate_limit)

        scored = []
        default_cover = DEFAULT_COVER
        reason = f"Recommended for fused mood: {user_emotion.capitalize()}"

        for s in songs:
            score, breakdown = self._score_song(user_emotion, prefs, s)

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

        # ---- Bucket shuffle ----
        buckets = defaultdict(list)
        for entry in scored:
            buckets[entry["score"]].append(entry)

        # Randomize inside each score bucket
        for score in buckets:
            random.shuffle(buckets[score])

        # Rebuild sorted list
        sorted_scores = sorted(buckets.keys(), reverse=True)

        randomized_result = []
        for sc in sorted_scores:
            randomized_result.extend(buckets[sc])

        return randomized_result[:top_k]

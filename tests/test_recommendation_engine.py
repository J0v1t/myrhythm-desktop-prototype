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
    prefs = SimpleNamespace(
        favorite_genres="pop",
        favorite_artists="",
        mood_mapping="{}",
    )
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


def test_recommendation_uses_injected_cloud_catalog_and_preferences():
    song = SimpleNamespace(
        id="song-123",
        title="Cloud Track",
        artist="Cloud Artist",
        genre="pop",
        duration=120,
        file_path="",
        cover_path="",
        track_object_key="tracks/cloud-track.mp3",
        track_checksum_sha256="a" * 64,
        cover_object_key="covers/cloud-track.webp",
        cover_checksum_sha256="b" * 64,
    )
    engine = RecommendationEngine(
        songs=[song],
        preferences={
            "favorite_genres": ["pop"],
            "favorite_artists": ["Cloud Artist"],
        },
    )

    results = engine.recommend(
        user_id="user-123",
        fer_emotion="happy",
        top_k=1,
    )

    assert results[0]["song_id"] == "song-123"
    assert results[0]["track_object_key"] == "tracks/cloud-track.mp3"
    assert results[0]["cover_object_key"] == "covers/cloud-track.webp"
    assert results[0]["track_checksum_sha256"] == "a" * 64
    assert results[0]["cover_checksum_sha256"] == "b" * 64


def test_real_artist_preference_scores_direct_artist_match():
    preferred = SimpleNamespace(
        id="preferred",
        title="Preferred",
        artist="Real Artist",
        genre="unknown",
        file_path="",
        cover_path="",
    )
    other = SimpleNamespace(
        id="other",
        title="Other",
        artist="Different Artist",
        genre="unknown",
        file_path="",
        cover_path="",
    )
    engine = RecommendationEngine(
        songs=[other, preferred],
        preferences={
            "favorite_genres": [],
            "favorite_artists": ["Real Artist"],
        },
    )

    results = engine.recommend(user_id="user-1", top_k=2)

    assert results[0]["song_id"] == "preferred"
    assert results[0]["breakdown"]["artist_preference"] == 1.0
    assert results[1]["breakdown"]["artist_preference"] == 0.0

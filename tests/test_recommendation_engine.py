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

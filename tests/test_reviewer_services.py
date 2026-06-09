from pathlib import Path
from types import SimpleNamespace

from app.cloud.reviewer_services import ReviewerCloudServices


def _song(title="Song", artist="Artist"):
    return SimpleNamespace(
        id="song-1",
        title=title,
        artist=artist,
        genre="pop",
        file_path="",
        cover_path="",
        track_object_key="tracks/song.mp3",
        track_checksum_sha256="a" * 64,
        cover_object_key="covers/song.webp",
        cover_checksum_sha256="b" * 64,
    )


class FakeDataClient:
    def __init__(self):
        self.preferences = {
            "genres": ["POP"],
            "artists": ["Artist"],
            "mood_map": {},
        }

    def list_song_catalog(self):
        return [_song("Song A", "Artist B"), _song("Song B", "Artist A")]

    def get_user_preferences(self, user_id):
        return self.preferences

    def save_user_preferences(self, user_id, genres, artists, mood_map):
        self.preferences = {
            "genres": genres,
            "artists": artists,
            "mood_map": mood_map,
        }
        return self.preferences

    def list_model_artifacts(self):
        return []


class FakeCache:
    def __init__(self):
        self.requests = []

    def get_music_asset(self, client, object_key, checksum, expected_size=None):
        self.requests.append((object_key, checksum, expected_size))
        return Path("cache") / Path(object_key).name


def _services(data=None):
    return ReviewerCloudServices(
        SimpleNamespace(id="user-1"),
        data_client=data or FakeDataClient(),
        asset_client=object(),
        asset_cache=FakeCache(),
    )


def test_reviewer_services_loads_and_reuses_cloud_catalog():
    services = _services()

    first = services.load_catalog()
    second = services.load_catalog()

    assert first is second
    assert [song.title for song in first] == ["Song A", "Song B"]
    assert services.list_artists() == ["Artist A", "Artist B"]


def test_reviewer_services_prepares_verified_music_assets():
    services = _services()
    song = _song()
    song.track_byte_size = 123
    song.cover_byte_size = 45

    assert services.prepare_track(song) == Path("cache/song.mp3")
    assert services.prepare_cover(song) == Path("cache/song.webp")
    assert services.asset_cache.requests == [
        ("tracks/song.mp3", "a" * 64, 123),
        ("covers/song.webp", "b" * 64, 45),
    ]


def test_reviewer_services_saves_and_reloads_cloud_preferences():
    services = _services()

    result = services.save_user_preferences(
        "user-1",
        ["ROCK"],
        ["Real Artist"],
        {"happy": "ROCK"},
    )

    assert result["artists"] == ["Real Artist"]
    assert services.load_preferences()["genres"] == ["ROCK"]


def test_reviewer_services_builds_recommender_from_cloud_data():
    services = _services()

    engine = services.recommendation_engine()

    assert [song.title for song in engine._songs] == ["Song A", "Song B"]
    assert engine._preferences == {
        "favorite_genres": ["POP"],
        "favorite_artists": ["Artist"],
    }


def test_reviewer_services_does_not_provision_models_when_loading_catalog():
    services = _services()

    services.load_catalog()

    assert not hasattr(services.asset_cache, "model_downloads")

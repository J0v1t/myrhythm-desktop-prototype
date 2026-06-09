from urllib.parse import parse_qs, urlparse

from app.cloud.supabase_data import SupabaseDataClient
from app.music.catalog import SongCatalogRecord


def test_get_user_preferences_requests_authenticated_user_row():
    calls = []

    def fake_request(method, url, headers, payload, timeout):
        calls.append((method, url, headers, payload, timeout))
        return [
            {
                "user_id": "user-123",
                "favorite_genres": ["ROCK"],
                "favorite_artists": ["ARTIST A"],
                "mood_mapping": {"happy": "ROCK"},
            }
        ]

    client = SupabaseDataClient(
        "https://example.supabase.co/rest/v1/",
        "sb_publishable_test",
        "access-token",
        request_json=fake_request,
    )

    result = client.get_user_preferences("user-123")

    assert result == {
        "genres": ["ROCK"],
        "artists": ["ARTIST A"],
        "mood_map": {"happy": "ROCK"},
    }
    method, url, headers, payload, timeout = calls[0]
    assert method == "GET"
    assert url == (
        "https://example.supabase.co/rest/v1/user_preferences"
        "?user_id=eq.user-123&select=user_id%2Cfavorite_genres%2Cfavorite_artists%2Cmood_mapping"
    )
    assert headers["apikey"] == "sb_publishable_test"
    assert headers["Authorization"] == "Bearer access-token"
    assert payload is None
    assert timeout == 15


def test_save_user_preferences_upserts_authenticated_user_row():
    calls = []

    def fake_request(method, url, headers, payload, timeout):
        calls.append((method, url, headers, payload, timeout))
        return [payload]

    client = SupabaseDataClient(
        "https://example.supabase.co",
        "sb_publishable_test",
        "access-token",
        request_json=fake_request,
    )

    result = client.save_user_preferences(
        "user-123",
        ["ROCK", "POP"],
        ["ARTIST A"],
        {"happy": "POP"},
    )

    assert result["genres"] == ["ROCK", "POP"]
    method, url, headers, payload, timeout = calls[0]
    assert method == "POST"
    assert url == "https://example.supabase.co/rest/v1/user_preferences?on_conflict=user_id"
    assert headers["Prefer"] == "resolution=merge-duplicates,return=representation"
    assert payload == {
        "user_id": "user-123",
        "favorite_genres": ["ROCK", "POP"],
        "favorite_artists": ["ARTIST A"],
        "mood_mapping": {"happy": "POP"},
    }


def test_has_completed_preferences_requires_genre_and_artist():
    assert SupabaseDataClient.has_completed_preferences(
        {"genres": ["ROCK"], "artists": ["ARTIST A"], "mood_map": {}}
    )
    assert not SupabaseDataClient.has_completed_preferences(
        {"genres": [], "artists": ["ARTIST A"], "mood_map": {}}
    )


def test_list_song_catalog_requests_active_songs_with_related_assets():
    calls = []

    def fake_request(method, url, headers, payload, timeout):
        calls.append((method, url, headers, payload, timeout))
        return [
            {
                "id": "song-123",
                "title": "Cloud Track",
                "artist": "Cloud Artist",
                "genre": "pop",
                "duration_seconds": 123.5,
                "license_status": "licensed",
                "source_notes": "curated",
                "assets": [
                    {
                        "asset_kind": "track",
                        "object_key": "tracks/cloud-track.mp3",
                        "checksum_sha256": "a" * 64,
                        "content_type": "audio/mpeg",
                        "byte_size": 2048,
                    },
                    {
                        "asset_kind": "cover",
                        "object_key": "covers/cloud-track.webp",
                        "checksum_sha256": "b" * 64,
                        "content_type": "image/webp",
                        "byte_size": 512,
                    },
                ],
            }
        ]

    client = SupabaseDataClient(
        "https://example.supabase.co",
        "sb_publishable_test",
        "access-token",
        request_json=fake_request,
    )

    records = client.list_song_catalog()

    assert records == [
        SongCatalogRecord(
            id="song-123",
            title="Cloud Track",
            artist="Cloud Artist",
            genre="pop",
            duration=123.5,
            file_path="",
            cover_path=records[0].cover_path,
            license_status="licensed",
            source_notes="curated",
            track_object_key="tracks/cloud-track.mp3",
            track_checksum_sha256="a" * 64,
            track_content_type="audio/mpeg",
            track_byte_size=2048,
            cover_object_key="covers/cloud-track.webp",
            cover_checksum_sha256="b" * 64,
            cover_content_type="image/webp",
            cover_byte_size=512,
        )
    ]
    method, url, headers, payload, timeout = calls[0]
    query = parse_qs(urlparse(url).query)
    assert method == "GET"
    assert urlparse(url).path == "/rest/v1/songs"
    assert query["is_active"] == ["eq.true"]
    assert query["order"] == ["title.asc"]
    assert "assets:asset_objects" in query["select"][0]
    assert headers["Authorization"] == "Bearer access-token"
    assert payload is None
    assert timeout == 15


def test_list_model_artifacts_requests_active_models_with_related_asset():
    calls = []

    def fake_request(method, url, headers, payload, timeout):
        calls.append((method, url, headers, payload, timeout))
        return [
            {
                "id": "model-123",
                "model_type": "fer",
                "version": "v1",
                "framework": "keras",
                "status": "active",
                "metrics": {"input_shape": [48, 48, 1]},
                "asset": {
                    "object_key": "fer/v1/myrhythm_fer.h5",
                    "checksum_sha256": "c" * 64,
                    "content_type": "application/x-hdf5",
                    "byte_size": 4096,
                },
            }
        ]

    client = SupabaseDataClient(
        "https://example.supabase.co",
        "sb_publishable_test",
        "access-token",
        request_json=fake_request,
    )

    artifacts = client.list_model_artifacts()

    assert len(artifacts) == 1
    assert artifacts[0].id == "model-123"
    assert artifacts[0].artifact_type == "fer"
    assert artifacts[0].version == "v1"
    assert artifacts[0].object_key == "fer/v1/myrhythm_fer.h5"
    assert artifacts[0].checksum_sha256 == "c" * 64
    assert artifacts[0].content_type == "application/x-hdf5"
    assert artifacts[0].byte_size == 4096
    assert artifacts[0].compatibility == {"input_shape": [48, 48, 1]}

    method, url, _, payload, _ = calls[0]
    query = parse_qs(urlparse(url).query)
    assert method == "GET"
    assert urlparse(url).path == "/rest/v1/model_artifacts"
    assert query["status"] == ["eq.active"]
    assert "asset:asset_objects" in query["select"][0]
    assert payload is None

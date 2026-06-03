from app.cloud.supabase_data import SupabaseDataClient


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

import pytest

from app.cloud.asset_api import AssetResponse, CloudflareAssetClient


def test_asset_client_fetches_music_asset_with_supabase_token():
    calls = []

    def fake_request(url, headers, timeout):
        calls.append((url, headers, timeout))
        return AssetResponse(b"cover", "image/webp")

    client = CloudflareAssetClient(
        "https://assets.example.test/",
        "access-token",
        request_asset=fake_request,
    )

    response = client.fetch_music_asset("covers/a song.webp")

    assert response.content == b"cover"
    assert response.content_type == "image/webp"
    url, headers, timeout = calls[0]
    assert url == "https://assets.example.test/assets/music/covers/a%20song.webp"
    assert headers["Authorization"] == "Bearer access-token"
    assert headers["User-Agent"] == "MyRhythmDesktop/1.0"
    assert timeout == 15


def test_asset_client_builds_model_asset_urls():
    client = CloudflareAssetClient("https://assets.example.test", "access-token")

    assert (
        client.model_asset_url("fer/v1/myrhythm_fer.h5")
        == "https://assets.example.test/assets/models/fer/v1/myrhythm_fer.h5"
    )


def test_asset_client_rejects_unsafe_object_keys():
    client = CloudflareAssetClient("https://assets.example.test", "access-token")

    with pytest.raises(ValueError):
        client.music_asset_url("../secret")

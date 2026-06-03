import io

import pytest
from urllib.error import HTTPError

from app.cloud.asset_api import AssetResponse, CloudflareAssetClient, _request_asset


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


def test_asset_client_reports_rate_limits(monkeypatch):
    def fake_urlopen(req, timeout):
        raise HTTPError(req.full_url, 429, "Too Many Requests", {}, io.BytesIO(b"{}"))

    monkeypatch.setattr("app.cloud.asset_api.request.urlopen", fake_urlopen)

    with pytest.raises(RuntimeError, match="Too many asset requests"):
        _request_asset("https://assets.example.test/a", {}, 15)


def test_asset_client_reports_forbidden_assets(monkeypatch):
    def fake_urlopen(req, timeout):
        raise HTTPError(req.full_url, 403, "Forbidden", {}, io.BytesIO(b"{}"))

    monkeypatch.setattr("app.cloud.asset_api.request.urlopen", fake_urlopen)

    with pytest.raises(RuntimeError, match="not available"):
        _request_asset("https://assets.example.test/a", {}, 15)

import io

import pytest
from urllib.error import HTTPError

from app.cloud.asset_api import (
    DEFAULT_MAX_ASSET_BYTES,
    AssetResponse,
    CloudflareAssetClient,
    _download_asset,
    _request_asset,
)


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


def test_asset_client_preserves_positional_timeout_constructor_contract():
    calls = []

    def fake_request(url, headers, timeout):
        calls.append(timeout)
        return AssetResponse(b"cover", "image/webp")

    client = CloudflareAssetClient(
        "https://assets.example.test/",
        "access-token",
        fake_request,
        7,
    )

    client.fetch_music_asset("covers/song.webp")

    assert calls == [7]


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


def test_asset_client_downloads_music_asset_to_file(tmp_path):
    calls = []

    def fake_download(url, headers, destination, timeout):
        calls.append((url, headers, destination, timeout))
        destination.write_bytes(b"track")
        return destination

    client = CloudflareAssetClient(
        "https://assets.example.test/",
        "access-token",
        download_asset=fake_download,
    )
    destination = tmp_path / "track.mp3"

    result = client.download_music_asset("tracks/a song.mp3", destination)

    assert result == destination
    assert destination.read_bytes() == b"track"
    url, headers, written_path, timeout = calls[0]
    assert url == "https://assets.example.test/assets/music/tracks/a%20song.mp3"
    assert headers["Authorization"] == "Bearer access-token"
    assert written_path == destination
    assert timeout == 15


def test_asset_client_downloads_model_asset_to_file(tmp_path):
    calls = []

    def fake_download(url, headers, destination, timeout):
        calls.append((url, destination))
        destination.write_bytes(b"model")
        return destination

    client = CloudflareAssetClient(
        "https://assets.example.test/",
        "access-token",
        download_asset=fake_download,
    )
    destination = tmp_path / "model.h5"

    result = client.download_model_asset("fer/v1/model.h5", destination)

    assert result == destination
    assert calls == [
        ("https://assets.example.test/assets/models/fer/v1/model.h5", destination)
    ]


def test_request_download_streams_response_in_chunks(monkeypatch, tmp_path):
    class StreamingResponse:
        headers = {"Content-Type": "audio/mpeg"}

        def __init__(self):
            self.chunks = iter([b"one", b"two", b""])

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return None

        def read(self, size=-1):
            assert size > 0
            return next(self.chunks)

    monkeypatch.setattr(
        "app.cloud.asset_api.request.urlopen",
        lambda req, timeout: StreamingResponse(),
    )
    destination = tmp_path / "streamed.bin"

    result = _download_asset("https://assets.example.test/a", {}, destination, 15)

    assert result == destination
    assert destination.read_bytes() == b"onetwo"


def test_request_download_rejects_oversized_content_length_before_writing(
    monkeypatch,
    tmp_path,
):
    class OversizedResponse:
        headers = {"Content-Length": "7"}

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return None

    monkeypatch.setattr(
        "app.cloud.asset_api.request.urlopen",
        lambda req, timeout: OversizedResponse(),
    )
    destination = tmp_path / "oversized.bin"

    with pytest.raises(RuntimeError, match="maximum allowed size"):
        _download_asset(
            "https://assets.example.test/a",
            {},
            destination,
            15,
            max_bytes=6,
        )

    assert not destination.exists()


def test_request_download_stops_unbounded_stream_at_client_limit(monkeypatch, tmp_path):
    class StreamingResponse:
        headers = {}

        def __init__(self):
            self.chunks = iter([b"123", b"456", b""])

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return None

        def read(self, size=-1):
            return next(self.chunks)

    monkeypatch.setattr(
        "app.cloud.asset_api.request.urlopen",
        lambda req, timeout: StreamingResponse(),
    )
    destination = tmp_path / "oversized.bin"

    with pytest.raises(RuntimeError, match="maximum allowed size"):
        _download_asset(
            "https://assets.example.test/a",
            {},
            destination,
            15,
            max_bytes=5,
        )

    assert not destination.exists()
    assert DEFAULT_MAX_ASSET_BYTES == 64 * 1024 * 1024

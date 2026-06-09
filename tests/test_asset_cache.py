import hashlib
from pathlib import Path

import pytest

from app.cloud.asset_cache import AssetCache, AssetIntegrityError


class FakeAssetClient:
    def __init__(self, content: bytes):
        self.content = content
        self.music_downloads = []
        self.model_downloads = []

    def download_music_asset(self, object_key: str, destination: Path) -> Path:
        self.music_downloads.append((object_key, destination))
        destination.write_bytes(self.content)
        return destination

    def download_model_asset(self, object_key: str, destination: Path) -> Path:
        self.model_downloads.append((object_key, destination))
        destination.write_bytes(self.content)
        return destination


def sha256(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def test_asset_cache_defaults_outside_repository(monkeypatch, tmp_path):
    local_app_data = tmp_path / "local-app-data"
    monkeypatch.delenv("MYRHYTHM_ASSET_CACHE_DIR", raising=False)
    monkeypatch.setenv("LOCALAPPDATA", str(local_app_data))

    cache = AssetCache()

    assert cache.root == local_app_data / "MyRhythm" / "asset-cache"


def test_asset_cache_downloads_atomically_and_reuses_verified_music(tmp_path):
    content = b"verified track"
    client = FakeAssetClient(content)
    cache = AssetCache(tmp_path / "cache")

    first = cache.get_music_asset(client, "tracks/cloud/song.mp3", sha256(content))
    second = cache.get_music_asset(client, "tracks/cloud/song.mp3", sha256(content))

    assert first == second
    assert first.read_bytes() == content
    assert sha256(content) in first.parts
    assert first.parts[-3:] == ("tracks", "cloud", "song.mp3")
    assert len(client.music_downloads) == 1
    assert client.music_downloads[0][1] != first
    assert not list(first.parent.glob("*.tmp"))


def test_asset_cache_replaces_corrupt_cached_file(tmp_path):
    expected = b"fresh track"
    client = FakeAssetClient(expected)
    cache = AssetCache(tmp_path / "cache")
    cached = cache.get_music_asset(client, "tracks/song.mp3", sha256(expected))
    cached.write_bytes(b"corrupt")

    result = cache.get_music_asset(client, "tracks/song.mp3", sha256(expected))

    assert result == cached
    assert result.read_bytes() == expected
    assert len(client.music_downloads) == 2


def test_asset_cache_rejects_checksum_mismatch_without_exposing_file(tmp_path):
    client = FakeAssetClient(b"wrong bytes")
    cache = AssetCache(tmp_path / "cache")

    with pytest.raises(AssetIntegrityError, match="SHA-256"):
        cache.get_model_asset(client, "fer/v1/model.h5", sha256(b"expected bytes"))

    assert not list((tmp_path / "cache").rglob("model.h5"))
    assert not list((tmp_path / "cache").rglob("*.tmp"))


def test_asset_cache_rejects_byte_size_mismatch_without_exposing_file(tmp_path):
    client = FakeAssetClient(b"unexpected length")
    cache = AssetCache(tmp_path / "cache")

    with pytest.raises(AssetIntegrityError, match="byte size"):
        cache.get_music_asset(
            client,
            "tracks/song.mp3",
            sha256(b"unexpected length"),
            expected_size=999,
        )

    assert not list((tmp_path / "cache").rglob("song.mp3"))
    assert not list((tmp_path / "cache").rglob("*.tmp"))


def test_asset_cache_cleans_partial_download_after_client_error(tmp_path):
    class FailingClient(FakeAssetClient):
        def download_music_asset(self, object_key: str, destination: Path) -> Path:
            destination.write_bytes(b"partial")
            raise RuntimeError("download interrupted")

    cache = AssetCache(tmp_path / "cache")

    with pytest.raises(RuntimeError, match="interrupted"):
        cache.get_music_asset(FailingClient(b""), "tracks/song.mp3", sha256(b"expected"))

    assert not list((tmp_path / "cache").rglob("song.mp3"))
    assert not list((tmp_path / "cache").rglob("*.tmp"))


@pytest.mark.parametrize(
    "object_key",
    ["../secret", "/absolute/file", "tracks\\windows-path.mp3", "tracks//empty.mp3"],
)
def test_asset_cache_rejects_unsafe_object_keys(tmp_path, object_key):
    client = FakeAssetClient(b"content")
    cache = AssetCache(tmp_path / "cache")

    with pytest.raises(ValueError, match="Invalid asset object key"):
        cache.get_music_asset(client, object_key, sha256(b"content"))

    assert client.music_downloads == []

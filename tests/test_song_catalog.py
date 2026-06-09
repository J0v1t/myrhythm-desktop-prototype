from types import SimpleNamespace

from app.music.catalog import (
    SongCatalogRecord,
    normalize_cloud_song_record,
    normalize_song_record,
)


def test_normalize_song_record_uses_default_cover_for_missing_cover(tmp_path):
    default_cover = tmp_path / "default_cover.png"
    default_cover.write_bytes(b"default")
    song = SimpleNamespace(
        id=7,
        title="Track A",
        artist="Artist A",
        genre="Pop",
        duration=180,
        file_path=str(tmp_path / "track.mp3"),
        cover_path=str(tmp_path / "missing.png"),
    )

    record = normalize_song_record(song, default_cover=default_cover)

    assert isinstance(record, SongCatalogRecord)
    assert record.id == 7
    assert record.title == "Track A"
    assert record.artist == "Artist A"
    assert record.genre == "Pop"
    assert record.duration == 180
    assert record.file_path.endswith("track.mp3")
    assert record.cover_path == str(default_cover)


def test_normalize_song_record_fills_unknown_text_fields(tmp_path):
    default_cover = tmp_path / "default_cover.png"
    default_cover.write_bytes(b"default")
    song = SimpleNamespace(
        id=None,
        title=None,
        artist=None,
        genre=None,
        duration=None,
        file_path="",
        cover_path=None,
    )

    record = normalize_song_record(song, default_cover=default_cover)

    assert record.title == "Unknown Title"
    assert record.artist == "Unknown Artist"
    assert record.genre == "Unknown Genre"
    assert record.duration is None
    assert record.cover_path == str(default_cover)


def test_catalog_record_can_be_converted_for_legacy_dashboard(tmp_path):
    default_cover = tmp_path / "default_cover.png"
    default_cover.write_bytes(b"default")
    record = SongCatalogRecord(
        id=1,
        title="Track B",
        artist="Artist B",
        genre="Rock",
        duration=210,
        file_path="C:/music/track-b.mp3",
        cover_path=str(default_cover),
        license_status="verified-local",
        source_notes="local test",
    )

    legacy = record.to_simple_namespace()

    assert legacy.id == 1
    assert legacy.title == "Track B"
    assert legacy.artist == "Artist B"
    assert legacy.file_path == "C:/music/track-b.mp3"
    assert legacy.cover_path == str(default_cover)


def test_catalog_record_preserves_recommendation_reason_for_dashboard(tmp_path):
    default_cover = tmp_path / "default_cover.png"
    default_cover.write_bytes(b"default")
    record = SongCatalogRecord(
        id=2,
        title="Mood Track",
        artist="Mood Artist",
        genre="Pop",
        duration=120,
        file_path="C:/music/mood.mp3",
        cover_path=str(default_cover),
        recommendation_reason="Recommended for fused mood: Happy",
    )

    legacy = record.to_simple_namespace()

    assert legacy.recommendation_reason == "Recommended for fused mood: Happy"


def test_cloud_song_record_preserves_object_keys_checksums_and_asset_metadata(tmp_path):
    default_cover = tmp_path / "default_cover.png"
    default_cover.write_bytes(b"default")

    record = normalize_cloud_song_record(
        {
            "id": "song-123",
            "title": "Cloud Track",
            "artist": "Cloud Artist",
            "genre": "pop",
            "duration_seconds": 123.5,
            "license_status": "licensed",
            "source_notes": "curated",
            "track_asset": {
                "object_key": "tracks/cloud-track.mp3",
                "checksum_sha256": "a" * 64,
                "content_type": "audio/mpeg",
                "byte_size": 2048,
            },
            "cover_asset": {
                "object_key": "covers/cloud-track.webp",
                "checksum_sha256": "b" * 64,
                "content_type": "image/webp",
                "byte_size": 512,
            },
        },
        default_cover=default_cover,
    )

    assert record.id == "song-123"
    assert record.file_path == ""
    assert record.cover_path == str(default_cover)
    assert record.track_object_key == "tracks/cloud-track.mp3"
    assert record.track_checksum_sha256 == "a" * 64
    assert record.track_content_type == "audio/mpeg"
    assert record.track_byte_size == 2048
    assert record.cover_object_key == "covers/cloud-track.webp"
    assert record.cover_checksum_sha256 == "b" * 64
    assert record.cover_content_type == "image/webp"
    assert record.cover_byte_size == 512

    legacy = record.to_simple_namespace()
    assert legacy.track_object_key == record.track_object_key
    assert legacy.track_checksum_sha256 == record.track_checksum_sha256
    assert legacy.cover_object_key == record.cover_object_key
    assert legacy.cover_checksum_sha256 == record.cover_checksum_sha256


def test_cloud_song_record_preserves_zero_duration(tmp_path):
    default_cover = tmp_path / "default_cover.png"
    default_cover.write_bytes(b"default")

    record = normalize_cloud_song_record(
        {"title": "Zero Duration", "duration_seconds": 0},
        default_cover=default_cover,
    )

    assert record.duration == 0


def test_cloud_song_record_maps_reverse_related_assets_by_kind(tmp_path):
    default_cover = tmp_path / "default_cover.png"
    default_cover.write_bytes(b"default")

    record = normalize_cloud_song_record(
        {
            "title": "Cloud Track",
            "assets": [
                {
                    "asset_kind": "cover",
                    "object_key": "covers/cloud.webp",
                    "checksum_sha256": "b" * 64,
                },
                {
                    "asset_kind": "track",
                    "object_key": "tracks/cloud.mp3",
                    "checksum_sha256": "a" * 64,
                },
            ],
        },
        default_cover=default_cover,
    )

    assert record.track_object_key == "tracks/cloud.mp3"
    assert record.cover_object_key == "covers/cloud.webp"

from types import SimpleNamespace

from app.music.catalog import SongCatalogRecord, normalize_song_record


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

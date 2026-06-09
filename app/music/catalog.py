from dataclasses import dataclass
from pathlib import Path
from types import SimpleNamespace
from typing import Mapping, Optional, Union

from app.config.runtime_assets import DEFAULT_COVER, resolve_cover_path


@dataclass(frozen=True)
class SongCatalogRecord:
    id: Optional[Union[int, str]]
    title: str
    artist: str
    genre: str
    duration: Optional[float]
    file_path: str
    cover_path: str
    license_status: str = "local"
    source_notes: str = ""
    recommendation_reason: str = ""
    track_object_key: str = ""
    track_checksum_sha256: str = ""
    track_content_type: str = ""
    track_byte_size: Optional[int] = None
    cover_object_key: str = ""
    cover_checksum_sha256: str = ""
    cover_content_type: str = ""
    cover_byte_size: Optional[int] = None

    def to_simple_namespace(self) -> SimpleNamespace:
        return SimpleNamespace(
            id=self.id,
            title=self.title,
            artist=self.artist,
            genre=self.genre,
            duration=self.duration,
            file_path=self.file_path,
            cover_path=self.cover_path,
            recommendation_reason=self.recommendation_reason,
            track_object_key=self.track_object_key,
            track_checksum_sha256=self.track_checksum_sha256,
            track_content_type=self.track_content_type,
            track_byte_size=self.track_byte_size,
            cover_object_key=self.cover_object_key,
            cover_checksum_sha256=self.cover_checksum_sha256,
            cover_content_type=self.cover_content_type,
            cover_byte_size=self.cover_byte_size,
        )


def normalize_song_record(song, default_cover: Path = DEFAULT_COVER) -> SongCatalogRecord:
    cover = resolve_cover_path(getattr(song, "cover_path", None), default_cover)
    return SongCatalogRecord(
        id=getattr(song, "id", None),
        title=getattr(song, "title", None) or "Unknown Title",
        artist=getattr(song, "artist", None) or "Unknown Artist",
        genre=getattr(song, "genre", None) or "Unknown Genre",
        duration=getattr(song, "duration", None),
        file_path=getattr(song, "file_path", None) or "",
        cover_path=str(cover),
        license_status=getattr(song, "license_status", "local") or "local",
        source_notes=getattr(song, "source_notes", "") or "",
        recommendation_reason=getattr(song, "recommendation_reason", "") or "",
        track_object_key=getattr(song, "track_object_key", "") or "",
        track_checksum_sha256=getattr(song, "track_checksum_sha256", "") or "",
        track_content_type=getattr(song, "track_content_type", "") or "",
        track_byte_size=getattr(song, "track_byte_size", None),
        cover_object_key=getattr(song, "cover_object_key", "") or "",
        cover_checksum_sha256=getattr(song, "cover_checksum_sha256", "") or "",
        cover_content_type=getattr(song, "cover_content_type", "") or "",
        cover_byte_size=getattr(song, "cover_byte_size", None),
    )


def normalize_cloud_song_record(
    row: Mapping[str, object],
    default_cover: Path = DEFAULT_COVER,
) -> SongCatalogRecord:
    track_asset = _asset_metadata(row.get("track_asset"))
    cover_asset = _asset_metadata(row.get("cover_asset"))
    related_assets = row.get("assets")
    if isinstance(related_assets, list):
        for asset in related_assets:
            if not isinstance(asset, Mapping):
                continue
            kind = str(asset.get("asset_kind") or "").strip().lower()
            object_key = str(asset.get("object_key") or "").strip().lower()
            if not track_asset and (
                kind in {"track", "music", "music_track", "audio"}
                or object_key.startswith("tracks/")
            ):
                track_asset = asset
            if not cover_asset and (
                kind in {"cover", "cover_art", "image"}
                or object_key.startswith("covers/")
            ):
                cover_asset = asset
    cover = resolve_cover_path(None, default_cover)
    duration = row.get("duration_seconds")
    if duration is None:
        duration = row.get("duration")
    return SongCatalogRecord(
        id=row.get("id"),
        title=str(row.get("title") or "Unknown Title"),
        artist=str(row.get("artist") or "Unknown Artist"),
        genre=str(row.get("genre") or "Unknown Genre"),
        duration=duration,
        file_path="",
        cover_path=str(cover),
        license_status=str(row.get("license_status") or "cloud"),
        source_notes=str(row.get("source_notes") or ""),
        track_object_key=str(track_asset.get("object_key") or ""),
        track_checksum_sha256=str(
            track_asset.get("checksum_sha256") or track_asset.get("sha256") or ""
        ),
        track_content_type=str(
            track_asset.get("content_type") or track_asset.get("mime_type") or ""
        ),
        track_byte_size=track_asset.get("byte_size"),
        cover_object_key=str(cover_asset.get("object_key") or ""),
        cover_checksum_sha256=str(
            cover_asset.get("checksum_sha256") or cover_asset.get("sha256") or ""
        ),
        cover_content_type=str(
            cover_asset.get("content_type") or cover_asset.get("mime_type") or ""
        ),
        cover_byte_size=cover_asset.get("byte_size"),
    )


def _asset_metadata(value: object) -> Mapping[str, object]:
    if isinstance(value, Mapping):
        return value
    if isinstance(value, list) and value and isinstance(value[0], Mapping):
        return value[0]
    return {}

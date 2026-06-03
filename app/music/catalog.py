from dataclasses import dataclass
from pathlib import Path
from types import SimpleNamespace
from typing import Optional

from app.config.runtime_assets import DEFAULT_COVER, resolve_cover_path


@dataclass(frozen=True)
class SongCatalogRecord:
    id: Optional[int]
    title: str
    artist: str
    genre: str
    duration: Optional[float]
    file_path: str
    cover_path: str
    license_status: str = "local"
    source_notes: str = ""
    recommendation_reason: str = ""

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
    )

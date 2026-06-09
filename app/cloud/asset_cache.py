"""Verified local cache for reproducible cloud assets."""

from __future__ import annotations

import hashlib
import os
import tempfile
from pathlib import Path
from typing import Callable, Optional, Union

from app.cloud.asset_api import CloudflareAssetClient


PathValue = Union[str, Path]
DownloadToFile = Callable[[str, Path], Path]


class AssetIntegrityError(ValueError):
    """Raised when a downloaded asset does not match its registered checksum."""


def default_asset_cache_root() -> Path:
    configured = os.getenv("MYRHYTHM_ASSET_CACHE_DIR", "").strip()
    if configured:
        return Path(configured).expanduser()

    local_app_data = os.getenv("LOCALAPPDATA", "").strip()
    if local_app_data:
        return Path(local_app_data) / "MyRhythm" / "asset-cache"

    xdg_cache_home = os.getenv("XDG_CACHE_HOME", "").strip()
    if xdg_cache_home:
        return Path(xdg_cache_home) / "myrhythm" / "asset-cache"

    return Path.home() / ".cache" / "myrhythm" / "asset-cache"


class AssetCache:
    def __init__(self, root: Optional[PathValue] = None):
        self.root = Path(root).expanduser() if root is not None else default_asset_cache_root()

    def get_music_asset(
        self,
        client: CloudflareAssetClient,
        object_key: str,
        sha256: str,
        expected_size: Optional[int] = None,
    ) -> Path:
        return self._get_asset(
            "music",
            object_key,
            sha256,
            client.download_music_asset,
            expected_size=expected_size,
        )

    def get_model_asset(
        self,
        client: CloudflareAssetClient,
        object_key: str,
        sha256: str,
        expected_size: Optional[int] = None,
    ) -> Path:
        return self._get_asset(
            "models",
            object_key,
            sha256,
            client.download_model_asset,
            expected_size=expected_size,
        )

    def _get_asset(
        self,
        asset_group: str,
        object_key: str,
        sha256: str,
        download_to_file: DownloadToFile,
        expected_size: Optional[int] = None,
    ) -> Path:
        key_parts = _safe_key_parts(object_key)
        checksum = _normalize_sha256(sha256)
        size = _normalize_expected_size(expected_size)
        target = self.root / asset_group / checksum / Path(*key_parts)
        target.parent.mkdir(parents=True, exist_ok=True)

        if (
            target.is_file()
            and (size is None or target.stat().st_size == size)
            and _file_sha256(target) == checksum
        ):
            return target
        if target.exists():
            target.unlink()

        file_descriptor, temporary_name = tempfile.mkstemp(
            prefix=f".{target.name}.",
            suffix=".tmp",
            dir=target.parent,
        )
        os.close(file_descriptor)
        temporary_path = Path(temporary_name)
        try:
            download_to_file(object_key, temporary_path)
            if size is not None and temporary_path.stat().st_size != size:
                raise AssetIntegrityError(
                    f"Downloaded asset failed byte size verification: {object_key}"
                )
            if _file_sha256(temporary_path) != checksum:
                raise AssetIntegrityError(
                    f"Downloaded asset failed SHA-256 verification: {object_key}"
                )
            os.replace(temporary_path, target)
            return target
        finally:
            temporary_path.unlink(missing_ok=True)


def _safe_key_parts(object_key: str) -> tuple[str, ...]:
    if not isinstance(object_key, str):
        raise ValueError("Invalid asset object key.")
    if object_key != object_key.strip() or not object_key:
        raise ValueError("Invalid asset object key.")
    if object_key.startswith("/") or "\\" in object_key or ":" in object_key:
        raise ValueError("Invalid asset object key.")

    parts = tuple(object_key.split("/"))
    if any(
        not part
        or part in {".", ".."}
        or any(ord(character) < 32 for character in part)
        for part in parts
    ):
        raise ValueError("Invalid asset object key.")
    return parts


def _normalize_sha256(value: str) -> str:
    checksum = str(value or "").strip().lower()
    if len(checksum) != 64 or any(character not in "0123456789abcdef" for character in checksum):
        raise ValueError("Invalid SHA-256 checksum.")
    return checksum


def _normalize_expected_size(value: Optional[int]) -> Optional[int]:
    if value is None:
        return None
    try:
        size = int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError("Invalid expected asset byte size.") from exc
    if size < 0:
        raise ValueError("Invalid expected asset byte size.")
    return size


def _file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        while True:
            chunk = source.read(1024 * 1024)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()

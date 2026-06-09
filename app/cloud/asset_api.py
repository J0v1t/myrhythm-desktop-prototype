"""Cloudflare Worker client for authenticated MyRhythm R2 assets."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Mapping, Union
from urllib import error as urlerror
from urllib import parse, request

from app.auth.supabase_auth import AuthUser, REQUEST_TIMEOUT_SECONDS


DEFAULT_ASSET_API_BASE_URL = "https://myrhythm-assets-api.zctrl7801.workers.dev"
DEFAULT_MAX_ASSET_BYTES = 64 * 1024 * 1024


@dataclass(frozen=True)
class AssetResponse:
    content: bytes
    content_type: str


AssetRequest = Callable[[str, Mapping[str, str], int], AssetResponse]
AssetDownload = Callable[[str, Mapping[str, str], Path, int], Path]


def load_asset_api_base_url() -> str:
    return os.getenv("MYRHYTHM_ASSET_API_BASE_URL", DEFAULT_ASSET_API_BASE_URL).strip()


def _request_asset(url: str, headers: Mapping[str, str], timeout: int) -> AssetResponse:
    req = request.Request(url, headers=dict(headers), method="GET")
    try:
        with request.urlopen(req, timeout=timeout) as response:
            return AssetResponse(
                content=response.read(),
                content_type=response.headers.get("Content-Type", "application/octet-stream"),
            )
    except urlerror.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        if exc.code == 429:
            raise RuntimeError("Too many asset requests. Please wait and try again.") from exc
        if exc.code == 403:
            raise RuntimeError("This asset is not available to your account.") from exc
        raise RuntimeError(body or str(exc)) from exc
    except urlerror.URLError as exc:
        raise RuntimeError("Could not reach the MyRhythm asset API.") from exc


def _download_asset(
    url: str,
    headers: Mapping[str, str],
    destination: Union[str, Path],
    timeout: int,
    max_bytes: int = DEFAULT_MAX_ASSET_BYTES,
) -> Path:
    destination_path = Path(destination)
    destination_path.parent.mkdir(parents=True, exist_ok=True)
    req = request.Request(url, headers=dict(headers), method="GET")
    try:
        with request.urlopen(req, timeout=timeout) as response:
            content_length = response.headers.get("Content-Length")
            if content_length and int(content_length) > max_bytes:
                raise RuntimeError("Asset exceeds the maximum allowed size.")
            bytes_written = 0
            with destination_path.open("wb") as output:
                while True:
                    chunk = response.read(1024 * 1024)
                    if not chunk:
                        break
                    bytes_written += len(chunk)
                    if bytes_written > max_bytes:
                        raise RuntimeError("Asset exceeds the maximum allowed size.")
                    output.write(chunk)
    except urlerror.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        if exc.code == 429:
            raise RuntimeError("Too many asset requests. Please wait and try again.") from exc
        if exc.code == 403:
            raise RuntimeError("This asset is not available to your account.") from exc
        raise RuntimeError(body or str(exc)) from exc
    except urlerror.URLError as exc:
        raise RuntimeError("Could not reach the MyRhythm asset API.") from exc
    except (RuntimeError, TypeError, ValueError):
        destination_path.unlink(missing_ok=True)
        raise
    return destination_path


class CloudflareAssetClient:
    def __init__(
        self,
        base_url: str,
        access_token: str,
        request_asset: AssetRequest = _request_asset,
        timeout: int = REQUEST_TIMEOUT_SECONDS,
        download_asset: AssetDownload = _download_asset,
    ):
        self.base_url = base_url.rstrip("/")
        self.access_token = access_token.strip()
        self._request_asset = request_asset
        self._download_asset = download_asset
        self.timeout = timeout

    @classmethod
    def from_auth_user(cls, user: AuthUser) -> "CloudflareAssetClient":
        if not user.access_token:
            raise ValueError("A Supabase access token is required for cloud asset access.")
        return cls(load_asset_api_base_url(), user.access_token)

    def fetch_music_asset(self, object_key: str) -> AssetResponse:
        return self._fetch("music", object_key)

    def fetch_model_asset(self, object_key: str) -> AssetResponse:
        return self._fetch("models", object_key)

    def download_music_asset(
        self,
        object_key: str,
        destination: Union[str, Path],
    ) -> Path:
        return self._download("music", object_key, destination)

    def download_model_asset(
        self,
        object_key: str,
        destination: Union[str, Path],
    ) -> Path:
        return self._download("models", object_key, destination)

    def music_asset_url(self, object_key: str) -> str:
        return self._asset_url("music", object_key)

    def model_asset_url(self, object_key: str) -> str:
        return self._asset_url("models", object_key)

    def _fetch(self, asset_group: str, object_key: str) -> AssetResponse:
        return self._request_asset(
            self._asset_url(asset_group, object_key),
            self._headers(),
            self.timeout,
        )

    def _download(
        self,
        asset_group: str,
        object_key: str,
        destination: Union[str, Path],
    ) -> Path:
        return self._download_asset(
            self._asset_url(asset_group, object_key),
            self._headers(),
            Path(destination),
            self.timeout,
        )

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.access_token}",
            "User-Agent": "MyRhythmDesktop/1.0",
        }

    def _asset_url(self, asset_group: str, object_key: str) -> str:
        key = object_key.strip()
        if not key or key.startswith("/") or ".." in key:
            raise ValueError("Invalid asset object key.")
        return f"{self.base_url}/assets/{asset_group}/{parse.quote(key, safe='/')}"

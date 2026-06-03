"""Cloudflare Worker client for authenticated MyRhythm R2 assets."""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Callable, Mapping
from urllib import error as urlerror
from urllib import parse, request

from app.auth.supabase_auth import AuthUser, REQUEST_TIMEOUT_SECONDS


DEFAULT_ASSET_API_BASE_URL = "https://myrhythm-assets-api.zctrl7801.workers.dev"


@dataclass(frozen=True)
class AssetResponse:
    content: bytes
    content_type: str


AssetRequest = Callable[[str, Mapping[str, str], int], AssetResponse]


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


class CloudflareAssetClient:
    def __init__(
        self,
        base_url: str,
        access_token: str,
        request_asset: AssetRequest = _request_asset,
        timeout: int = REQUEST_TIMEOUT_SECONDS,
    ):
        self.base_url = base_url.rstrip("/")
        self.access_token = access_token.strip()
        self._request_asset = request_asset
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

    def music_asset_url(self, object_key: str) -> str:
        return self._asset_url("music", object_key)

    def model_asset_url(self, object_key: str) -> str:
        return self._asset_url("models", object_key)

    def _fetch(self, asset_group: str, object_key: str) -> AssetResponse:
        return self._request_asset(
            self._asset_url(asset_group, object_key),
            {
                "Authorization": f"Bearer {self.access_token}",
                "User-Agent": "MyRhythmDesktop/1.0",
            },
            self.timeout,
        )

    def _asset_url(self, asset_group: str, object_key: str) -> str:
        key = object_key.strip()
        if not key or key.startswith("/") or ".." in key:
            raise ValueError("Invalid asset object key.")
        return f"{self.base_url}/assets/{asset_group}/{parse.quote(key, safe='/')}"

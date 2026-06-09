"""Authenticated Supabase Data API adapter for user-owned app data."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Callable, Mapping, Optional
from urllib import error as urlerror
from urllib import parse, request

from app.auth.supabase_auth import (
    AuthUser,
    REQUEST_TIMEOUT_SECONDS,
    load_supabase_config,
    normalize_supabase_project_url,
)
from app.music.catalog import SongCatalogRecord, normalize_cloud_song_record


JsonRequest = Callable[
    [str, str, Mapping[str, str], Optional[Mapping[str, object]], int],
    object,
]


@dataclass(frozen=True)
class ModelArtifactRecord:
    id: object
    artifact_type: str
    version: str
    object_key: str
    checksum_sha256: str
    content_type: str = ""
    byte_size: Optional[int] = None
    framework: str = ""
    runtime_version: str = ""
    compatibility: Optional[Mapping[str, object]] = None


def _rest_base_url(project_url: str) -> str:
    return f"{normalize_supabase_project_url(project_url)}/rest/v1"


def _request_json(
    method: str,
    url: str,
    headers: Mapping[str, str],
    payload: Optional[Mapping[str, object]],
    timeout: int,
) -> object:
    data = None
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")

    req = request.Request(url, data=data, headers=dict(headers), method=method)
    try:
        with request.urlopen(req, timeout=timeout) as response:
            body = response.read().decode("utf-8")
    except urlerror.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(body or str(exc)) from exc
    except urlerror.URLError as exc:
        raise RuntimeError("Could not reach Supabase Data API.") from exc

    if not body:
        return None
    return json.loads(body)


class SupabaseDataClient:
    def __init__(
        self,
        project_url: str,
        publishable_key: str,
        access_token: str,
        request_json: JsonRequest = _request_json,
        timeout: int = REQUEST_TIMEOUT_SECONDS,
    ):
        self.rest_url = _rest_base_url(project_url)
        self.publishable_key = publishable_key.strip()
        self.access_token = access_token.strip()
        self._request_json = request_json
        self.timeout = timeout

    @classmethod
    def from_auth_user(cls, user: AuthUser) -> "SupabaseDataClient":
        if not user.access_token:
            raise ValueError("A Supabase access token is required for cloud data access.")
        config = load_supabase_config()
        return cls(config.project_url, config.publishable_key, user.access_token)

    def get_user_preferences(self, user_id: str) -> dict:
        query = parse.urlencode(
            {
                "user_id": f"eq.{user_id}",
                "select": "user_id,favorite_genres,favorite_artists,mood_mapping",
            }
        )
        response = self._request_json(
            "GET",
            f"{self.rest_url}/user_preferences?{query}",
            self._headers(),
            None,
            self.timeout,
        )
        if not response:
            return {"genres": [], "artists": [], "mood_map": {}}
        row = response[0]
        return self._map_preferences(row)

    def save_user_preferences(
        self,
        user_id: str,
        genres: list[str],
        artists: list[str],
        mood_map: Optional[dict] = None,
    ) -> dict:
        payload = {
            "user_id": user_id,
            "favorite_genres": genres,
            "favorite_artists": artists,
            "mood_mapping": mood_map or {},
        }
        response = self._request_json(
            "POST",
            f"{self.rest_url}/user_preferences?on_conflict=user_id",
            {
                **self._headers(),
                "Prefer": "resolution=merge-duplicates,return=representation",
            },
            payload,
            self.timeout,
        )
        if not response:
            return self._map_preferences(payload)
        return self._map_preferences(response[0])

    def list_song_catalog(self) -> list[SongCatalogRecord]:
        query = parse.urlencode(
            {
                "is_active": "eq.true",
                "select": (
                    "*,"
                    "assets:asset_objects!asset_objects_song_id_fkey(*)"
                ),
                "order": "title.asc",
            }
        )
        response = self._request_json(
            "GET",
            f"{self.rest_url}/songs?{query}",
            self._headers(),
            None,
            self.timeout,
        )
        return [
            normalize_cloud_song_record(row)
            for row in (response or [])
            if isinstance(row, Mapping)
        ]

    def list_model_artifacts(self) -> list[ModelArtifactRecord]:
        query = parse.urlencode(
            {
                "status": "eq.active",
                "select": "*,asset:asset_objects!model_artifacts_asset_object_id_fkey(*)",
                "order": "model_type.asc,version.desc",
            }
        )
        response = self._request_json(
            "GET",
            f"{self.rest_url}/model_artifacts?{query}",
            self._headers(),
            None,
            self.timeout,
        )
        return [
            self._map_model_artifact(row)
            for row in (response or [])
            if isinstance(row, Mapping)
        ]

    @staticmethod
    def has_completed_preferences(preferences: Optional[Mapping[str, object]]) -> bool:
        if not preferences:
            return False
        return bool(preferences.get("genres")) and bool(preferences.get("artists"))

    def _headers(self) -> dict[str, str]:
        return {
            "apikey": self.publishable_key,
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

    @staticmethod
    def _map_preferences(row: Mapping[str, object]) -> dict:
        return {
            "genres": list(row.get("favorite_genres") or []),
            "artists": list(row.get("favorite_artists") or []),
            "mood_map": dict(row.get("mood_mapping") or {}),
        }

    @staticmethod
    def _map_model_artifact(row: Mapping[str, object]) -> ModelArtifactRecord:
        asset = row.get("asset")
        if isinstance(asset, list):
            asset = asset[0] if asset else {}
        if not isinstance(asset, Mapping):
            asset = {}
        compatibility = (
            row.get("metrics")
            or row.get("compatibility")
            or row.get("compatibility_metadata")
        )
        return ModelArtifactRecord(
            id=row.get("id"),
            artifact_type=str(row.get("model_type") or row.get("artifact_type") or ""),
            version=str(row.get("version") or ""),
            object_key=str(asset.get("object_key") or ""),
            checksum_sha256=str(
                asset.get("checksum_sha256") or asset.get("sha256") or ""
            ),
            content_type=str(asset.get("content_type") or asset.get("mime_type") or ""),
            byte_size=asset.get("byte_size"),
            framework=str(row.get("framework") or ""),
            runtime_version=str(row.get("runtime_version") or ""),
            compatibility=dict(compatibility) if isinstance(compatibility, Mapping) else {},
        )

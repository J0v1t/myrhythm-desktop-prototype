"""Authenticated Supabase Data API adapter for user-owned app data."""

from __future__ import annotations

import json
from typing import Callable, Mapping, Optional
from urllib import error as urlerror
from urllib import parse, request

from app.auth.supabase_auth import (
    AuthUser,
    REQUEST_TIMEOUT_SECONDS,
    load_supabase_config,
    normalize_supabase_project_url,
)


JsonRequest = Callable[
    [str, str, Mapping[str, str], Optional[Mapping[str, object]], int],
    object,
]


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

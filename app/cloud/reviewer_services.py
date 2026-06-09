"""Authenticated cloud services used by the signed-in reviewer experience."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

from app.cloud.asset_api import CloudflareAssetClient
from app.cloud.asset_cache import AssetCache
from app.cloud.model_provisioning import ModelProvisioningResult, provision_runtime_models
from app.cloud.supabase_data import SupabaseDataClient
from app.music.recommendation.recommendation_engine import RecommendationEngine


class ReviewerCloudServices:
    def __init__(
        self,
        user,
        data_client: SupabaseDataClient,
        asset_client: CloudflareAssetClient,
        asset_cache: AssetCache,
    ):
        self.user = user
        self.data_client = data_client
        self.asset_client = asset_client
        self.asset_cache = asset_cache
        self._catalog: Optional[list] = None
        self._preferences: Optional[dict] = None

    @classmethod
    def from_auth_user(cls, user) -> "ReviewerCloudServices":
        return cls(
            user=user,
            data_client=SupabaseDataClient.from_auth_user(user),
            asset_client=CloudflareAssetClient.from_auth_user(user),
            asset_cache=AssetCache(),
        )

    def load_catalog(self, force: bool = False) -> list:
        if self._catalog is None or force:
            records = self.data_client.list_song_catalog()
            self._catalog = []
            for record in records:
                if not (
                    getattr(record, "track_object_key", "")
                    and getattr(record, "track_checksum_sha256", "")
                ):
                    continue
                to_namespace = getattr(record, "to_simple_namespace", None)
                self._catalog.append(to_namespace() if callable(to_namespace) else record)
            if not self._catalog:
                raise RuntimeError(
                    "The cloud music catalog is unavailable for this account."
                )
        return self._catalog

    def list_artists(self, limit: int = 9) -> list[str]:
        artists = {
            str(song.artist).strip()
            for song in self.load_catalog()
            if str(getattr(song, "artist", "")).strip()
        }
        return sorted(artists, key=str.casefold)[:limit]

    def load_preferences(self, force: bool = False) -> dict:
        if self._preferences is None or force:
            self._preferences = self.data_client.get_user_preferences(self.user.id)
        return self._preferences

    def save_user_preferences(self, user_id, genres, artists, mood_map=None) -> dict:
        self._preferences = self.data_client.save_user_preferences(
            user_id,
            genres,
            artists,
            mood_map or {},
        )
        return self._preferences

    def prepare_track(self, song) -> Path:
        return self.asset_cache.get_music_asset(
            self.asset_client,
            song.track_object_key,
            song.track_checksum_sha256,
            expected_size=getattr(song, "track_byte_size", None),
        )

    def prepare_cover(self, song) -> Path:
        return self.asset_cache.get_music_asset(
            self.asset_client,
            song.cover_object_key,
            song.cover_checksum_sha256,
            expected_size=getattr(song, "cover_byte_size", None),
        )

    def recommendation_engine(self) -> RecommendationEngine:
        preferences = self.load_preferences()
        return RecommendationEngine(
            songs=self.load_catalog(),
            preferences={
                "favorite_genres": preferences.get("genres", []),
                "favorite_artists": preferences.get("artists", []),
            },
        )

    def provision_models(self) -> ModelProvisioningResult:
        result = provision_runtime_models(
            self.data_client.list_model_artifacts(),
            self.asset_cache,
            asset_client=self.asset_client,
        )
        os.environ.update(result.runtime_asset_overrides)
        return result

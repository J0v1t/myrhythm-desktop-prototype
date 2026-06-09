from pathlib import Path


MIGRATIONS = Path(__file__).resolve().parents[1] / "supabase" / "migrations"


def test_reviewer_asset_access_migration_versions_rls_and_rpc_contract():
    migrations = list(MIGRATIONS.glob("*_harden_reviewer_asset_access.sql"))

    assert len(migrations) == 1
    sql = migrations[0].read_text(encoding="utf-8").lower()

    for table in ("songs", "asset_objects", "model_artifacts", "user_preferences"):
        assert f"alter table public.{table} enable row level security" in sql

    assert "create or replace function public.authorize_asset_object_access" in sql
    assert "security definer" in sql
    assert "auth.uid()" in sql
    assert "revoke all on function public.authorize_asset_object_access" in sql
    assert "grant execute on function public.authorize_asset_object_access" in sql
    assert "to authenticated" in sql
    assert "revoke all on table public.songs from anon" in sql
    assert "grant select on table public.songs to authenticated" in sql
    assert (
        "grant select, insert, update on table public.user_preferences to authenticated"
        in sql
    )

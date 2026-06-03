from pathlib import Path


WORKER_ROOT = Path(__file__).resolve().parents[1] / "cloudflare" / "worker"


def test_worker_config_keeps_secrets_out_of_source():
    config = (WORKER_ROOT / "wrangler.toml").read_text(encoding="utf-8")

    assert "SUPABASE_URL" in config
    assert "SUPABASE_PUBLIC_KEY" not in config
    assert "service_role" not in config.lower()
    assert "secret" not in config.lower()


def test_worker_requires_supabase_session_before_r2_access():
    source = (WORKER_ROOT / "src" / "index.js").read_text(encoding="utf-8")

    assert "validateSupabaseToken" in source
    assert "/auth/v1/user" in source
    assert "MUSIC_ASSETS" in source
    assert "ML_MODELS" in source
    assert "missing_bearer_token" in source


def test_worker_rejects_malformed_object_keys():
    source = (WORKER_ROOT / "src" / "index.js").read_text(encoding="utf-8")

    assert "invalid_object_key" in source
    assert 'return json({ error: route.error }, 400, env)' in source
    assert "key.includes(\"..\")" in source

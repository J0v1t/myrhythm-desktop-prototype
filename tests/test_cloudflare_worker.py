from pathlib import Path


WORKER_ROOT = Path(__file__).resolve().parents[1] / "cloudflare" / "worker"


def test_worker_config_keeps_secrets_out_of_source():
    config = (WORKER_ROOT / "wrangler.toml").read_text(encoding="utf-8")

    assert "SUPABASE_URL" in config
    assert "ALLOW_MODEL_DOWNLOADS = \"true\"" in config
    assert "SUPABASE_PUBLIC_KEY" not in config
    assert "service_role" not in config.lower()
    assert "secret" not in config.lower()


def test_worker_config_declares_rate_limit_bindings():
    config = (WORKER_ROOT / "wrangler.toml").read_text(encoding="utf-8")

    assert "IP_RATE_LIMITER" in config
    assert "USER_ASSET_RATE_LIMITER" in config
    assert "USER_MODEL_RATE_LIMITER" in config
    assert config.count("[[ratelimits]]") == 3


def test_worker_config_enables_observability_and_size_caps():
    config = (WORKER_ROOT / "wrangler.toml").read_text(encoding="utf-8")

    assert "MAX_MUSIC_ASSET_BYTES" in config
    assert "MAX_MODEL_ASSET_BYTES" in config
    assert "[observability]" in config
    assert "enabled = true" in config
    assert "head_sampling_rate = 1" in config


def test_worker_requires_supabase_session_before_r2_access():
    source = (WORKER_ROOT / "src" / "index.js").read_text(encoding="utf-8")

    assert "validateSupabaseToken" in source
    assert "/auth/v1/user" in source
    assert "MUSIC_ASSETS" in source
    assert "ML_MODELS" in source
    assert "missing_bearer_token" in source


def test_worker_authorizes_assets_against_supabase_metadata():
    source = (WORKER_ROOT / "src" / "index.js").read_text(encoding="utf-8")

    assert "authorizeAssetAccess" in source
    assert "/rest/v1/rpc/authorize_asset_object_access" in source
    assert "asset_forbidden" in source
    assert "model_downloads_disabled" in source


def test_worker_rejects_malformed_object_keys():
    source = (WORKER_ROOT / "src" / "index.js").read_text(encoding="utf-8")

    assert "invalid_object_key" in source
    assert 'return json({ error: route.error }, 400, env)' in source
    assert "key.includes(\"..\")" in source


def test_worker_returns_429_when_rate_limited():
    source = (WORKER_ROOT / "src" / "index.js").read_text(encoding="utf-8")

    assert "rateLimited(env)" in source
    assert "Retry-After" in source
    assert "status: 429" in source


def test_worker_fails_closed_when_a_rate_limiter_binding_is_missing():
    source = (WORKER_ROOT / "src" / "index.js").read_text(encoding="utf-8")

    assert "rate_limiter_unavailable" in source
    assert "if (!limiter)" in source
    assert "success: true" not in source


def test_worker_rejects_oversized_objects_before_streaming():
    source = (WORKER_ROOT / "src" / "index.js").read_text(encoding="utf-8")

    assert "asset_too_large" in source
    assert "MAX_MUSIC_ASSET_BYTES" in source
    assert "MAX_MODEL_ASSET_BYTES" in source
    assert "status: 413" in source

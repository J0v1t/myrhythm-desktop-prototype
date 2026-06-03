import json

import pytest

from app.auth.supabase_auth import (
    AuthUser,
    SupabaseAuthClient,
    load_supabase_config,
    normalize_supabase_project_url,
)


def test_normalize_supabase_project_url_accepts_rest_endpoint():
    url = "https://yyjlkqvrjabcuuugpvyg.supabase.co/rest/v1/"

    assert normalize_supabase_project_url(url) == "https://yyjlkqvrjabcuuugpvyg.supabase.co"


def test_load_supabase_config_reads_project_url_and_publishable_key():
    env = {
        "SUPABASE_URL": "https://example.supabase.co/rest/v1/",
        "SUPABASE_PUBLIC_KEY": "sb_publishable_test",
    }

    config = load_supabase_config(env)

    assert config.project_url == "https://example.supabase.co"
    assert config.publishable_key == "sb_publishable_test"


def test_signup_posts_to_supabase_auth_with_user_metadata():
    calls = []

    def fake_post(url, headers, payload, timeout):
        calls.append((url, headers, payload, timeout))
        return {
            "user": {
                "id": "user-123",
                "email": "new@example.com",
                "user_metadata": {"name": "New Listener"},
            },
            "session": None,
        }

    client = SupabaseAuthClient(
        "https://example.supabase.co",
        "sb_publishable_test",
        post_json=fake_post,
    )

    result = client.sign_up("New Listener", "new@example.com", "secret123")

    assert result.success is True
    assert result.user == AuthUser(
        user_id="user-123",
        email="new@example.com",
        name="New Listener",
        access_token=None,
        refresh_token=None,
    )
    assert result.prefill_email == "new@example.com"
    assert "Account created" in result.message
    assert calls == [
        (
            "https://example.supabase.co/auth/v1/signup",
            {
                "apikey": "sb_publishable_test",
                "Authorization": "Bearer sb_publishable_test",
                "Content-Type": "application/json",
            },
            {
                "email": "new@example.com",
                "password": "secret123",
                "data": {"name": "New Listener"},
            },
            15,
        )
    ]


def test_signin_posts_password_grant_and_returns_session_user():
    def fake_post(url, headers, payload, timeout):
        return {
            "access_token": "access",
            "refresh_token": "refresh",
            "user": {
                "id": "user-123",
                "email": "new@example.com",
                "user_metadata": {"name": "New Listener"},
            },
        }

    client = SupabaseAuthClient(
        "https://example.supabase.co",
        "sb_publishable_test",
        post_json=fake_post,
    )

    result = client.sign_in("new@example.com", "secret123")

    assert result.success is True
    assert result.user == AuthUser(
        user_id="user-123",
        email="new@example.com",
        name="New Listener",
        access_token="access",
        refresh_token="refresh",
    )


def test_signin_maps_supabase_errors_to_user_safe_message():
    def fake_post(url, headers, payload, timeout):
        raise RuntimeError(json.dumps({"message": "Invalid login credentials"}))

    client = SupabaseAuthClient(
        "https://example.supabase.co",
        "sb_publishable_test",
        post_json=fake_post,
    )

    result = client.sign_in("new@example.com", "wrong-password")

    assert result.success is False
    assert result.message == "Invalid email or password."


def test_signup_maps_email_rate_limit_to_actionable_message():
    def fake_post(url, headers, payload, timeout):
        raise RuntimeError(
            json.dumps(
                {
                    "code": 429,
                    "error_code": "over_email_send_rate_limit",
                    "msg": "email rate limit exceeded",
                }
            )
        )

    client = SupabaseAuthClient(
        "https://example.supabase.co",
        "sb_publishable_test",
        post_json=fake_post,
    )

    result = client.sign_up("New Listener", "new@example.com", "secret123")

    assert result.success is False
    assert result.message == (
        "Supabase has temporarily paused confirmation emails. "
        "Please wait before creating another account."
    )


def test_signup_maps_invalid_email_to_actionable_message():
    def fake_post(url, headers, payload, timeout):
        raise RuntimeError(
            json.dumps(
                {
                    "code": 400,
                    "error_code": "email_address_invalid",
                    "msg": "Unable to validate email address: invalid format",
                }
            )
        )

    client = SupabaseAuthClient(
        "https://example.supabase.co",
        "sb_publishable_test",
        post_json=fake_post,
    )

    result = client.sign_up("New Listener", "new@example.com", "secret123")

    assert result.success is False
    assert result.message == "Enter a real email address that can receive confirmation email."

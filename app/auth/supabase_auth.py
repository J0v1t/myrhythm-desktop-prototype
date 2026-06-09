"""
Supabase Auth adapter for the desktop client.

Only the project URL and publishable key belong in this client. Service-role
keys, object-storage secrets, and database passwords must stay server-side.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
import os
from pathlib import Path
from typing import Callable, Mapping, Optional
from urllib import error as urlerror
from urllib import request


DEFAULT_SUPABASE_URL = "https://yyjlkqvrjabcuuugpvyg.supabase.co"
DEFAULT_SUPABASE_PUBLIC_KEY = "sb_publishable_7iqov_85_d7Xn1aRs09EOg_PrZTNJYi"
REQUEST_TIMEOUT_SECONDS = 15


@dataclass(frozen=True)
class SupabaseConfig:
    project_url: str
    publishable_key: str


@dataclass(frozen=True)
class AuthUser:
    user_id: str
    email: str
    name: Optional[str] = None
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None

    @property
    def id(self) -> str:
        return self.user_id


@dataclass(frozen=True)
class AuthResult:
    success: bool
    message: str
    user: Optional[AuthUser] = None
    prefill_email: Optional[str] = None


JsonPost = Callable[[str, Mapping[str, str], Mapping[str, object], int], Mapping[str, object]]


def normalize_supabase_project_url(url: str) -> str:
    cleaned = (url or "").strip().rstrip("/")
    for suffix in ("/rest/v1", "/auth/v1"):
        if cleaned.endswith(suffix):
            cleaned = cleaned[: -len(suffix)]
    return cleaned.rstrip("/")


def _load_dotenv_values(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}

    values: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def load_supabase_config(env: Optional[Mapping[str, str]] = None) -> SupabaseConfig:
    environ = env if env is not None else os.environ
    project_root = Path(__file__).resolve().parents[2]
    dotenv = {} if env is not None else _load_dotenv_values(project_root / ".env")

    raw_url = (
        environ.get("SUPABASE_URL")
        or environ.get("MYRHYTHM_SUPABASE_URL")
        or dotenv.get("SUPABASE_URL")
        or dotenv.get("MYRHYTHM_SUPABASE_URL")
        or DEFAULT_SUPABASE_URL
    )
    publishable_key = (
        environ.get("SUPABASE_PUBLIC_KEY")
        or environ.get("SUPABASE_PUBLISHABLE_KEY")
        or environ.get("MYRHYTHM_SUPABASE_PUBLIC_KEY")
        or dotenv.get("SUPABASE_PUBLIC_KEY")
        or dotenv.get("SUPABASE_PUBLISHABLE_KEY")
        or dotenv.get("MYRHYTHM_SUPABASE_PUBLIC_KEY")
        or DEFAULT_SUPABASE_PUBLIC_KEY
    ).strip()

    project_url = normalize_supabase_project_url(raw_url)
    if not project_url or not publishable_key:
        raise ValueError("Supabase URL and publishable key are required.")

    return SupabaseConfig(project_url=project_url, publishable_key=publishable_key)


def _post_json(
    url: str,
    headers: Mapping[str, str],
    payload: Mapping[str, object],
    timeout: int,
) -> Mapping[str, object]:
    body = json.dumps(payload).encode("utf-8")
    req = request.Request(url, data=body, headers=dict(headers), method="POST")
    try:
        with request.urlopen(req, timeout=timeout) as response:
            response_body = response.read().decode("utf-8")
    except urlerror.HTTPError as exc:
        response_body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(response_body or str(exc)) from exc
    except urlerror.URLError as exc:
        raise RuntimeError("Could not reach Supabase Auth. Check your internet connection.") from exc

    if not response_body:
        return {}
    return json.loads(response_body)


class SupabaseAuthClient:
    def __init__(
        self,
        project_url: str,
        publishable_key: str,
        post_json: JsonPost = _post_json,
        timeout: int = REQUEST_TIMEOUT_SECONDS,
    ):
        self.project_url = normalize_supabase_project_url(project_url)
        self.publishable_key = publishable_key.strip()
        self._post_json = post_json
        self.timeout = timeout

    @classmethod
    def from_env(cls) -> "SupabaseAuthClient":
        config = load_supabase_config()
        return cls(config.project_url, config.publishable_key)

    def sign_up(self, name: str, email: str, password: str) -> AuthResult:
        normalized_email = email.strip().lower()
        try:
            response = self._post_json(
                f"{self.project_url}/auth/v1/signup",
                self._headers(),
                {
                    "email": normalized_email,
                    "password": password,
                    "data": {"name": name.strip()},
                },
                self.timeout,
            )
        except RuntimeError as exc:
            return AuthResult(False, _safe_error_message(str(exc), signup=True))

        user = _build_auth_user(response, fallback_email=normalized_email)
        message = "Account created. Check your inbox to confirm your email, then sign in."
        if response.get("session"):
            message = "Account created. You can now sign in with your new credentials."
        return AuthResult(True, message, user=user, prefill_email=normalized_email)

    def sign_in(self, email: str, password: str) -> AuthResult:
        normalized_email = email.strip().lower()
        try:
            response = self._post_json(
                f"{self.project_url}/auth/v1/token?grant_type=password",
                self._headers(),
                {"email": normalized_email, "password": password},
                self.timeout,
            )
        except RuntimeError as exc:
            return AuthResult(False, _safe_error_message(str(exc), signup=False))

        user = _build_auth_user(response, fallback_email=normalized_email)
        if user is None or not user.access_token:
            return AuthResult(False, "Invalid email or password.")
        return AuthResult(True, "Signed in successfully.", user=user)

    def _headers(self) -> dict[str, str]:
        return {
            "apikey": self.publishable_key,
            "Authorization": f"Bearer {self.publishable_key}",
            "Content-Type": "application/json",
        }


def _build_auth_user(
    response: Mapping[str, object],
    fallback_email: str,
) -> Optional[AuthUser]:
    user_data = response.get("user")
    if not isinstance(user_data, Mapping):
        return None

    metadata = user_data.get("user_metadata")
    if not isinstance(metadata, Mapping):
        metadata = {}

    user_id = str(user_data.get("id") or "")
    if not user_id:
        return None

    session = response.get("session")
    if not isinstance(session, Mapping):
        session = response

    return AuthUser(
        user_id=user_id,
        email=str(user_data.get("email") or fallback_email),
        name=metadata.get("name") if isinstance(metadata.get("name"), str) else None,
        access_token=session.get("access_token") if isinstance(session.get("access_token"), str) else None,
        refresh_token=session.get("refresh_token") if isinstance(session.get("refresh_token"), str) else None,
    )


def _safe_error_message(raw_error: str, signup: bool) -> str:
    lowered = raw_error.lower()
    if "over_email_send_rate_limit" in lowered or "email rate limit" in lowered:
        return (
            "Supabase has temporarily paused confirmation emails. "
            "Please wait before creating another account."
        )
    if "email_address_invalid" in lowered or "unable to validate email address" in lowered:
        return "Enter a real email address that can receive confirmation email."
    if "invalid login credentials" in lowered:
        return "Invalid email or password."
    if "already registered" in lowered or "already exists" in lowered or "user exists" in lowered:
        return "An account with this email already exists. Sign in instead."
    if "password" in lowered and ("weak" in lowered or "six" in lowered or "6" in lowered):
        return "Use a stronger password with at least 6 characters."
    if "network" in lowered or "could not reach" in lowered or "connection" in lowered:
        return "Could not reach Supabase Auth. Check your internet connection."
    if signup:
        return "Could not create the account. Please check the details and try again."
    return "Could not sign in. Please try again."

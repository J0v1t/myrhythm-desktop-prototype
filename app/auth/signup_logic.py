"""Signup logic for the desktop application."""

from app.auth.supabase_auth import SupabaseAuthClient


def register_user(name, email, password, auth_client=None):
    """
    Register a new user with Supabase email/password auth.

    Args:
        name (str): User's name
        email (str): User's email
        password (str): User's password
        auth_client: Optional SupabaseAuthClient-compatible adapter

    Returns:
        tuple: (success: bool, message: str)
               - On success: (True, success_message)
               - On failure: (False, error_message)
    """
    try:
        client = auth_client or SupabaseAuthClient.from_env()
        result = client.sign_up(name, email, password)
        return result.success, result.message
    except Exception as e:
        return False, f"Registration error: {str(e)}"

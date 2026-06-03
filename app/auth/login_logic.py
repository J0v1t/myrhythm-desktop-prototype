"""Login logic for the desktop application."""

from app.auth.supabase_auth import SupabaseAuthClient


def authenticate_user(email, password, auth_client=None):
    """
    Authenticate a user with Supabase email/password auth.

    Args:
        email (str): User's email
        password (str): User's password
        auth_client: Optional SupabaseAuthClient-compatible adapter

    Returns:
        tuple: (success: bool, message: str or user object)
               - On success: (True, user_object)
               - On failure: (False, error_message)
    """
    try:
        client = auth_client or SupabaseAuthClient.from_env()
        result = client.sign_in(email, password)
        if result.success:
            return True, result.user
        return False, result.message
    except Exception as e:
        return False, f"Authentication error: {str(e)}"

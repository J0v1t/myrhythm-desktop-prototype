"""
Login logic for the desktop application.
"""

from app.database.models.user import User
from app.database.schema import db


def authenticate_user(email, password):
    """
    Authenticate a user with email and password.

    Args:
        email (str): User's email
        password (str): User's password

    Returns:
        tuple: (success: bool, message: str or user object)
               - On success: (True, user_object)
               - On failure: (False, error_message)
    """
    try:
        user = db.query(User).filter_by(email=email).first()
        if not user or not user.check_password(password):
            return False, "Invalid email or password"
        return True, user
    except Exception as e:
        return False, f"Authentication error: {str(e)}"

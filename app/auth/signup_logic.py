"""
Signup logic for the desktop application.
"""

from app.database.models.user import User
from app.database.schema import db


def register_user(name, email, password):
    """
    Register a new user.

    Args:
        name (str): User's name
        email (str): User's email
        password (str): User's password

    Returns:
        tuple: (success: bool, message: str)
               - On success: (True, "User registered successfully!")
               - On failure: (False, error_message)
    """
    try:
        existing_user = db.query(User).filter_by(email=email).first()
        if existing_user:
            return False, "Email already registered."

        new_user = User(name=name, email=email)
        new_user.set_password(password)

        db.add(new_user)
        db.commit()

        return True, "User registered successfully!"
    except Exception as e:
        db.rollback()
        return False, f"Registration error: {str(e)}"

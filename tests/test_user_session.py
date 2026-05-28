import pytest
from app.logic.user_session import set_active_user, get_active_user_id, clear_active_user

class TestUserSession:
    def test_set_active_user(self):
        set_active_user(1, "testuser")
        assert get_active_user_id() == 1

    def test_clear_active_user(self):
        set_active_user(1, "testuser")
        clear_active_user()
        assert get_active_user_id() is None

    def test_get_active_user_id_no_user(self):
        clear_active_user()
        assert get_active_user_id() is None

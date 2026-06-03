import os
import sys

import pytest

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

QtWidgets = pytest.importorskip("PyQt5.QtWidgets")

from app.gui.login_window import LoginWindow
from app.gui.preferences_window import PreferencesWindow
from app.gui.signup_window import SignupWindow


@pytest.fixture(scope="module")
def qapp():
    app = QtWidgets.QApplication.instance() or QtWidgets.QApplication(sys.argv)
    yield app


def test_login_window_prefills_email(qapp):
    window = LoginWindow(prefill_email="created@example.com")

    assert window.ui.lineEdit_7.text() == "created@example.com"


def test_signup_success_opens_signin_with_created_email(qapp, monkeypatch):
    opened_with = []

    class FakeLoginWindow(QtWidgets.QDialog):
        def __init__(self, prefill_email=None):
            super().__init__()
            opened_with.append(prefill_email)
            self.user = None

        def exec_(self):
            return QtWidgets.QDialog.Rejected

    window = SignupWindow(
        register_func=lambda name, email, password: (
            True,
            "Account created. Check your inbox to confirm your email, then sign in.",
        ),
        login_window_cls=FakeLoginWindow,
    )
    monkeypatch.setattr(
        "app.gui.signup_window.QMessageBox.information",
        lambda *args, **kwargs: None,
    )

    window.ui.lineEdit.setText("Created User")
    window.ui.lineEdit_3.setText("created@example.com")
    window.ui.lineEdit_4.setText("secret123")
    window.signup()

    assert opened_with == ["created@example.com"]


def test_preferences_window_uses_injected_cloud_save_function(qapp):
    calls = []

    class FakeUser:
        id = "user-123"

    window = PreferencesWindow(
        FakeUser(),
        save_preferences_func=lambda user_id, genres, artists, mood_map: calls.append(
            (user_id, genres, artists, mood_map)
        ),
    )
    window.selected_genres = ["ROCK"]
    window.selected_artists = ["ARTIST A"]

    window.save_preferences()

    assert calls == [("user-123", ["ROCK"], ["ARTIST A"], {})]

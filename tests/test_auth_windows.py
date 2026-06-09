import os
import sys

import pytest

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

QtWidgets = pytest.importorskip("PyQt5.QtWidgets")

from app.gui.login_window import LoginWindow
from app.gui.preferences_window import PreferencesWindow
from app.gui.signup_window import SignupWindow

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


@pytest.fixture(scope="module")
def qapp():
    app = QtWidgets.QApplication.instance() or QtWidgets.QApplication(sys.argv)
    yield app


def test_login_window_prefills_email(qapp):
    window = LoginWindow(prefill_email="created@example.com")

    assert window.ui.lineEdit_7.text() == "created@example.com"


def test_auth_windows_use_original_hero_with_visible_logo(qapp):
    login = LoginWindow()
    signup = SignupWindow()

    assert os.path.isfile(os.path.join(PROJECT_ROOT, "media", "auth_hero.jpg"))
    assert not login.ui.label_19.isHidden()
    assert not signup.ui.label_9.isHidden()


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


def test_preferences_window_opens_dashboard_with_cloud_services(qapp):
    opened_with = []

    class FakeUser:
        id = "user-123"

    class FakeDashboard:
        def show(self):
            opened_with.append("shown")

    cloud_services = object()
    window = PreferencesWindow(
        FakeUser(),
        save_preferences_func=lambda *args: None,
        dashboard_factory=lambda user_id, services: (
            opened_with.append((user_id, services)) or FakeDashboard()
        ),
        cloud_services=cloud_services,
    )

    window.go_to_dashboard2()

    assert opened_with == [("user-123", cloud_services), "shown"]


def test_preferences_window_uses_real_cloud_catalog_artists(qapp):
    class FakeUser:
        id = "user-123"

    class FakeCloudServices:
        def list_artists(self, limit=9):
            return ["Real Artist", "Another Artist"]

    window = PreferencesWindow(FakeUser(), cloud_services=FakeCloudServices())

    assert window.artists[:2] == ["Real Artist", "Another Artist"]
    assert window.artist_labels[0].text() == "Real Artist"
    assert window.artist_labels[1].text() == "Another Artist"
    assert window.ui2.label_15.text() == "Real Artist"
    assert window.ui2.label_16.text() == "Another Artist"
    assert window.artist_cards[0].isVisibleTo(window.widget2)
    assert window.artist_cards[1].isVisibleTo(window.widget2)
    assert not window.artist_cards[2].isVisibleTo(window.widget2)

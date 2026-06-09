from types import SimpleNamespace

from run import create_reviewer_window


class FakeServices:
    def __init__(self, preferences):
        self.preferences = preferences
        self.calls = []

    def load_catalog(self):
        self.calls.append("catalog")
        return [object()]

    def load_preferences(self):
        self.calls.append("preferences")
        return self.preferences

    def save_user_preferences(self, *args):
        self.calls.append(("save", args))


def test_create_reviewer_window_opens_cloud_dashboard_for_completed_preferences():
    services = FakeServices({"genres": ["POP"], "artists": ["Artist"]})
    opened = []

    window = create_reviewer_window(
        SimpleNamespace(id="user-1"),
        services,
        dashboard_factory=lambda user_id, cloud_services: (
            opened.append((user_id, cloud_services)) or object()
        ),
    )

    assert window is not None
    assert opened == [("user-1", services)]
    assert services.calls == ["catalog", "preferences"]


def test_create_reviewer_window_opens_cloud_preferences_for_new_user():
    services = FakeServices({"genres": [], "artists": []})
    opened = []

    window = create_reviewer_window(
        SimpleNamespace(id="user-1"),
        services,
        preferences_factory=lambda user, **kwargs: (
            opened.append((user, kwargs)) or object()
        ),
    )

    assert window is not None
    user, kwargs = opened[0]
    assert user.id == "user-1"
    assert kwargs["save_preferences_func"] == services.save_user_preferences
    assert kwargs["cloud_services"] is services

from pathlib import Path
from types import SimpleNamespace

import pytest
from PyQt5 import QtCore, QtWidgets

from app.gui.dashboard2 import DashboardWindow, HoverAccentFilter, Ui_Form
from app.gui.recognition import Recognition


class FakeCloudServices:
    def __init__(self, songs, tmp_path):
        self.songs = songs
        self.tmp_path = tmp_path
        self.prepared = []

    def load_catalog(self):
        return self.songs

    def prepare_cover(self, song):
        self.prepared.append(("cover", song.id))
        return self.tmp_path / "cover.webp"

    def prepare_track(self, song):
        self.prepared.append(("track", song.id))
        return self.tmp_path / "track.mp3"


@pytest.fixture(scope="module")
def qapp():
    return QtWidgets.QApplication.instance() or QtWidgets.QApplication([])


def test_dashboard_loads_cloud_catalog_without_sqlite(tmp_path):
    songs = [SimpleNamespace(id="song-1", title="Cloud Song")]
    services = FakeCloudServices(songs, tmp_path)
    dashboard = SimpleNamespace(cloud_services=services, playlist=[])

    DashboardWindow.load_playlist(dashboard)

    assert dashboard.playlist == songs


def test_dashboard_prepares_cloud_track_without_blocking_on_cover(tmp_path):
    song = SimpleNamespace(
        id="song-1",
        title="Cloud Song",
        file_path="",
        cover_path="",
        track_object_key="tracks/cloud-song.mp3",
        cover_object_key="covers/cloud-song.webp",
    )
    services = FakeCloudServices([song], tmp_path)
    dashboard = SimpleNamespace(cloud_services=services)

    prepared = DashboardWindow.prepare_song_for_playback(dashboard, song)

    assert prepared is song
    assert song.file_path == str(tmp_path / "track.mp3")
    assert song.cover_path == ""
    assert services.prepared == [("track", "song-1")]


def test_dashboard_uses_local_cover_without_fetching(tmp_path):
    cover = tmp_path / "cover.webp"
    cover.write_bytes(b"cover")
    song = SimpleNamespace(id="song-1", cover_path=str(cover), cover_object_key="covers/cloud.webp")
    services = FakeCloudServices([song], tmp_path)
    dashboard = SimpleNamespace(cloud_services=services)

    resolved = DashboardWindow.cover_path_for(dashboard, song, Path("fallback.png"))

    assert resolved == str(cover)
    assert services.prepared == []


def test_dashboard_uses_placeholder_until_cover_download_finishes(tmp_path):
    song = SimpleNamespace(
        id="song-1",
        cover_path="",
        cover_object_key="covers/cloud.webp",
    )
    services = FakeCloudServices([song], tmp_path)
    dashboard = SimpleNamespace(cloud_services=services)

    resolved = DashboardWindow.cover_path_for(dashboard, song, Path("fallback.png"))

    assert resolved == "fallback.png"
    assert services.prepared == []


def test_dashboard_queues_cloud_cover_when_placeholder_exists(tmp_path):
    media_path = tmp_path / "media"
    media_path.mkdir()
    placeholder = media_path / "default_cover.png"
    placeholder.write_bytes(b"placeholder")
    song = SimpleNamespace(
        id="song-1",
        cover_path=str(placeholder),
        cover_object_key="covers/cloud.webp",
        cover_checksum_sha256="b" * 64,
    )
    queued = []
    dashboard = SimpleNamespace(
        ui=SimpleNamespace(media_path=str(media_path)),
        cloud_services=FakeCloudServices([song], tmp_path),
        _queued_cover_ids=set(),
        _cover_thread_pool=SimpleNamespace(start=queued.append),
        cover_downloaded=lambda *args: None,
        cover_download_failed=lambda *args: None,
    )

    DashboardWindow.queue_cover_download(dashboard, song)

    assert len(queued) == 1
    assert "song-1" in dashboard._queued_cover_ids


def test_dashboard_applies_downloaded_cover_to_registered_widgets(tmp_path):
    cover = tmp_path / "cover.webp"
    cover.write_bytes(b"cover")
    song = SimpleNamespace(id="song-1", cover_path="")
    calls = []
    dashboard = SimpleNamespace(
        _cover_widgets={"song-1": ["widget-a", "widget-b"]},
        _queued_cover_ids={"song-1"},
        render_cover_widget=lambda widget, path: calls.append((widget, path)),
    )

    DashboardWindow.cover_downloaded(dashboard, song, str(cover))

    assert song.cover_path == str(cover)
    assert calls == [("widget-a", str(cover)), ("widget-b", str(cover))]


def test_dashboard_uses_existing_cached_track_without_refetching(tmp_path):
    track = tmp_path / "track.mp3"
    track.write_bytes(b"track")
    song = SimpleNamespace(
        id="song-1",
        file_path=str(track),
        cover_path="",
        track_object_key="tracks/cloud.mp3",
        cover_object_key="covers/cloud.webp",
    )
    services = FakeCloudServices([song], tmp_path)
    dashboard = SimpleNamespace(cloud_services=services)

    prepared = DashboardWindow.prepare_song_for_playback(dashboard, song)

    assert prepared.file_path == str(track)
    assert services.prepared == []


def test_dashboard_reports_track_preparation_failure_without_crashing(monkeypatch):
    messages = []
    dashboard = SimpleNamespace(
        prepare_song_for_playback=lambda song: (_ for _ in ()).throw(
            RuntimeError("download failed")
        )
    )
    monkeypatch.setattr(
        "app.gui.dashboard2.QtWidgets.QMessageBox.warning",
        lambda *args: messages.append(args[-1]),
    )

    result = DashboardWindow.load_song(
        dashboard,
        SimpleNamespace(title="Cloud Song"),
    )

    assert result is False
    assert "download failed" in messages[0]


def test_dashboard_recommended_song_preserves_cloud_asset_references():
    dashboard = SimpleNamespace(
        ui=SimpleNamespace(media_path="media"),
        recommended_playlist=[],
        playlist=[],
        current_index=0,
        play_current_song=lambda: None,
    )

    DashboardWindow.load_recommended_songs(
        dashboard,
        [
            {
                "song_id": "song-1",
                "title": "Cloud Song",
                "artist": "Cloud Artist",
                "genre": "pop",
                "track_object_key": "tracks/cloud.mp3",
                "track_checksum_sha256": "a" * 64,
                "track_byte_size": 2048,
                "cover_object_key": "covers/cloud.webp",
                "cover_checksum_sha256": "b" * 64,
                "cover_byte_size": 512,
            }
        ],
    )

    song = dashboard.playlist[0]
    assert song.track_object_key == "tracks/cloud.mp3"
    assert song.track_byte_size == 2048
    assert song.cover_object_key == "covers/cloud.webp"
    assert song.cover_byte_size == 512
    assert song.cover_path == ""


def test_up_next_hides_unused_rows_and_shrinks_card(qapp, tmp_path):
    form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(form)
    dashboard = SimpleNamespace(
        ui=ui,
        playlist=[
            SimpleNamespace(id="song-1", title="Playing", artist="Artist", cover_path=""),
            SimpleNamespace(id="song-2", title="Next", artist="Artist", cover_path=""),
        ],
        current_index=0,
        cover_path_for=lambda song, fallback: str(fallback),
        register_cover_widget=lambda song, widget: None,
        render_cover_widget=lambda widget, path: None,
        queue_cover_download=lambda song: None,
    )

    DashboardWindow.update_up_next(dashboard)

    assert not ui.pushButton_16.isHidden()
    assert ui.pushButton_17.isHidden()
    assert ui.label_58.isHidden()
    assert ui.label_59.isHidden()
    assert ui.widget_9.maximumHeight() < 220


def test_hover_filter_adds_and_removes_visual_accent(qapp):
    widget = QtWidgets.QPushButton()
    hover_filter = HoverAccentFilter(widget)
    widget.installEventFilter(hover_filter)

    QtWidgets.QApplication.sendEvent(widget, QtCore.QEvent(QtCore.QEvent.Enter))
    assert widget.graphicsEffect() is not None

    QtWidgets.QApplication.sendEvent(widget, QtCore.QEvent(QtCore.QEvent.Leave))
    assert widget.graphicsEffect() is None


def test_recognition_uses_injected_cloud_recommendation_engine():
    calls = []

    class FakeEngine:
        def recommend(self, **kwargs):
            calls.append(kwargs)
            return [{"song_id": "song-1"}]

    dashboard = SimpleNamespace(
        load_recommended_songs=lambda songs: calls.append(songs),
    )
    recognition = SimpleNamespace(
        user_id="user-123",
        dashboard=dashboard,
        recommendation_engine_factory=lambda: FakeEngine(),
        signal_session=SimpleNamespace(
            recommendation_inputs=lambda: {
                "fer_emotion": "happy",
                "hr_emotion": None,
                "combined_mode": False,
            }
        ),
    )

    Recognition.open_recommendations(recognition)

    assert calls[0]["user_id"] == "user-123"
    assert calls[1] == [{"song_id": "song-1"}]


def test_dashboard_provisions_models_only_when_recognition_opens(monkeypatch):
    calls = []

    class Services:
        def provision_models(self):
            calls.append("models")
            return SimpleNamespace(failures={})

        def recommendation_engine(self):
            return object()

    class FakeRecognition:
        def __init__(self, **kwargs):
            calls.append(kwargs)

        def show(self):
            calls.append("shown")

    monkeypatch.setattr("app.gui.dashboard2.Ui_Recognition", FakeRecognition)
    dashboard = SimpleNamespace(
        cloud_services=Services(),
        user_id="user-1",
    )

    DashboardWindow.open_recognition(dashboard)

    assert calls[0] == "models"
    assert calls[1]["user_id"] == "user-1"
    assert calls[2] == "shown"

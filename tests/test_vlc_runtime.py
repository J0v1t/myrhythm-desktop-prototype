import sys

from app.config.vlc_runtime import check_vlc_readiness


class FakeVlcInstance:
    def __init__(self):
        self.released = False

    def release(self):
        self.released = True


class ReadyVlc:
    def __init__(self):
        self.instance = FakeVlcInstance()

    def Instance(self, *options):
        assert options == ("--no-plugins-cache",)
        return self.instance


def test_vlc_readiness_checks_native_libvlc_without_importing_dashboard():
    sys.modules.pop("app.gui.dashboard2", None)
    vlc = ReadyVlc()

    readiness = check_vlc_readiness(vlc_module=vlc)

    assert readiness.ready is True
    assert readiness.message == "VLC playback is ready."
    assert readiness.error is None
    assert vlc.instance.released is True
    assert "app.gui.dashboard2" not in sys.modules


def test_vlc_readiness_reports_missing_python_binding_with_prerequisite():
    def missing_binding(_module_name):
        raise ModuleNotFoundError("No module named 'vlc'")

    readiness = check_vlc_readiness(import_module=missing_binding)

    assert readiness.ready is False
    assert "Install VLC media player" in readiness.message
    assert "native libVLC" in readiness.message
    assert "python-vlc" in readiness.error


def test_vlc_readiness_reports_missing_native_libvlc_with_prerequisite():
    class MissingNativeVlc:
        @staticmethod
        def Instance(*_options):
            raise OSError("no function 'libvlc_new'")

    readiness = check_vlc_readiness(vlc_module=MissingNativeVlc())

    assert readiness.ready is False
    assert "Install VLC media player" in readiness.message
    assert "native libVLC" in readiness.message
    assert "no function 'libvlc_new'" in readiness.error


def test_vlc_readiness_does_not_treat_cleanup_failure_as_missing_libvlc():
    class CleanupFailsInstance:
        @staticmethod
        def release():
            raise RuntimeError("cleanup failed")

    class ReadyVlcWithCleanupFailure:
        @staticmethod
        def Instance(*_options):
            return CleanupFailsInstance()

    readiness = check_vlc_readiness(vlc_module=ReadyVlcWithCleanupFailure())

    assert readiness.ready is True

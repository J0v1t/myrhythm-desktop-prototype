from PyQt5.QtCore import QThread, pyqtSignal
from .fer_inference import FERModel


class FERLoaderThread(QThread):
    loaded = pyqtSignal(object)
    status = pyqtSignal(str)
    error = pyqtSignal(str)

    def run(self):
        self.status.emit("Loading model")
        try:
            model = FERModel()   # heavy operation (30–60s)
        except FileNotFoundError as exc:
            self.status.emit("Model missing")
            self.error.emit(str(exc))
            return
        except Exception as exc:
            self.status.emit("Error")
            self.error.emit(str(exc))
            return

        self.loaded.emit(model)

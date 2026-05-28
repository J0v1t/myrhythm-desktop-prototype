from PyQt5.QtCore import QThread, pyqtSignal
from .fer_inference import FERModel


class FERLoaderThread(QThread):
    loaded = pyqtSignal(object)

    def run(self):
        model = FERModel()   # heavy operation (30–60s)
        self.loaded.emit(model)

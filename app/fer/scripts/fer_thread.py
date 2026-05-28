from PyQt5.QtCore import QThread, pyqtSignal


class FERInferenceThread(QThread):
    result_ready = pyqtSignal(object)  # (result)

    def __init__(self, fer_model):
        super().__init__()
        self.fer_model = fer_model
        self.frame = None
        self.running = True

    def run(self):
        while self.running:
            if self.frame is not None:
                frame_copy = self.frame.copy()
                result = self.fer_model.predict_emotion(frame_copy)
                self.result_ready.emit(result)
                self.frame = None  # avoid backlog
                self.msleep(1)

    def update_frame(self, frame):
        if self.frame is None:
            self.frame = frame
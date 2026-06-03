from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal
from collections import deque
import sys, os, cv2, asyncio

# --- Path Setup ---
current_dir = os.path.dirname(os.path.abspath(__file__))  # app/gui
project_root = os.path.dirname(os.path.dirname(current_dir))  # myrhythm/
sys.path.append(project_root)  # myrhythm/
sys.path.append(os.path.join(project_root, "app", "hr"))  # app/hr
sys.path.append(os.path.join(project_root, "app", "music", "recommendation"))  # app/music/recommendation
sys.path.append(os.path.join(project_root, "app", "gui"))  # app/gui

# --- FER Module Imports ---
try:
    from app.fer.scripts.camera_module import Camera
    from app.fer.scripts.model_loader import FERLoaderThread
    from app.fer.scripts.fer_thread import FERInferenceThread
except ImportError:
    print("Warning: FER Modules not found. FER features will not work.")

# --- HR Module Imports ---
try:
    from app.hr.scripts.ble_reader import read_heart_rate_live
    from app.hr.scripts.pipeline import predict_emotions_live, calculate_final_emotion_and_save
    from app.hr.trained_hr_models.classifier import load_model_components
except ImportError:
    print("Warning: HR Modules not found. HR features will not work.")

try:
    from app.music.recommendation.recommendation_engine import RecommendationEngine
    from app.gui.dashboard2 import DashboardWindow
except ImportError:
    print("Warning: Recommendation Modules not found. Recommendation features will not work.")

from app.emotion.signal_session import EmotionSignalSession


# -------------------------------------------------------------------------
# Main GUI Class
# -------------------------------------------------------------------------
class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1199, 834)
        Form.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        Form.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        base_path = os.path.dirname(__file__)  # app/gui/
        self.media_path = os.path.abspath(os.path.join(base_path, "..", "..", "media"))
        self.frame = QtWidgets.QFrame(Form)
        self.frame.setGeometry(QtCore.QRect(20, 20, 1161, 801))
        self.frame.setStyleSheet("background-color: rgb(30, 30, 30);\n"
"border-radius:20px;")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout.setContentsMargins(20, 20, 20, 22)
        self.verticalLayout.setSpacing(11)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(167, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans ExtraBold")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setStyleSheet("color: rgb(255, 255, 255);")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        spacerItem1 = QtWidgets.QSpacerItem(92, 0, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.pushButton = QtWidgets.QPushButton(self.frame)
        self.pushButton.setMaximumSize(QtCore.QSize(40, 40))
        self.pushButton.setStyleSheet("background-color: rgb(50, 50, 50);\n"
"border-radius:20px;")
        self.pushButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.media_path, "x.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton.setIcon(icon)
        self.pushButton.setIconSize(QtCore.QSize(25, 25))
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_2.addWidget(self.pushButton)
        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 1)
        self.horizontalLayout_2.setStretch(3, 1)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setContentsMargins(-1, -1, -1, 0)
        self.horizontalLayout_4.setSpacing(20)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.frame_2 = QtWidgets.QFrame(self.frame)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout_3.setContentsMargins(-1, -1, -1, 20)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setContentsMargins(-1, -1, 8, -1)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_5 = QtWidgets.QLabel(self.frame_2)
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans ExtraBold")
        font.setPointSize(15)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_6.addWidget(self.label_5)
        self.checkBox = QtWidgets.QCheckBox(self.frame_2)
        self.checkBox.setMinimumSize(QtCore.QSize(0, 0))
        self.checkBox.setMaximumSize(QtCore.QSize(50, 16777215))
        self.checkBox.setStyleSheet("QCheckBox {\n"
"    spacing: 5px;\n"
"}\n"
"\n"
"QCheckBox::indicator {\n"
"    width: 40px;\n"
"    height: 20px;\n"
"    border-radius: 10px; /* Makes it round (half of height) */\n"
"}\n"
"\n"
"/* The OFF state (Gray) */\n"
"QCheckBox::indicator:unchecked {\n"
"    background-color: #555555;\n"
"    border: 2px solid #555555;\n"
"    /* To add a circle knob, you usually need an image here, \n"
"       but we can simulate the \"track\" look with colors */\n"
"}\n"
"\n"
"/* The ON state (Green/Blue) */\n"
"QCheckBox::indicator:checked {\n"
"    background-color: #00b894; /* Green color */\n"
"    border: 2px solid #00b894;\n"
"}")
        self.checkBox.setText("Camera")
        self.checkBox.setObjectName("checkBox")
        self.checkBox.setChecked(False)
        self.horizontalLayout_6.addWidget(self.checkBox)
        self.verticalLayout_3.addLayout(self.horizontalLayout_6)
        self.label_6 = QtWidgets.QLabel(self.frame_2)
        self.label_6.setMinimumSize(QtCore.QSize(515, 315))
        self.label_6.setMaximumSize(QtCore.QSize(515, 315))
        self.label_6.setStyleSheet("background-color: rgb(50, 50, 50);\n"
"border-radius:15px;\n" "color: rgb(255, 255, 255);")
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setText("")
        self.label_6.setObjectName("label_6")
        self.verticalLayout_3.addWidget(self.label_6, 0, QtCore.Qt.AlignHCenter)
        self.verticalLayout_3.setStretch(0, 1)
        self.verticalLayout_3.setStretch(1, 2)
        self.horizontalLayout_4.addWidget(self.frame_2)
        self.frame_3 = QtWidgets.QFrame(self.frame)
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.frame_3)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setContentsMargins(-1, -1, 8, -1)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_13 = QtWidgets.QLabel(self.frame_3)
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans ExtraBold")
        font.setPointSize(15)
        self.label_13.setFont(font)
        self.label_13.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_13.setObjectName("label_13")
        self.horizontalLayout_7.addWidget(self.label_13)
        self.checkBox_2 = QtWidgets.QCheckBox(self.frame_3)
        self.checkBox_2.setMinimumSize(QtCore.QSize(0, 0))
        self.checkBox_2.setMaximumSize(QtCore.QSize(50, 16777215))
        self.checkBox_2.setStyleSheet("QCheckBox {\n"
"    spacing: 5px;\n"
"}\n"
"\n"
"QCheckBox::indicator {\n"
"    width: 40px;\n"
"    height: 20px;\n"
"    border-radius: 10px; /* Makes it round (half of height) */\n"
"}\n"
"\n"
"/* The OFF state (Gray) */\n"
"QCheckBox::indicator:unchecked {\n"
"    background-color: #555555;\n"
"    border: 2px solid #555555;\n"
"    /* To add a circle knob, you usually need an image here, \n"
"       but we can simulate the \"track\" look with colors */\n"
"}\n"
"\n"
"/* The ON state (Green/Blue) */\n"
"QCheckBox::indicator:checked {\n"
"    background-color: #00b894; /* Green color */\n"
"    border: 2px solid #00b894;\n"
"}")
        self.checkBox_2.setText("")
        self.checkBox_2.setObjectName("checkBox_2")
        self.horizontalLayout_7.addWidget(self.checkBox_2)
        self.verticalLayout_7.addLayout(self.horizontalLayout_7)
        self.label_14 = QtWidgets.QLabel(self.frame_3)
        self.label_14.setMaximumSize(QtCore.QSize(280, 16777215))
        self.label_14.setText("")
        self.label_14.setPixmap(QtGui.QPixmap(os.path.join(self.media_path, "normal.png")))
        self.label_14.setScaledContents(True)
        self.label_14.setObjectName("label_14")
        self.verticalLayout_7.addWidget(self.label_14, 0, QtCore.Qt.AlignHCenter)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_15 = QtWidgets.QLabel(self.frame_3)
        font = QtGui.QFont()
        font.setFamily("Noto Serif JP SemiBold")
        font.setPointSize(25)
        self.label_15.setFont(font)
        self.label_15.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_15.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_15.setObjectName("label_15")
        self.horizontalLayout_5.addWidget(self.label_15)
        self.label_16 = QtWidgets.QLabel(self.frame_3)
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans Medium")
        font.setPointSize(16)
        self.label_16.setFont(font)
        self.label_16.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_16.setObjectName("label_16")
        self.horizontalLayout_5.addWidget(self.label_16)
        self.verticalLayout_7.addLayout(self.horizontalLayout_5)
        self.verticalLayout_7.setStretch(1, 3)
        self.verticalLayout_7.setStretch(2, 1)
        self.horizontalLayout_4.addWidget(self.frame_3)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.label_3 = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans SemiBold")
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setContentsMargins(-1, -1, -1, 10)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap(os.path.join(self.media_path, "gray-smile.png")))
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.label_4 = QtWidgets.QLabel(self.frame)
        self.label_4.setMaximumSize(QtCore.QSize(16777215, 35))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans ExtraBold")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_2.addWidget(self.label_4)
        self.verticalLayout_2.setStretch(0, 2)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setContentsMargins(-1, -1, -1, 10)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_9 = QtWidgets.QLabel(self.frame)
        self.label_9.setText("")
        self.label_9.setPixmap(QtGui.QPixmap(os.path.join(self.media_path, "gray-neutral.png")))
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.verticalLayout_5.addWidget(self.label_9)
        self.label_10 = QtWidgets.QLabel(self.frame)
        self.label_10.setMaximumSize(QtCore.QSize(16777215, 35))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans ExtraBold")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_10.setFont(font)
        self.label_10.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_10.setAlignment(QtCore.Qt.AlignCenter)
        self.label_10.setObjectName("label_10")
        self.verticalLayout_5.addWidget(self.label_10)
        self.verticalLayout_5.setStretch(0, 2)
        self.horizontalLayout.addLayout(self.verticalLayout_5)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setContentsMargins(-1, -1, -1, 10)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_7 = QtWidgets.QLabel(self.frame)
        self.label_7.setText("")
        self.label_7.setPixmap(QtGui.QPixmap(os.path.join(self.media_path, "gray-sad.png")))
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.verticalLayout_4.addWidget(self.label_7)
        self.label_8 = QtWidgets.QLabel(self.frame)
        self.label_8.setMaximumSize(QtCore.QSize(16777215, 35))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans ExtraBold")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName("label_8")
        self.verticalLayout_4.addWidget(self.label_8)
        self.verticalLayout_4.setStretch(0, 2)
        self.horizontalLayout.addLayout(self.verticalLayout_4)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setContentsMargins(-1, -1, -1, 10)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.label_11 = QtWidgets.QLabel(self.frame)
        self.label_11.setText("")
        self.label_11.setPixmap(QtGui.QPixmap(os.path.join(self.media_path, "gray-angry.png")))
        self.label_11.setAlignment(QtCore.Qt.AlignCenter)
        self.label_11.setObjectName("label_11")
        self.verticalLayout_6.addWidget(self.label_11)
        self.label_12 = QtWidgets.QLabel(self.frame)
        self.label_12.setMaximumSize(QtCore.QSize(16777215, 35))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans ExtraBold")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_12.setFont(font)
        self.label_12.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_12.setAlignment(QtCore.Qt.AlignCenter)
        self.label_12.setObjectName("label_12")
        self.verticalLayout_6.addWidget(self.label_12)
        self.verticalLayout_6.setStretch(0, 2)
        self.horizontalLayout.addLayout(self.verticalLayout_6)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.pushButton_3 = QtWidgets.QPushButton(self.frame)
        self.pushButton_3.setMinimumSize(QtCore.QSize(0, 50))
        self.pushButton_3.setMaximumSize(QtCore.QSize(250, 16777215))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans SemiBold")
        font.setPointSize(12)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(50, 50, 50);\n"
"border-radius:25px;")
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout_3.addWidget(self.pushButton_3)
        self.horizontalLayout_3.setStretch(0, 2)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 1)
        self.verticalLayout.setStretch(2, 1)
        self.verticalLayout.setStretch(3, 1)
        self.verticalLayout.setStretch(4, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

        self.pushButton.clicked.connect(Form.close)
        
        # Placeholder for HR Worker
        self.hr_worker = None

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Emotion Detection"))
        self.label_5.setText(_translate("Form", "Face Recognition"))
        self.label_13.setText(_translate("Form", "Heart Rate"))
        self.label_15.setText(_translate("Form", "--"))
        self.label_16.setText(_translate("Form", "bpm"))
        self.label_3.setText(_translate("Form", "Your current mood is:"))
        self.label_4.setText(_translate("Form", "Happy"))
        self.label_10.setText(_translate("Form", "Neutral"))
        self.label_8.setText(_translate("Form", "Sad"))
        self.label_12.setText(_translate("Form", "Angry"))
        self.pushButton_3.setText(_translate("Form", "Proceed"))
    

class Recognition(QtWidgets.QWidget, Ui_Form):
    def __init__(self, user_id, dashboard=None ,parent=None):
        super().__init__(parent)
        self.setupUi(self)    
        self.user_id = user_id
        self.dashboard = dashboard 

        # State
        self.hr_worker = None
        self.emotion_buffer = deque(maxlen=7)
        self.current_emotion = "neutral"
        self.current_hr_emotion = "neutral" # Stores HR emotion
        self.signal_session = EmotionSignalSession()
        self.last_hr_status = "Off"

        # Connect UI signals → logic handlers
        self.connect_signals()

        # Initialize the borders based on checkbox state
        self.update_frame_border()
        self.update_frame_3_border()

    # ----------------------------------------------------------------------
    # Signal Connections
    # ----------------------------------------------------------------------
    def connect_signals(self):
        # Facial Recognition (FER)
        self.checkBox.stateChanged.connect(self.update_frame_border)
        self.checkBox.stateChanged.connect(self.toggle_camera)

        # Heart Rate (HR)
        self.checkBox_2.stateChanged.connect(self.update_frame_3_border)
        self.checkBox_2.stateChanged.connect(self.toggle_heart_rate)

        # Recommendations
        self.pushButton_3.clicked.connect(self.proceed_and_close)

    def set_fer_status(self, status):
        state = self.signal_session.update_fer(status=status)
        self.label_3.setText(f"Fused mood: {state.fused_mood.capitalize()}")
        self.label_6.clear()
        if status != "Camera active":
            self.label_6.setText(status)

    def set_hr_status(self, status):
        self.last_hr_status = status
        state = self.signal_session.update_hr(status=status)
        self.label_16.setText(status)
        self.label_3.setText(f"Fused mood: {state.fused_mood.capitalize()}")

    # --------------------------------------------------------------------------
    # Heart Rate Monitor Logic
    # --------------------------------------------------------------------------
    def toggle_heart_rate(self):
        """Called when the HR switch (checkBox_2) is toggled."""
        if self.checkBox_2.isChecked():
            # Start Monitoring
            self.start_hr_monitor()
        else:
            # Stop Monitoring
            self.stop_hr_monitor()

    def start_hr_monitor(self):
        """Initializes and starts the HR worker thread."""
        if self.hr_worker is not None:
            return # Already running

        self.set_hr_status("Loading model")
        
        self.hr_worker = HeartRateWorker()
        self.hr_worker.data_update.connect(self.update_hr_display)
        self.hr_worker.status_update.connect(self.update_hr_status)
        # New Connection for tracking real emotion for recommendations
        self.hr_worker.real_emotion_update.connect(self.update_hr_emotion)
        
        self.hr_worker.finished.connect(self.on_hr_worker_finished)
        self.hr_worker.start()

    def stop_hr_monitor(self):
        """Stops the HR worker thread."""
        if self.hr_worker:
            self.label_16.setText("Stopping...")
            self.hr_worker.stop_process()
            # We don't set hr_worker to None here immediately; 
            # wait for finished signal or let it cleanup.

    def update_hr_display(self, raw_bpm, emotion):
        """Slot to update the UI with new HR data."""
        # label_15: Big Number (Raw BPM)
        self.label_15.setText(f"{raw_bpm}")
        
        # label_16: Small Text (Emotion)
        hr_label = None if emotion in ("Buffering...", "Invalid Input", "Model Missing") else emotion
        state = self.signal_session.update_hr(status="Connected", bpm=raw_bpm, label=hr_label)
        self.current_hr_emotion = state.hr_label or "neutral"
        self.label_16.setText(f"{emotion}")
        self.label_3.setText(f"Fused mood: {state.fused_mood.capitalize()}")

    def update_hr_emotion(self, real_emotion):
        """Captures the actual emotion from HR for the recommendation logic."""
        if real_emotion not in ("Buffering Data", "Invalid Input", "Model Missing"):
            self.current_hr_emotion = real_emotion.lower()

    def update_hr_status(self, status_msg):
        """Slot for status updates (Connecting, Error, etc)."""
        self.set_hr_status(status_msg)
        if status_msg == "Device not found":
             self.label_15.setText("--")

    def on_hr_worker_finished(self):
        """Cleanup when thread ends."""
        self.hr_worker = None
        self.label_15.setText("--")
        self.current_hr_emotion = "neutral"
        terminal_status = self.last_hr_status
        state = self.signal_session.reset_hr("Off")
        if terminal_status in {"Device not found", "Model missing", "Error"}:
            self.label_16.setText(terminal_status)
        else:
            self.label_16.setText("bpm") # Reset to default
        self.label_3.setText(f"Fused mood: {state.fused_mood.capitalize()}")

        # If the checkbox is still checked but thread died (e.g. error), uncheck it
        if self.checkBox_2.isChecked():
            self.checkBox_2.blockSignals(True)
            self.checkBox_2.setChecked(False)
            self.checkBox_2.blockSignals(False)
            self.update_frame_3_border()

    # --------------------------------------------------------------------------
    # Facial Emotion Recognition Logic
    # --------------------------------------------------------------------------
    def toggle_camera(self):
        """Turns camera ON or OFF."""
        if self.checkBox.isChecked():
            # turn ON
            if not hasattr(self, 'cam') or not self.cam.available:
                self.start_camera()
            else:
                self.timer.start(30)
        else:
            # turn OFF
            if hasattr(self, 'timer'):
                self.timer.stop()

            self.signal_session.reset_fer("Off")
            self.label_6.clear()
            self.label_6.setText("Camera Off")
            self.label_3.setText(f"Fused mood: {self.signal_session.state.fused_mood.capitalize()}")

            # Reset icons
            gray = os.path.join(self.media_path, "gray-")
            self.label_2.setPixmap(QtGui.QPixmap(gray + "smile.png"))
            self.label_9.setPixmap(QtGui.QPixmap(gray + "neutral.png"))
            self.label_7.setPixmap(QtGui.QPixmap(gray + "sad.png"))
            self.label_11.setPixmap(QtGui.QPixmap(gray + "angry.png"))
    
    def start_camera(self):
        self.set_fer_status("Loading model")

        # Start background model loader
        self.loader = FERLoaderThread()
        self.loader.loaded.connect(self.on_model_loaded)
        self.loader.status.connect(self.set_fer_status)
        self.loader.error.connect(self.on_fer_loader_error)
        self.loader.start()

    def stop_camera(self):
        if hasattr(self, "timer"):
            self.timer.stop()
        if hasattr(self, "infer_thread"):
            self.infer_thread.running = False

        self.signal_session.reset_fer("Off")
        self.label_6.clear()
        self.label_6.setText("Camera Off")
        self.label_3.setText(f"Fused mood: {self.signal_session.state.fused_mood.capitalize()}")

    def on_model_loaded(self, model):
        self.fer_model = model
        self.set_fer_status("Camera active")

        # Start inference thread
        self.infer_thread = FERInferenceThread(model)
        self.infer_thread.result_ready.connect(self.on_inference_result)
        self.infer_thread.start()

        # Start camera
        self.cam = Camera()
        if not self.cam.available:
            self.set_fer_status("No webcam detected")
            return
        
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

        self.set_fer_status("Camera active")

    def on_fer_loader_error(self, message):
        print(f"FER loader error: {message}")
        if self.checkBox.isChecked():
            self.checkBox.blockSignals(True)
            self.checkBox.setChecked(False)
            self.checkBox.blockSignals(False)
            self.update_frame_border()

    def on_inference_result(self, result):
        self.latest_result = result

    def update_frame(self):
        success, frame = self.cam.read_frame()
        if not success:
            return
        
        self.latest_raw_frame = frame.copy()

        # send frame to inference thread
        self.infer_thread.update_frame(frame)

        display = frame.copy()

        if hasattr(self, "latest_result") and self.latest_result:
            display = self.fer_model.draw_prediction(display,  self.latest_result)
            emotion = self.latest_result["label"].lower()
            self.update_emotion(emotion)

        self.display_frame(display)

    def display_frame(self, frame):
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        qimg = QtGui.QImage(rgb_image.data, w, h, ch * w, QtGui.QImage.Format_RGB888)
        self.label_6.setPixmap(QtGui.QPixmap.fromImage(qimg))

    def update_emotion(self, emotion):
        self.emotion_buffer.append(emotion)
        smoothed = max(set(self.emotion_buffer), key=self.emotion_buffer.count)
        self.current_emotion = smoothed          # stable emotion
        state = self.signal_session.update_fer(status="Camera active", label=smoothed)
        
        # Update the GUI text
        self.label_3.setText(f"Fused mood: {state.fused_mood.capitalize()}")

        icons = {
            "happy": ("happy.png", "gray-neutral.png", "gray-sad.png", "gray-angry.png"),
            "neutral": ("gray-smile.png", "neutral.png", "gray-sad.png", "gray-angry.png"),
            "sad": ("gray-smile.png", "gray-neutral.png", "sad.png", "gray-angry.png"),
            "angry": ("gray-smile.png", "gray-neutral.png", "gray-sad.png", "angry.png"),
        }

        happy_icon, neutral_icon, sad_icon, angry_icon = icons.get(smoothed, icons["neutral"])

        self.label_2.setPixmap(QtGui.QPixmap(os.path.join(self.media_path, happy_icon)))
        self.label_9.setPixmap(QtGui.QPixmap(os.path.join(self.media_path, neutral_icon)))
        self.label_7.setPixmap(QtGui.QPixmap(os.path.join(self.media_path, sad_icon)))
        self.label_11.setPixmap(QtGui.QPixmap(os.path.join(self.media_path, angry_icon)))

    def open_recommendations(self):
        engine = RecommendationEngine()

        inputs = self.signal_session.recommendation_inputs()

        try:
            recommendations = engine.recommend(
                user_id=self.user_id,
                fer_emotion=inputs["fer_emotion"],
                hr_emotion=inputs["hr_emotion"],
                combined_mode=inputs["combined_mode"],
                top_k=10  # Request 10 songs
            )

            if not recommendations:
                print("No recommended songs found.")
                return

            # Send the recommended songs list to the dashboard
            if self.dashboard:
                self.dashboard.load_recommended_songs(recommendations)

        except Exception as e:
            print(f"Error generating recommendations: {e}")

    def proceed_and_close(self):
        # 1. Open recommendations
        self.open_recommendations()
        
        # 2. Close the Recognition UI
        self.close()


    def update_frame_border(self):
        if self.checkBox.isChecked():
            self.frame_2.setStyleSheet("#frame_2 {\n"
"    border: 2px solid white;\n"
"}\n"
"")
        else:
            self.frame_2.setStyleSheet("#frame_2 {\n"
"    border: none;\n"
"}\n"
"")

    def update_frame_3_border(self):
        if self.checkBox_2.isChecked():
            self.frame_3.setStyleSheet("#frame_3 {\n"
"    border: 2px solid white;\n"
"}\n"
"")
        else:
            self.frame_3.setStyleSheet("#frame_3 {\n"
"    border: none;\n"
"}\n"
"")

# -------------------------------------------------------------------------
# Heart Rate Worker Thread
# -------------------------------------------------------------------------
class HeartRateWorker(QtCore.QThread):
    """
    Runs the asyncio loop for BLE Heart Rate reading in a separate thread
    to keep the PyQt GUI responsive.
    """
    # Signal to update GUI: (raw_bpm, display_string)
    data_update = QtCore.pyqtSignal(int, str)
    
    # NEW: Signal to update Recommendation Engine: (real_emotion_category)
    real_emotion_update = QtCore.pyqtSignal(str)
    
    status_update = QtCore.pyqtSignal(str) # To show status like "Connecting..."

    def __init__(self):
        super().__init__()
        self._loop = None
        self._stop_event = None

    def run(self):
        """Entry point for the thread."""
        try:
            # Create a new event loop for this thread
            self._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._loop)
            self._stop_event = asyncio.Event()

            # Load HR Model
            self.status_update.emit("Loading model")
            if load_model_components():
                self.status_update.emit("Scanning BLE")
                # Run the async task
                self._loop.run_until_complete(self.async_main())
            else:
                self.status_update.emit("Model missing")
        except Exception as e:
            print(f"HR Worker Error: {e}")
            self.status_update.emit("Error")
        finally:
            if self._loop and self._loop.is_running():
                self._loop.close()

    async def async_main(self):
        """Async main wrapper for the BLE reader."""
        # Callback function for every new HR reading
        def hr_callback(raw_bpm):
            # 1. Predict Emotion
            quadrant, real_emotion = predict_emotions_live(raw_bpm)
            
            # 2. Display Logic
            display_emotion = real_emotion
            if quadrant == "Buffering Data":
                display_emotion = "Buffering..."
            
            # 3. Emit Signal to GUI (Display)
            self.data_update.emit(raw_bpm, display_emotion)
            
            # 4. Emit Signal to Recommendation Logic (Raw Category)
            # Send the real prediction even if currently buffering display
            self.real_emotion_update.emit(real_emotion)

        # Start reading
        success = await read_heart_rate_live(hr_callback, self._stop_event)
        
        if not success:
            self.status_update.emit("Device not found")
        
        # Save final emotion on exit
        calculate_final_emotion_and_save()

    def stop_process(self):
        """Thread-safe way to stop the asyncio loop."""
        if self._loop and self._stop_event:
            self._loop.call_soon_threadsafe(self._stop_event.set)
        
        self.quit()
        self.wait()
            

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    dashboard = DashboardWindow()
    dashboard.show()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

import sys, os, vlc, re

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QCompleter
from types import SimpleNamespace

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from app.gui.recognition import Recognition as Ui_Recognition


def normalize_text(text):
    """Lowercase and remove non-alphanumeric characters for simple NLP-like matching."""
    text = text.lower().strip()
    text = re.sub(r'[^a-z0-9 ]', '', text)
    return text


class ClickableLabel(QtWidgets.QLabel):
    clicked = QtCore.pyqtSignal()
    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.clicked.emit()
        super().mouseReleaseEvent(event)


class HoverAccentFilter(QtCore.QObject):
    """Adds a subtle, layout-stable glow to interactive dashboard elements."""

    def eventFilter(self, widget, event):
        if event.type() == QtCore.QEvent.Enter:
            effect = QtWidgets.QGraphicsDropShadowEffect(widget)
            effect.setBlurRadius(18)
            effect.setOffset(0, 2)
            effect.setColor(QtGui.QColor(255, 255, 255, 70))
            widget.setGraphicsEffect(effect)
        elif event.type() == QtCore.QEvent.Leave:
            widget.setGraphicsEffect(None)
        return False


class CoverDownloadSignals(QtCore.QObject):
    downloaded = QtCore.pyqtSignal(object, str)
    failed = QtCore.pyqtSignal(object, str)


class CoverDownloadTask(QtCore.QRunnable):
    def __init__(self, cloud_services, song):
        super().__init__()
        self.cloud_services = cloud_services
        self.song = song
        self.signals = CoverDownloadSignals()

    def run(self):
        try:
            path = self.cloud_services.prepare_cover(self.song)
        except Exception as exc:
            self.signals.failed.emit(self.song, str(exc))
            return
        self.signals.downloaded.emit(self.song, str(path))


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1422, 1018)
        Form.setStyleSheet("background-color: rgb(20, 20, 20);")
        Form.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        Form.setMouseTracking(False)
        base_path = os.path.dirname(__file__)  # app/gui/
        self.media_path = os.path.abspath(os.path.join(base_path, "..", "..", "media"))
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(13)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setSpacing(15)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(12)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.user_2 = QtWidgets.QLabel(Form)
        self.user_2.setMaximumSize(QtCore.QSize(60, 60))
        self.user_2.setText("")
        self.user_2.setPixmap(QtGui.QPixmap(os.path.join(self.media_path, "user.png")))
        self.user_2.setScaledContents(True)
        self.user_2.setObjectName("user_2")
        self.horizontalLayout_3.addWidget(self.user_2)
        self.pushButton_9 = QtWidgets.QPushButton(Form)
        self.pushButton_9.setMinimumSize(QtCore.QSize(50, 50))
        self.pushButton_9.setMaximumSize(QtCore.QSize(50, 50))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans SemiBold")
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_9.setFont(font)
        self.pushButton_9.setStyleSheet(
    "QPushButton {\n"
    "    background-color: rgb(45, 45, 45);\n"
    "    color: rgb(255, 255, 255);\n"
    "    border-radius: 25px;\n"
    "}\n"
    "QPushButton:hover {\n"
    "    background-color: rgb(60, 60, 60);\n"
    "}"
)

        self.pushButton_9.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.media_path, "home.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_9.setIcon(icon)
        self.pushButton_9.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_9.setObjectName("pushButton_9")
        self.horizontalLayout_3.addWidget(self.pushButton_9)
        self.pushButton_10 = QtWidgets.QPushButton(Form)
        self.pushButton_10.setMinimumSize(QtCore.QSize(50, 50))
        self.pushButton_10.setMaximumSize(QtCore.QSize(50, 50))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans SemiBold")
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_10.setFont(font)
        self.pushButton_10.setStyleSheet(
    "QPushButton {\n"
    "    background-color: rgb(45, 45, 45);\n"
    "    color: rgb(255, 255, 255);\n"
    "    border-radius: 25px;\n"
    "}\n"
    "QPushButton:hover {\n"
    "    background-color: rgb(60, 60, 60);\n"
    "}"
)

        self.pushButton_10.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(os.path.join(self.media_path, "radio.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_10.setIcon(icon1)
        self.pushButton_10.setIconSize(QtCore.QSize(50, 50))
        self.pushButton_10.setObjectName("pushButton_10")
        self.horizontalLayout_3.addWidget(self.pushButton_10)
        self.horizontalFrame = QtWidgets.QFrame(Form)
        self.horizontalFrame.setMaximumSize(QtCore.QSize(16777215, 50))
        self.horizontalFrame.setStyleSheet("background-color: rgb(45, 45, 45);\n"
"border-radius:15px;")
        self.horizontalFrame.setObjectName("horizontalFrame")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.horizontalFrame)
        self.horizontalLayout_4.setContentsMargins(3, 0, 0, 0)
        self.horizontalLayout_4.setSpacing(9)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_10 = ClickableLabel(self.horizontalFrame)
        self.label_10.setMaximumSize(QtCore.QSize(40, 40))
        self.label_10.setText("")
        self.label_10.setPixmap(QtGui.QPixmap(os.path.join(self.media_path, "search.svg")))
        self.label_10.setScaledContents(True)
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_4.addWidget(self.label_10)

        self.pushButton_9.clicked.connect(lambda: self.tabWidget.setCurrentIndex(0))
        self.lineEdit_2 = QtWidgets.QLineEdit(self.horizontalFrame)
        self.lineEdit_2.setMinimumSize(QtCore.QSize(800, 50))
        self.lineEdit_2.setMaximumSize(QtCore.QSize(1500, 50))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans SemiBold")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.lineEdit_2.setFont(font)
        self.lineEdit_2.setStyleSheet("color: rgb(214, 214, 214);\n"
"")
        self.lineEdit_2.setText("")
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.horizontalLayout_4.addWidget(self.lineEdit_2)
        self.horizontalLayout_4.setStretch(0, 1)
        self.horizontalLayout_4.setStretch(1, 7)
        self.horizontalLayout_3.addWidget(self.horizontalFrame)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.minimize_2 = ClickableLabel(Form)
        self.minimize_2.setMaximumSize(QtCore.QSize(30, 30))
        self.minimize_2.setPixmap(QtGui.QPixmap(os.path.join(self.media_path, "minimize.png")))
        self.minimize_2.setScaledContents(True)
        self.minimize_2.setObjectName("minimize_2")
        self.horizontalLayout_3.addWidget(self.minimize_2)
        self.minimize_2.clicked.connect(Form.showMinimized)
        self.maximize_2 = ClickableLabel(Form)
        self.maximize_2.setMaximumSize(QtCore.QSize(25, 25))
        self.maximize_2.setText("")
        self.maximize_2.setPixmap(QtGui.QPixmap(os.path.join(self.media_path, "maximize.png")))
        self.maximize_2.setScaledContents(True)
        self.maximize_2.setObjectName("maximize_2")
        self.horizontalLayout_3.addWidget(self.maximize_2)
        self.close_2 = ClickableLabel(Form)
        self.close_2.setMinimumSize(QtCore.QSize(30, 0))
        self.close_2.setMaximumSize(QtCore.QSize(30, 30))
        self.close_2.setPixmap(QtGui.QPixmap(os.path.join(self.media_path, "x.svg")))
        self.close_2.setScaledContents(True)
        self.close_2.setObjectName("close_2")
        self.horizontalLayout_3.addWidget(self.close_2)
        self.close_2.clicked.connect(QtWidgets.QApplication.instance().quit)
        self.horizontalLayout_3.setStretch(1, 11)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.verticalLayout_3.setStretch(0, 1)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.horizontalLayout.setStretch(0, 4)
        self.verticalLayout_6.addLayout(self.horizontalLayout)

        self.maximized = False
        self._normalGeometry = Form.geometry()

        # --- Addition for drag window functionality ---
        self._startPos = None
        self._isTracking = False

        def mousePressEvent(event):
            if event.button() == QtCore.Qt.LeftButton and not self.maximized:
                # Track offset between mouse and top-left of window
                self._startPos = event.globalPos() - Form.frameGeometry().topLeft()
                self._isTracking = True

        def mouseMoveEvent(event):
            if self._isTracking and not self.maximized:
                # Move window according to the offset
                Form.move(event.globalPos() - self._startPos)

        def mouseReleaseEvent(event):
            if event.button() == QtCore.Qt.LeftButton:
                self._isTracking = False

        # Assign the above events to the Form
        Form.mousePressEvent = mousePressEvent
        Form.mouseMoveEvent = mouseMoveEvent
        Form.mouseReleaseEvent = mouseReleaseEvent
        # --- End of addition ---

        def toggle_maximize():
            if self.maximized:
                Form.showNormal()
                Form.setMinimumSize(QtCore.QSize(0, 0))
                Form.setMaximumSize(QtCore.QSize(16777215, 16777215))
                self.maximized = False
                self._startPos = None
                self._isTracking = False
                self.maximize_2.setPixmap(QtGui.QPixmap(os.path.join(self.media_path, "maximize.png")))
            else:
                Form.showMaximized()
                self.maximized = True
                self._startPos = None
                self._isTracking = False
                self.maximize_2.setPixmap(QtGui.QPixmap(os.path.join(self.media_path, "restore_down.png")))

        self.maximize_2.clicked.connect(toggle_maximize)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout()
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.tabWidget = QtWidgets.QTabWidget(Form)
        self.tabWidget.setStyleSheet("QTabWidget::pane {\n"
"    background: rgb(20, 20, 20);\n"
"}\n"
"\n"
"QTabBar::tab {\n"
"    height: 0px;       /* hides the tabs completely */\n"
"    width: 0px;\n"
"    margin: 0px;\n"
"    padding: 0px;\n"
"    border: none;\n"
"}\n"
"\n"
"QTabBar::tab:selected {\n"
"    background: rgb(45, 45, 45);\n"
"    color: white;\n"
"}\n"
"\n"
"QTabBar::tab:hover {\n"
"    background: rgb(60, 60, 60);\n"
"}\n"
"")
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayout_14 = QtWidgets.QVBoxLayout(self.tab)
        self.verticalLayout_14.setObjectName("verticalLayout_14")
        self.widget_5 = QtWidgets.QWidget(self.tab)
        self.widget_5.setMinimumSize(QtCore.QSize(0, 231))
        self.widget_5.setStyleSheet("background-color:rgb(33, 33, 33);\n"
"border-radius:15px;")
        self.widget_5.setObjectName("widget_5")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.widget_5)
        self.gridLayout_5.setObjectName("gridLayout_5") 
        self.label_25 = QtWidgets.QLabel(self.widget_5)
        self.label_25.setMinimumSize(QtCore.QSize(400, 207))
        self.label_25.setMaximumSize(QtCore.QSize(16777215, 250))
        self.label_25.setStyleSheet("background-color: rgb(16, 133, 165);\n"
"border-radius:10px;")
        self.label_25.setText("")
        self.label_25.setPixmap(QtGui.QPixmap(os.path.join(self.media_path, "banner2.webp")))
        self.label_25.setScaledContents(True)
        self.label_25.setObjectName("label_25")
        self.gridLayout_5.addWidget(self.label_25, 0, 1, 1, 1)
        self.label_26 = QtWidgets.QLabel(self.widget_5)
        self.label_26.setMinimumSize(QtCore.QSize(400, 207))
        self.label_26.setMaximumSize(QtCore.QSize(16777215, 250))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans ExtraBold")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_26.setFont(font)
        self.label_26.setStyleSheet("background-color: rgb(158, 34, 207);\n"
"border-radius:10px;\n"
"\n"
"")
        self.label_26.setTextFormat(QtCore.Qt.AutoText)
        self.label_26.setAlignment(QtCore.Qt.AlignCenter)
        self.label_26.setPixmap(QtGui.QPixmap(os.path.join(self.media_path, "banner3.webp")))
        self.label_26.setScaledContents(True)
        self.label_26.setObjectName("label_26")
        self.gridLayout_5.addWidget(self.label_26, 0, 2, 1, 1)
        self.label_27 = QtWidgets.QLabel(self.widget_5)
        self.label_27.setMinimumSize(QtCore.QSize(400, 207))
        self.label_27.setMaximumSize(QtCore.QSize(16777215, 250))
        self.label_27.setStyleSheet("background-color: rgb(186, 105, 51);\n"
"border-radius:10px;")
        self.label_27.setText("")
        self.label_27.setPixmap(QtGui.QPixmap(os.path.join(self.media_path, "banner1.webp")))
        self.label_27.setScaledContents(True)
        self.label_27.setObjectName("label_27")
        self.gridLayout_5.addWidget(self.label_27, 0, 0, 1, 1)

        # Add clickable functionality to label_27 to switch to tab 3 in tabWidget
        self.label_27.mouseReleaseEvent = lambda event: self.tabWidget.setCurrentIndex(2) if event.button() == QtCore.Qt.LeftButton else None

        # Add clickable functionality to label_25 and label_26 to switch to tab 3 in tabWidget
        self.label_25.mouseReleaseEvent = lambda event: self.tabWidget.setCurrentIndex(2) if event.button() == QtCore.Qt.LeftButton else None
        self.label_26.mouseReleaseEvent = lambda event: self.tabWidget.setCurrentIndex(2) if event.button() == QtCore.Qt.LeftButton else None
        self.verticalLayout_14.addWidget(self.widget_5)
        self.scrollArea_2 = QtWidgets.QScrollArea(self.tab)
        self.scrollArea_2.setMinimumSize(QtCore.QSize(0, 250))
        self.scrollArea_2.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.scrollArea_2.setStyleSheet("QScrollArea {\n"
"    /* Ensures the scroll area itself is frameless */\n"
"    border: none;\n"
"    background-color: transparent;\n"
"}\n"
"\n"
"/* 1. Base Scroll Bar Styling (The main vertical bar) */\n"
"QScrollBar:vertical {\n"
"    border: none;\n"
"    background: transparent;\n"
"    /* Make the entire area where the scrollbar sits very narrow */\n"
"    width: 8px; \n"
"    /* The arrows aren\'t typically used in this style, so we hide them */\n"
"    margin: 0px 0 0px 0;\n"
"}\n"
"\n"
"/* 2. Scroll Bar Handle (The movable thumb) */\n"
"QScrollBar::handle:vertical {\n"
"    /* Color and rounded edges for the thumb */\n"
"    background: #555555; /* Dark gray color */\n"
"    min-height: 20px;\n"
"    border-radius: 4px; /* Slightly rounded edges */\n"
"}\n"
"\n"
"/* 3. Handle Hover State */\n"
"QScrollBar::handle:vertical:hover {\n"
"    background: #888888; /* Slightly lighter gray on hover */\n"
"}\n"
"\n"
"/* 4. Scroll Bar Track (The background area behind the thumb) */\n"
"QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
"    background: none;\n"
"}\n"
"\n"
"/* 5. Hiding the Arrows (If they appear) */\n"
"QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n"
"    border: none;\n"
"    width: 0px;\n"
"    height: 0px;\n"
"    background: none;\n"
"}\n"
"\n"
"QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {\n"
"    border: none;\n"
"    background: none;\n"
"}")
        self.scrollArea_2.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollArea_2.setObjectName("scrollArea_2")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 1039, 1126))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_2)
        self.verticalLayout_2.setContentsMargins(-1, 4, -1, -1)
        self.verticalLayout_2.setSpacing(15)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.widget_14 = QtWidgets.QWidget(self.scrollAreaWidgetContents_2)
        self.widget_14.setMinimumSize(QtCore.QSize(0, 400))
        self.widget_14.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.widget_14.setStyleSheet("background-color:rgb(33, 33, 33);\n"
"border-radius:15px;")
        self.widget_14.setObjectName("widget_14")
        self.verticalLayout_280 = QtWidgets.QVBoxLayout(self.widget_14)
        self.verticalLayout_280.setContentsMargins(15, 10, 15, 10)
        self.verticalLayout_280.setSpacing(15)
        self.verticalLayout_280.setObjectName("verticalLayout_280")
        self.label_41 = QtWidgets.QLabel(self.widget_14)
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans ExtraBold")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_41.setFont(font)
        self.label_41.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_41.setMidLineWidth(0)
        self.label_41.setObjectName("label_41")
        self.verticalLayout_280.addWidget(self.label_41)
        self.horizontalLayout_36 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_36.setContentsMargins(-1, 0, -1, 0)
        self.horizontalLayout_36.setSpacing(20)
        self.horizontalLayout_36.setObjectName("horizontalLayout_36")
        self.verticalLayout_281 = QtWidgets.QVBoxLayout()
        self.verticalLayout_281.setContentsMargins(-1, -1, -1, 0)
        self.verticalLayout_281.setSpacing(5)
        self.verticalLayout_281.setObjectName("verticalLayout_281")
        self.label_446 = QtWidgets.QLabel(self.widget_14)
        self.label_446.setMinimumSize(QtCore.QSize(100, 100))
        self.label_446.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.label_446.setStyleSheet("background-color: rgb(186, 105, 51);\n"
"border-radius:10px;")
        self.label_446.setText("")
        self.label_446.setObjectName("label_446")
        self.verticalLayout_281.addWidget(self.label_446)
        self.verticalLayout_282 = QtWidgets.QVBoxLayout()
        self.verticalLayout_282.setContentsMargins(-1, 0, -1, 10)
        self.verticalLayout_282.setSpacing(10)
        self.verticalLayout_282.setObjectName("verticalLayout_282")
        self.label_447 = QtWidgets.QLabel(self.widget_14)
        self.label_447.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans Medium")
        font.setPointSize(10)
        self.label_447.setFont(font)
        self.label_447.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_447.setObjectName("label_447")
        self.verticalLayout_282.addWidget(self.label_447)
        self.label_448 = QtWidgets.QLabel(self.widget_14)
        self.label_448.setMaximumSize(QtCore.QSize(16777215, 18))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans Medium")
        font.setPointSize(10)
        self.label_448.setFont(font)
        self.label_448.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_448.setObjectName("label_448")
        self.verticalLayout_282.addWidget(self.label_448)
        self.verticalLayout_282.setStretch(0, 1)
        self.verticalLayout_281.addLayout(self.verticalLayout_282)
        self.verticalLayout_281.setStretch(0, 1)
        self.horizontalLayout_36.addLayout(self.verticalLayout_281)
        self.verticalLayout_283 = QtWidgets.QVBoxLayout()
        self.verticalLayout_283.setSpacing(5)
        self.verticalLayout_283.setObjectName("verticalLayout_283")
        self.label_449 = QtWidgets.QLabel(self.widget_14)
        self.label_449.setMinimumSize(QtCore.QSize(100, 100))
        self.label_449.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.label_449.setStyleSheet("background-color: rgb(186, 105, 51);\n"
"border-radius:10px;")
        self.label_449.setText("")
        self.label_449.setObjectName("label_449")
        self.verticalLayout_283.addWidget(self.label_449)
        self.verticalLayout_284 = QtWidgets.QVBoxLayout()
        self.verticalLayout_284.setContentsMargins(-1, 0, -1, 10)
        self.verticalLayout_284.setSpacing(10)
        self.verticalLayout_284.setObjectName("verticalLayout_284")
        self.label_450 = QtWidgets.QLabel(self.widget_14)
        self.label_450.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans Medium")
        font.setPointSize(10)
        self.label_450.setFont(font)
        self.label_450.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_450.setObjectName("label_450")
        self.verticalLayout_284.addWidget(self.label_450)
        self.label_451 = QtWidgets.QLabel(self.widget_14)
        self.label_451.setMaximumSize(QtCore.QSize(16777215, 18))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans Medium")
        font.setPointSize(10)
        self.label_451.setFont(font)
        self.label_451.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_451.setObjectName("label_451")
        self.verticalLayout_284.addWidget(self.label_451)
        self.verticalLayout_283.addLayout(self.verticalLayout_284)
        self.verticalLayout_283.setStretch(0, 5)
        self.horizontalLayout_36.addLayout(self.verticalLayout_283)
        self.verticalLayout_285 = QtWidgets.QVBoxLayout()
        self.verticalLayout_285.setSpacing(5)
        self.verticalLayout_285.setObjectName("verticalLayout_285")
        self.label_452 = QtWidgets.QLabel(self.widget_14)
        self.label_452.setMinimumSize(QtCore.QSize(100, 100))
        self.label_452.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.label_452.setStyleSheet("background-color: rgb(186, 105, 51);\n"
"border-radius:10px;")
        self.label_452.setText("")
        self.label_452.setObjectName("label_452")
        self.verticalLayout_285.addWidget(self.label_452)
        self.verticalLayout_286 = QtWidgets.QVBoxLayout()
        self.verticalLayout_286.setContentsMargins(-1, 0, -1, 10)
        self.verticalLayout_286.setSpacing(10)
        self.verticalLayout_286.setObjectName("verticalLayout_286")
        self.label_453 = QtWidgets.QLabel(self.widget_14)
        self.label_453.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans Medium")
        font.setPointSize(10)
        self.label_453.setFont(font)
        self.label_453.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_453.setObjectName("label_453")
        self.verticalLayout_286.addWidget(self.label_453)
        self.label_454 = QtWidgets.QLabel(self.widget_14)
        self.label_454.setMaximumSize(QtCore.QSize(16777215, 18))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans Medium")
        font.setPointSize(10)
        self.label_454.setFont(font)
        self.label_454.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_454.setObjectName("label_454")
        self.verticalLayout_286.addWidget(self.label_454)
        self.verticalLayout_286.setStretch(0, 1)
        self.verticalLayout_286.setStretch(1, 1)
        self.verticalLayout_285.addLayout(self.verticalLayout_286)
        self.verticalLayout_285.setStretch(0, 6)
        self.horizontalLayout_36.addLayout(self.verticalLayout_285)
        self.verticalLayout_287 = QtWidgets.QVBoxLayout()
        self.verticalLayout_287.setSpacing(5)
        self.verticalLayout_287.setObjectName("verticalLayout_287")
        self.label_455 = QtWidgets.QLabel(self.widget_14)
        self.label_455.setMinimumSize(QtCore.QSize(100, 100))
        self.label_455.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.label_455.setStyleSheet("background-color: rgb(186, 105, 51);\n"
"border-radius:10px;")
        self.label_455.setText("")
        self.label_455.setObjectName("label_455")
        self.verticalLayout_287.addWidget(self.label_455)
        self.verticalLayout_288 = QtWidgets.QVBoxLayout()
        self.verticalLayout_288.setContentsMargins(-1, 0, -1, 10)
        self.verticalLayout_288.setSpacing(10)
        self.verticalLayout_288.setObjectName("verticalLayout_288")
        self.label_456 = QtWidgets.QLabel(self.widget_14)
        self.label_456.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans Medium")
        font.setPointSize(10)
        self.label_456.setFont(font)
        self.label_456.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_456.setObjectName("label_456")
        self.verticalLayout_288.addWidget(self.label_456)
        self.label_457 = QtWidgets.QLabel(self.widget_14)
        self.label_457.setMaximumSize(QtCore.QSize(16777215, 18))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans Medium")
        font.setPointSize(10)
        self.label_457.setFont(font)
        self.label_457.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_457.setObjectName("label_457")
        self.verticalLayout_288.addWidget(self.label_457)
        self.verticalLayout_288.setStretch(0, 1)
        self.verticalLayout_288.setStretch(1, 1)
        self.verticalLayout_287.addLayout(self.verticalLayout_288)
        self.verticalLayout_287.setStretch(0, 6)
        self.horizontalLayout_36.addLayout(self.verticalLayout_287)
        self.verticalLayout_289 = QtWidgets.QVBoxLayout()
        self.verticalLayout_289.setSpacing(5)
        self.verticalLayout_289.setObjectName("verticalLayout_289")
        self.label_458 = QtWidgets.QLabel(self.widget_14)
        self.label_458.setMinimumSize(QtCore.QSize(100, 100))
        self.label_458.setMaximumSize(QtCore.QSize(16777215, 500))
        self.label_458.setStyleSheet("background-color: rgb(186, 105, 51);\n"
"border-radius:10px;")
        self.label_458.setText("")
        self.label_458.setObjectName("label_458")
        self.verticalLayout_289.addWidget(self.label_458)
        self.verticalLayout_290 = QtWidgets.QVBoxLayout()
        self.verticalLayout_290.setContentsMargins(-1, 0, -1, 10)
        self.verticalLayout_290.setSpacing(10)
        self.verticalLayout_290.setObjectName("verticalLayout_290")
        self.label_459 = QtWidgets.QLabel(self.widget_14)
        self.label_459.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans Medium")
        font.setPointSize(10)
        self.label_459.setFont(font)
        self.label_459.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_459.setObjectName("label_459")
        self.verticalLayout_290.addWidget(self.label_459)
        self.label_460 = QtWidgets.QLabel(self.widget_14)
        self.label_460.setMaximumSize(QtCore.QSize(16777215, 18))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans Medium")
        font.setPointSize(10)
        self.label_460.setFont(font)
        self.label_460.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_460.setObjectName("label_460")
        self.verticalLayout_290.addWidget(self.label_460)
        self.verticalLayout_290.setStretch(0, 1)
        self.verticalLayout_290.setStretch(1, 1)
        self.verticalLayout_289.addLayout(self.verticalLayout_290)
        self.verticalLayout_289.setStretch(0, 6)
        self.horizontalLayout_36.addLayout(self.verticalLayout_289)
        self.verticalLayout_280.addLayout(self.horizontalLayout_36)
        self.verticalLayout_280.setStretch(0, 1)
        self.verticalLayout_280.setStretch(1, 6)
        self.verticalLayout_2.addWidget(self.widget_14)
        self.widget_13 = QtWidgets.QWidget(self.scrollAreaWidgetContents_2)
        self.widget_13.setMinimumSize(QtCore.QSize(0, 400))
        self.widget_13.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.widget_13.setStyleSheet("background-color:rgb(33, 33, 33);\n"
"border-radius:15px;")
        self.widget_13.setObjectName("widget_13")
        self.verticalLayout_269 = QtWidgets.QVBoxLayout(self.widget_13)
        self.verticalLayout_269.setContentsMargins(15, 10, 15, 10)
        self.verticalLayout_269.setSpacing(15)
        self.verticalLayout_269.setObjectName("verticalLayout_269")
        self.label_40 = QtWidgets.QLabel(self.widget_13)
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans ExtraBold")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_40.setFont(font)
        self.label_40.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_40.setMidLineWidth(0)
        self.label_40.setObjectName("label_40")
        self.verticalLayout_269.addWidget(self.label_40)
        self.horizontalLayout_35 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_35.setContentsMargins(-1, 0, -1, 0)
        self.horizontalLayout_35.setSpacing(20)
        self.horizontalLayout_35.setObjectName("horizontalLayout_35")
        self.verticalLayout_270 = QtWidgets.QVBoxLayout()
        self.verticalLayout_270.setContentsMargins(-1, -1, -1, 0)
        self.verticalLayout_270.setSpacing(5)
        self.verticalLayout_270.setObjectName("verticalLayout_270")
        self.label_431 = QtWidgets.QLabel(self.widget_13)
        self.label_431.setMinimumSize(QtCore.QSize(100, 100))
        self.label_431.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.label_431.setStyleSheet("background-color: rgb(186, 105, 51);\n"
"border-radius:10px;")
        self.label_431.setText("")
        self.label_431.setObjectName("label_431")
        self.verticalLayout_270.addWidget(self.label_431)
        self.verticalLayout_271 = QtWidgets.QVBoxLayout()
        self.verticalLayout_271.setContentsMargins(-1, 0, -1, 10)
        self.verticalLayout_271.setSpacing(10)
        self.verticalLayout_271.setObjectName("verticalLayout_271")
        self.label_432 = QtWidgets.QLabel(self.widget_13)
        self.label_432.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans Medium")
        font.setPointSize(10)
        self.label_432.setFont(font)
        self.label_432.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_432.setObjectName("label_432")
        self.verticalLayout_271.addWidget(self.label_432)
        self.label_433 = QtWidgets.QLabel(self.widget_13)
        self.label_433.setMaximumSize(QtCore.QSize(16777215, 18))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans Medium")
        font.setPointSize(10)
        self.label_433.setFont(font)
        self.label_433.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_433.setObjectName("label_433")
        self.verticalLayout_271.addWidget(self.label_433)
        self.verticalLayout_271.setStretch(0, 1)
        self.verticalLayout_270.addLayout(self.verticalLayout_271)
        self.verticalLayout_270.setStretch(0, 1)
        self.horizontalLayout_35.addLayout(self.verticalLayout_270)
        self.verticalLayout_272 = QtWidgets.QVBoxLayout()
        self.verticalLayout_272.setSpacing(5)
        self.verticalLayout_272.setObjectName("verticalLayout_272")
        self.label_434 = QtWidgets.QLabel(self.widget_13)
        self.label_434.setMinimumSize(QtCore.QSize(100, 100))
        self.label_434.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.label_434.setStyleSheet("background-color: rgb(186, 105, 51);\n"
"border-radius:10px;")
        self.label_434.setText("")
        self.label_434.setObjectName("label_434")
        self.verticalLayout_272.addWidget(self.label_434)
        self.verticalLayout_273 = QtWidgets.QVBoxLayout()
        self.verticalLayout_273.setContentsMargins(-1, 0, -1, 10)
        self.verticalLayout_273.setSpacing(10)
        self.verticalLayout_273.setObjectName("verticalLayout_273")
        self.label_435 = QtWidgets.QLabel(self.widget_13)
        self.label_435.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans Medium")
        font.setPointSize(10)
        self.label_435.setFont(font)
        self.label_435.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_435.setObjectName("label_435")
        self.verticalLayout_273.addWidget(self.label_435)
        self.label_436 = QtWidgets.QLabel(self.widget_13)
        self.label_436.setMaximumSize(QtCore.QSize(16777215, 18))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans Medium")
        font.setPointSize(10)
        self.label_436.setFont(font)
        self.label_436.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_436.setObjectName("label_436")
        self.verticalLayout_273.addWidget(self.label_436)
        self.verticalLayout_272.addLayout(self.verticalLayout_273)
        self.verticalLayout_272.setStretch(0, 5)
        self.horizontalLayout_35.addLayout(self.verticalLayout_272)
        self.verticalLayout_274 = QtWidgets.QVBoxLayout()
        self.verticalLayout_274.setSpacing(5)
        self.verticalLayout_274.setObjectName("verticalLayout_274")
        self.label_437 = QtWidgets.QLabel(self.widget_13)
        self.label_437.setMinimumSize(QtCore.QSize(100, 100))
        self.label_437.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.label_437.setStyleSheet("background-color: rgb(186, 105, 51);\n"
"border-radius:10px;")
        self.label_437.setText("")
        self.label_437.setObjectName("label_437")
        self.verticalLayout_274.addWidget(self.label_437)
        self.verticalLayout_275 = QtWidgets.QVBoxLayout()
        self.verticalLayout_275.setContentsMargins(-1, 0, -1, 10)
        self.verticalLayout_275.setSpacing(10)
        self.verticalLayout_275.setObjectName("verticalLayout_275")
        self.label_438 = QtWidgets.QLabel(self.widget_13)
        self.label_438.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans Medium")
        font.setPointSize(10)
        self.label_438.setFont(font)
        self.label_438.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_438.setObjectName("label_438")
        self.verticalLayout_275.addWidget(self.label_438)
        self.label_439 = QtWidgets.QLabel(self.widget_13)
        self.label_439.setMaximumSize(QtCore.QSize(16777215, 18))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans Medium")
        font.setPointSize(10)
        self.label_439.setFont(font)
        self.label_439.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_439.setObjectName("label_439")
        self.verticalLayout_275.addWidget(self.label_439)
        self.verticalLayout_275.setStretch(0, 1)
        self.verticalLayout_275.setStretch(1, 1)
        self.verticalLayout_274.addLayout(self.verticalLayout_275)
        self.verticalLayout_274.setStretch(0, 6)
        self.horizontalLayout_35.addLayout(self.verticalLayout_274)
        self.verticalLayout_276 = QtWidgets.QVBoxLayout()
        self.verticalLayout_276.setSpacing(5)
        self.verticalLayout_276.setObjectName("verticalLayout_276")
        self.label_440 = QtWidgets.QLabel(self.widget_13)
        self.label_440.setMinimumSize(QtCore.QSize(100, 100))
        self.label_440.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.label_440.setStyleSheet("background-color: rgb(186, 105, 51);\n"
"border-radius:10px;")
        self.label_440.setText("")
        self.label_440.setObjectName("label_440")
        self.verticalLayout_276.addWidget(self.label_440)
        self.verticalLayout_277 = QtWidgets.QVBoxLayout()
        self.verticalLayout_277.setContentsMargins(-1, 0, -1, 10)
        self.verticalLayout_277.setSpacing(10)
        self.verticalLayout_277.setObjectName("verticalLayout_277")
        self.label_441 = QtWidgets.QLabel(self.widget_13)
        self.label_441.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans Medium")
        font.setPointSize(10)
        self.label_441.setFont(font)
        self.label_441.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_441.setObjectName("label_441")
        self.verticalLayout_277.addWidget(self.label_441)
        self.label_442 = QtWidgets.QLabel(self.widget_13)
        self.label_442.setMaximumSize(QtCore.QSize(16777215, 18))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans Medium")
        font.setPointSize(10)
        self.label_442.setFont(font)
        self.label_442.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_442.setObjectName("label_442")
        self.verticalLayout_277.addWidget(self.label_442)
        self.verticalLayout_277.setStretch(0, 1)
        self.verticalLayout_277.setStretch(1, 1)
        self.verticalLayout_276.addLayout(self.verticalLayout_277)
        self.verticalLayout_276.setStretch(0, 6)
        self.horizontalLayout_35.addLayout(self.verticalLayout_276)
        self.verticalLayout_278 = QtWidgets.QVBoxLayout()
        self.verticalLayout_278.setSpacing(5)
        self.verticalLayout_278.setObjectName("verticalLayout_278")
        self.label_443 = QtWidgets.QLabel(self.widget_13)
        self.label_443.setMinimumSize(QtCore.QSize(100, 100))
        self.label_443.setMaximumSize(QtCore.QSize(16777215, 500))
        self.label_443.setStyleSheet("background-color: rgb(186, 105, 51);\n"
"border-radius:10px;")
        self.label_443.setText("")
        self.label_443.setObjectName("label_443")
        self.verticalLayout_278.addWidget(self.label_443)
        self.verticalLayout_279 = QtWidgets.QVBoxLayout()
        self.verticalLayout_279.setContentsMargins(-1, 0, -1, 10)
        self.verticalLayout_279.setSpacing(10)
        self.verticalLayout_279.setObjectName("verticalLayout_279")
        self.label_444 = QtWidgets.QLabel(self.widget_13)
        self.label_444.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans Medium")
        font.setPointSize(10)
        self.label_444.setFont(font)
        self.label_444.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_444.setObjectName("label_444")
        self.verticalLayout_279.addWidget(self.label_444)
        self.label_445 = QtWidgets.QLabel(self.widget_13)
        self.label_445.setMaximumSize(QtCore.QSize(16777215, 18))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans Medium")
        font.setPointSize(10)
        self.label_445.setFont(font)
        self.label_445.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_445.setObjectName("label_445")
        self.verticalLayout_279.addWidget(self.label_445)
        self.verticalLayout_279.setStretch(0, 1)
        self.verticalLayout_279.setStretch(1, 1)
        self.verticalLayout_278.addLayout(self.verticalLayout_279)
        self.verticalLayout_278.setStretch(0, 6)
        self.horizontalLayout_35.addLayout(self.verticalLayout_278)
        self.verticalLayout_269.addLayout(self.horizontalLayout_35)
        self.verticalLayout_269.setStretch(0, 1)
        self.verticalLayout_269.setStretch(1, 6)
        self.verticalLayout_2.addWidget(self.widget_13)
        self.widget_11 = QtWidgets.QWidget(self.scrollAreaWidgetContents_2)
        self.widget_11.setMinimumSize(QtCore.QSize(0, 400))
        self.widget_11.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.widget_11.setStyleSheet("background-color:rgb(33, 33, 33);\n"
"border-radius:15px;")
        self.widget_11.setObjectName("widget_11")
        self.verticalLayout_225 = QtWidgets.QVBoxLayout(self.widget_11)
        self.verticalLayout_225.setContentsMargins(15, 10, 15, 10)
        self.verticalLayout_225.setSpacing(15)
        self.verticalLayout_225.setObjectName("verticalLayout_225")
        self.label_36 = QtWidgets.QLabel(self.widget_11)
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans ExtraBold")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_36.setFont(font)
        self.label_36.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_36.setMidLineWidth(0)
        self.label_36.setObjectName("label_36")
        self.verticalLayout_225.addWidget(self.label_36)
        self.horizontalLayout_31 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_31.setContentsMargins(-1, 0, -1, 0)
        self.horizontalLayout_31.setSpacing(20)
        self.horizontalLayout_31.setObjectName("horizontalLayout_31")
        self.verticalLayout_226 = QtWidgets.QVBoxLayout()
        self.verticalLayout_226.setContentsMargins(-1, -1, -1, 0)
        self.verticalLayout_226.setSpacing(5)
        self.verticalLayout_226.setObjectName("verticalLayout_226")
        self.label_371 = QtWidgets.QLabel(self.widget_11)
        self.label_371.setMinimumSize(QtCore.QSize(100, 100))
        self.label_371.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.label_371.setStyleSheet("background-color: rgb(186, 105, 51);\n"
"border-radius:10px;")
        self.label_371.setText("")
        self.label_371.setObjectName("label_371")
        self.verticalLayout_226.addWidget(self.label_371)
        self.verticalLayout_227 = QtWidgets.QVBoxLayout()
        self.verticalLayout_227.setContentsMargins(-1, 0, -1, 10)
        self.verticalLayout_227.setSpacing(10)
        self.verticalLayout_227.setObjectName("verticalLayout_227")
        self.label_372 = QtWidgets.QLabel(self.widget_11)
        self.label_372.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans Medium")
        font.setPointSize(10)
        self.label_372.setFont(font)
        self.label_372.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_372.setObjectName("label_372")
        self.verticalLayout_227.addWidget(self.label_372)
        self.label_373 = QtWidgets.QLabel(self.widget_11)
        self.label_373.setMaximumSize(QtCore.QSize(16777215, 18))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans Medium")
        font.setPointSize(10)
        self.label_373.setFont(font)
        self.label_373.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_373.setObjectName("label_373")
        self.verticalLayout_227.addWidget(self.label_373)
        self.verticalLayout_227.setStretch(0, 1)
        self.verticalLayout_226.addLayout(self.verticalLayout_227)
        self.verticalLayout_226.setStretch(0, 1)
        self.horizontalLayout_31.addLayout(self.verticalLayout_226)
        self.verticalLayout_228 = QtWidgets.QVBoxLayout()
        self.verticalLayout_228.setSpacing(5)
        self.verticalLayout_228.setObjectName("verticalLayout_228")
        self.label_374 = QtWidgets.QLabel(self.widget_11)
        self.label_374.setMinimumSize(QtCore.QSize(100, 100))
        self.label_374.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.label_374.setStyleSheet("background-color: rgb(186, 105, 51);\n"
"border-radius:10px;")
        self.label_374.setText("")
        self.label_374.setObjectName("label_374")
        self.verticalLayout_228.addWidget(self.label_374)
        self.verticalLayout_229 = QtWidgets.QVBoxLayout()
        self.verticalLayout_229.setContentsMargins(-1, 0, -1, 10)
        self.verticalLayout_229.setSpacing(10)
        self.verticalLayout_229.setObjectName("verticalLayout_229")
        self.label_375 = QtWidgets.QLabel(self.widget_11)
        self.label_375.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans Medium")
        font.setPointSize(10)
        self.label_375.setFont(font)
        self.label_375.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_375.setObjectName("label_375")
        self.verticalLayout_229.addWidget(self.label_375)
        self.label_376 = QtWidgets.QLabel(self.widget_11)
        self.label_376.setMaximumSize(QtCore.QSize(16777215, 18))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans Medium")
        font.setPointSize(10)
        self.label_376.setFont(font)
        self.label_376.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_376.setObjectName("label_376")
        self.verticalLayout_229.addWidget(self.label_376)
        self.verticalLayout_228.addLayout(self.verticalLayout_229)
        self.verticalLayout_228.setStretch(0, 5)
        self.horizontalLayout_31.addLayout(self.verticalLayout_228)
        self.verticalLayout_230 = QtWidgets.QVBoxLayout()
        self.verticalLayout_230.setSpacing(5)
        self.verticalLayout_230.setObjectName("verticalLayout_230")
        self.label_377 = QtWidgets.QLabel(self.widget_11)
        self.label_377.setMinimumSize(QtCore.QSize(100, 100))
        self.label_377.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.label_377.setStyleSheet("background-color: rgb(186, 105, 51);\n"
"border-radius:10px;")
        self.label_377.setText("")
        self.label_377.setObjectName("label_377")
        self.verticalLayout_230.addWidget(self.label_377)
        self.verticalLayout_231 = QtWidgets.QVBoxLayout()
        self.verticalLayout_231.setContentsMargins(-1, 0, -1, 10)
        self.verticalLayout_231.setSpacing(10)
        self.verticalLayout_231.setObjectName("verticalLayout_231")
        self.label_378 = QtWidgets.QLabel(self.widget_11)
        self.label_378.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans Medium")
        font.setPointSize(10)
        self.label_378.setFont(font)
        self.label_378.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_378.setObjectName("label_378")
        self.verticalLayout_231.addWidget(self.label_378)
        self.label_379 = QtWidgets.QLabel(self.widget_11)
        self.label_379.setMaximumSize(QtCore.QSize(16777215, 18))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans Medium")
        font.setPointSize(10)
        self.label_379.setFont(font)
        self.label_379.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_379.setObjectName("label_379")
        self.verticalLayout_231.addWidget(self.label_379)
        self.verticalLayout_231.setStretch(0, 1)
        self.verticalLayout_231.setStretch(1, 1)
        self.verticalLayout_230.addLayout(self.verticalLayout_231)
        self.verticalLayout_230.setStretch(0, 6)
        self.horizontalLayout_31.addLayout(self.verticalLayout_230)
        self.verticalLayout_232 = QtWidgets.QVBoxLayout()
        self.verticalLayout_232.setSpacing(5)
        self.verticalLayout_232.setObjectName("verticalLayout_232")
        self.label_380 = QtWidgets.QLabel(self.widget_11)
        self.label_380.setMinimumSize(QtCore.QSize(100, 100))
        self.label_380.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.label_380.setStyleSheet("background-color: rgb(186, 105, 51);\n"
"border-radius:10px;")
        self.label_380.setText("")
        self.label_380.setObjectName("label_380")
        self.verticalLayout_232.addWidget(self.label_380)
        self.verticalLayout_233 = QtWidgets.QVBoxLayout()
        self.verticalLayout_233.setContentsMargins(-1, 0, -1, 10)
        self.verticalLayout_233.setSpacing(10)
        self.verticalLayout_233.setObjectName("verticalLayout_233")
        self.label_381 = QtWidgets.QLabel(self.widget_11)
        self.label_381.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans Medium")
        font.setPointSize(10)
        self.label_381.setFont(font)
        self.label_381.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_381.setObjectName("label_381")
        self.verticalLayout_233.addWidget(self.label_381)
        self.label_382 = QtWidgets.QLabel(self.widget_11)
        self.label_382.setMaximumSize(QtCore.QSize(16777215, 18))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans Medium")
        font.setPointSize(10)
        self.label_382.setFont(font)
        self.label_382.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_382.setObjectName("label_382")
        self.verticalLayout_233.addWidget(self.label_382)
        self.verticalLayout_233.setStretch(0, 1)
        self.verticalLayout_233.setStretch(1, 1)
        self.verticalLayout_232.addLayout(self.verticalLayout_233)
        self.verticalLayout_232.setStretch(0, 6)
        self.horizontalLayout_31.addLayout(self.verticalLayout_232)
        self.verticalLayout_234 = QtWidgets.QVBoxLayout()
        self.verticalLayout_234.setSpacing(5)
        self.verticalLayout_234.setObjectName("verticalLayout_234")
        self.label_383 = QtWidgets.QLabel(self.widget_11)
        self.label_383.setMinimumSize(QtCore.QSize(100, 100))
        self.label_383.setMaximumSize(QtCore.QSize(16777215, 500))
        self.label_383.setStyleSheet("background-color: rgb(186, 105, 51);\n"
"border-radius:10px;")
        self.label_383.setText("")
        self.label_383.setObjectName("label_383")
        self.verticalLayout_234.addWidget(self.label_383)
        self.verticalLayout_235 = QtWidgets.QVBoxLayout()
        self.verticalLayout_235.setContentsMargins(-1, 0, -1, 10)
        self.verticalLayout_235.setSpacing(10)
        self.verticalLayout_235.setObjectName("verticalLayout_235")
        self.label_384 = QtWidgets.QLabel(self.widget_11)
        self.label_384.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans Medium")
        font.setPointSize(10)
        self.label_384.setFont(font)
        self.label_384.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_384.setObjectName("label_384")
        self.verticalLayout_235.addWidget(self.label_384)
        self.label_385 = QtWidgets.QLabel(self.widget_11)
        self.label_385.setMaximumSize(QtCore.QSize(16777215, 18))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans Medium")
        font.setPointSize(10)
        self.label_385.setFont(font)
        self.label_385.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_385.setObjectName("label_385")
        self.verticalLayout_235.addWidget(self.label_385)
        self.verticalLayout_235.setStretch(0, 1)
        self.verticalLayout_235.setStretch(1, 1)
        self.verticalLayout_234.addLayout(self.verticalLayout_235)
        self.verticalLayout_234.setStretch(0, 6)
        self.horizontalLayout_31.addLayout(self.verticalLayout_234)
        self.verticalLayout_225.addLayout(self.horizontalLayout_31)
        self.verticalLayout_225.setStretch(0, 1)
        self.verticalLayout_225.setStretch(1, 6)
        self.verticalLayout_2.addWidget(self.widget_11)
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)
        self.verticalLayout_14.addWidget(self.scrollArea_2)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.tab_2)
        self.verticalLayout_9.setSpacing(15)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setSpacing(20)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.verticalFrame = QtWidgets.QFrame(self.tab_2)
        self.verticalFrame.setStyleSheet("background-color:rgb(33, 33, 33);\n"
"border-radius:15px;")
        self.verticalFrame.setObjectName("verticalFrame")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.verticalFrame)
        self.verticalLayout_5.setContentsMargins(21, 7, 12, 15)
        self.verticalLayout_5.setSpacing(10)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label = QtWidgets.QLabel(self.verticalFrame)
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans ExtraBold")
        font.setPointSize(15)
        self.label.setFont(font)
        self.label.setStyleSheet("color: rgb(255, 255, 255);")
        self.label.setObjectName("label")
        self.verticalLayout_5.addWidget(self.label)
        self.pushButton_2 = QtWidgets.QPushButton(self.verticalFrame)
        self.pushButton_2.setMinimumSize(QtCore.QSize(100, 200))
        self.pushButton_2.setMaximumSize(QtCore.QSize(200, 16777215))
        self.pushButton_2.setStyleSheet("background-color: rgb(186, 105, 51);\n"
"border-radius:5px;")
        self.pushButton_2.setText("")
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout_5.addWidget(self.pushButton_2)
        self.verticalLayout_15 = QtWidgets.QVBoxLayout()
        self.verticalLayout_15.setContentsMargins(-1, 0, -1, 0)
        self.verticalLayout_15.setSpacing(0)
        self.verticalLayout_15.setObjectName("verticalLayout_15")
        self.label_2 = QtWidgets.QLabel(self.verticalFrame)
        self.label_2.setMaximumSize(QtCore.QSize(16777215, 42))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans SemiBold")
        font.setPointSize(15)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_2.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_15.addWidget(self.label_2)
        self.label_3 = QtWidgets.QLabel(self.verticalFrame)
        self.label_3.setMaximumSize(QtCore.QSize(16777215, 26))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans Medium")
        font.setPointSize(9)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("color: rgb(196, 196, 196);")
        self.label_3.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_15.addWidget(self.label_3)
        self.verticalLayout_5.addLayout(self.verticalLayout_15)
        self.verticalLayout_5.setStretch(0, 1)
        self.verticalLayout_5.setStretch(1, 10)
        self.verticalLayout_5.setStretch(2, 2)
        self.horizontalLayout_5.addWidget(self.verticalFrame)
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setContentsMargins(15, -1, 5, 5)
        self.verticalLayout_7.setSpacing(15)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.label_6 = QtWidgets.QLabel(self.tab_2)
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans ExtraBold")
        font.setPointSize(15)
        self.label_6.setFont(font)
        self.label_6.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_6.setObjectName("label_6")
        self.verticalLayout_7.addWidget(self.label_6)
        self.horizontalLayout_15 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_15.setObjectName("horizontalLayout_15")
        self.pushButton_8 = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_8.setMinimumSize(QtCore.QSize(0, 65))
        self.pushButton_8.setMaximumSize(QtCore.QSize(70, 80))
        self.pushButton_8.setStyleSheet("background-color: rgb(186, 105, 51);\n"
"border-radius:5px;")
        self.pushButton_8.setText("")
        self.pushButton_8.setObjectName("pushButton_8")
        self.horizontalLayout_15.addWidget(self.pushButton_8)
        self.verticalLayout_18 = QtWidgets.QVBoxLayout()
        self.verticalLayout_18.setSpacing(0)
        self.verticalLayout_18.setObjectName("verticalLayout_18")
        self.label_24 = QtWidgets.QLabel(self.tab_2)
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans SemiBold")
        font.setPointSize(10)
        self.label_24.setFont(font)
        self.label_24.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_24.setObjectName("label_24")
        self.verticalLayout_18.addWidget(self.label_24)
        self.label_28 = QtWidgets.QLabel(self.tab_2)
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans Medium")
        font.setPointSize(8)
        self.label_28.setFont(font)
        self.label_28.setStyleSheet("color: rgb(196, 196, 196);")
        self.label_28.setObjectName("label_28")
        self.verticalLayout_18.addWidget(self.label_28)
        self.horizontalLayout_15.addLayout(self.verticalLayout_18)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_15.addItem(spacerItem1)
        self.label_33 = QtWidgets.QLabel(self.tab_2)
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans Medium")
        self.label_33.setFont(font)
        self.label_33.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_33.setObjectName("label_33")
        self.horizontalLayout_15.addWidget(self.label_33)
        self.horizontalLayout_15.setStretch(0, 1)
        self.horizontalLayout_15.setStretch(1, 2)
        self.horizontalLayout_15.setStretch(2, 3)
        self.horizontalLayout_15.setStretch(3, 1)
        self.verticalLayout_7.addLayout(self.horizontalLayout_15)
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        self.pushButton_7 = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_7.setMinimumSize(QtCore.QSize(0, 65))
        self.pushButton_7.setMaximumSize(QtCore.QSize(70, 80))
        self.pushButton_7.setStyleSheet("background-color: rgb(186, 105, 51);\n"
"border-radius:5px;")
        self.pushButton_7.setText("")
        self.pushButton_7.setObjectName("pushButton_7")
        self.horizontalLayout_14.addWidget(self.pushButton_7)
        self.verticalLayout_17 = QtWidgets.QVBoxLayout()
        self.verticalLayout_17.setSpacing(0)
        self.verticalLayout_17.setObjectName("verticalLayout_17")
        self.label_20 = QtWidgets.QLabel(self.tab_2)
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans SemiBold")
        font.setPointSize(10)
        self.label_20.setFont(font)
        self.label_20.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_20.setObjectName("label_20")
        self.verticalLayout_17.addWidget(self.label_20)
        self.label_21 = QtWidgets.QLabel(self.tab_2)
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans Medium")
        font.setPointSize(8)
        self.label_21.setFont(font)
        self.label_21.setStyleSheet("color: rgb(196, 196, 196);")
        self.label_21.setObjectName("label_21")
        self.verticalLayout_17.addWidget(self.label_21)
        self.horizontalLayout_14.addLayout(self.verticalLayout_17)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_14.addItem(spacerItem2)
        self.label_23 = QtWidgets.QLabel(self.tab_2)
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans Medium")
        self.label_23.setFont(font)
        self.label_23.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_23.setObjectName("label_23")
        self.horizontalLayout_14.addWidget(self.label_23)
        self.horizontalLayout_14.setStretch(0, 1)
        self.horizontalLayout_14.setStretch(1, 2)
        self.horizontalLayout_14.setStretch(2, 3)
        self.horizontalLayout_14.setStretch(3, 1)
        self.verticalLayout_7.addLayout(self.horizontalLayout_14)
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.pushButton_6 = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_6.setMinimumSize(QtCore.QSize(0, 65))
        self.pushButton_6.setMaximumSize(QtCore.QSize(70, 80))
        self.pushButton_6.setStyleSheet("background-color: rgb(186, 105, 51);\n"
"border-radius:5px;")
        self.pushButton_6.setText("")
        self.pushButton_6.setObjectName("pushButton_6")
        self.horizontalLayout_11.addWidget(self.pushButton_6)
        self.verticalLayout_16 = QtWidgets.QVBoxLayout()
        self.verticalLayout_16.setSpacing(0)
        self.verticalLayout_16.setObjectName("verticalLayout_16")
        self.label_17 = QtWidgets.QLabel(self.tab_2)
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans SemiBold")
        font.setPointSize(10)
        self.label_17.setFont(font)
        self.label_17.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_17.setObjectName("label_17")
        self.verticalLayout_16.addWidget(self.label_17)
        self.label_18 = QtWidgets.QLabel(self.tab_2)
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans Medium")
        font.setPointSize(8)
        self.label_18.setFont(font)
        self.label_18.setStyleSheet("color: rgb(196, 196, 196);")
        self.label_18.setObjectName("label_18")
        self.verticalLayout_16.addWidget(self.label_18)
        self.horizontalLayout_11.addLayout(self.verticalLayout_16)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_11.addItem(spacerItem3)
        self.label_19 = QtWidgets.QLabel(self.tab_2)
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans Medium")
        self.label_19.setFont(font)
        self.label_19.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_19.setObjectName("label_19")
        self.horizontalLayout_11.addWidget(self.label_19)
        self.horizontalLayout_11.setStretch(0, 1)
        self.horizontalLayout_11.setStretch(1, 2)
        self.horizontalLayout_11.setStretch(2, 3)
        self.horizontalLayout_11.setStretch(3, 1)
        self.verticalLayout_7.addLayout(self.horizontalLayout_11)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.pushButton_4 = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_4.setMinimumSize(QtCore.QSize(0, 65))
        self.pushButton_4.setMaximumSize(QtCore.QSize(70, 80))
        self.pushButton_4.setStyleSheet("background-color: rgb(186, 105, 51);\n"
"border-radius:5px;")
        self.pushButton_4.setText("")
        self.pushButton_4.setObjectName("pushButton_4")
        self.horizontalLayout_6.addWidget(self.pushButton_4)
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setSpacing(0)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_11 = QtWidgets.QLabel(self.tab_2)
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans SemiBold")
        font.setPointSize(10)
        self.label_11.setFont(font)
        self.label_11.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_11.setObjectName("label_11")
        self.verticalLayout_10.addWidget(self.label_11)
        self.label_12 = QtWidgets.QLabel(self.tab_2)
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans Medium")
        font.setPointSize(8)
        self.label_12.setFont(font)
        self.label_12.setStyleSheet("color: rgb(196, 196, 196);")
        self.label_12.setObjectName("label_12")
        self.verticalLayout_10.addWidget(self.label_12)
        self.horizontalLayout_6.addLayout(self.verticalLayout_10)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem4)
        self.label_13 = QtWidgets.QLabel(self.tab_2)
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans Medium")
        self.label_13.setFont(font)
        self.label_13.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_13.setObjectName("label_13")
        self.horizontalLayout_6.addWidget(self.label_13)
        self.horizontalLayout_6.setStretch(0, 1)
        self.horizontalLayout_6.setStretch(1, 2)
        self.horizontalLayout_6.setStretch(2, 3)
        self.horizontalLayout_6.setStretch(3, 1)
        self.verticalLayout_7.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_5.addLayout(self.verticalLayout_7)
        self.horizontalLayout_5.setStretch(0, 1)
        self.horizontalLayout_5.setStretch(1, 1)
        self.verticalLayout_9.addLayout(self.horizontalLayout_5)
        self.widget_12 = QtWidgets.QWidget(self.tab_2)
        self.widget_12.setMinimumSize(QtCore.QSize(0, 360))
        self.widget_12.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.widget_12.setStyleSheet("background-color:rgb(33, 33, 33);\n"
"border-radius:15px;")
        self.widget_12.setObjectName("widget_12")
        self.verticalLayout_313 = QtWidgets.QVBoxLayout(self.widget_12)
        self.verticalLayout_313.setContentsMargins(15, 10, 15, 10)
        self.verticalLayout_313.setSpacing(15)
        self.verticalLayout_313.setObjectName("verticalLayout_313")
        self.label_44 = QtWidgets.QLabel(self.widget_12)
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans ExtraBold")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_44.setFont(font)
        self.label_44.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_44.setMidLineWidth(0)
        self.label_44.setObjectName("label_44")
        self.verticalLayout_313.addWidget(self.label_44)
        self.horizontalLayout_39 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_39.setContentsMargins(-1, 0, -1, 0)
        self.horizontalLayout_39.setSpacing(20)
        self.horizontalLayout_39.setObjectName("horizontalLayout_39")
        self.verticalLayout_314 = QtWidgets.QVBoxLayout()
        self.verticalLayout_314.setContentsMargins(-1, -1, -1, 0)
        self.verticalLayout_314.setSpacing(5)
        self.verticalLayout_314.setObjectName("verticalLayout_314")
        self.label_491 = QtWidgets.QLabel(self.widget_12)
        self.label_491.setMinimumSize(QtCore.QSize(100, 100))
        self.label_491.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.label_491.setStyleSheet("background-color: rgb(186, 105, 51);\n"
"border-radius:10px;")
        self.label_491.setText("")
        self.label_491.setObjectName("label_491")
        self.verticalLayout_314.addWidget(self.label_491)
        self.verticalLayout_315 = QtWidgets.QVBoxLayout()
        self.verticalLayout_315.setContentsMargins(-1, 0, -1, 10)
        self.verticalLayout_315.setSpacing(10)
        self.verticalLayout_315.setObjectName("verticalLayout_315")
        self.label_492 = QtWidgets.QLabel(self.widget_12)
        self.label_492.setMaximumSize(QtCore.QSize(16777215, 20))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans Medium")
        font.setPointSize(10)
        self.label_492.setFont(font)
        self.label_492.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_492.setObjectName("label_492")
        self.verticalLayout_315.addWidget(self.label_492)
        self.label_493 = QtWidgets.QLabel(self.widget_12)
        self.label_493.setMaximumSize(QtCore.QSize(16777215, 18))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans Medium")
        font.setPointSize(10)
        self.label_493.setFont(font)
        self.label_493.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_493.setObjectName("label_493")
        self.verticalLayout_315.addWidget(self.label_493)
        self.verticalLayout_315.setStretch(0, 1)
        self.verticalLayout_314.addLayout(self.verticalLayout_315)
        self.verticalLayout_314.setStretch(0, 1)
        self.horizontalLayout_39.addLayout(self.verticalLayout_314)
        self.verticalLayout_316 = QtWidgets.QVBoxLayout()
        self.verticalLayout_316.setSpacing(5)
        self.verticalLayout_316.setObjectName("verticalLayout_316")
        self.label_494 = QtWidgets.QLabel(self.widget_12)
        self.label_494.setMinimumSize(QtCore.QSize(100, 100))
        self.label_494.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.label_494.setStyleSheet("background-color: rgb(186, 105, 51);\n"
"border-radius:10px;")
        self.label_494.setText("")
        self.label_494.setObjectName("label_494")
        self.verticalLayout_316.addWidget(self.label_494)
        self.verticalLayout_317 = QtWidgets.QVBoxLayout()
        self.verticalLayout_317.setContentsMargins(-1, 0, -1, 10)
        self.verticalLayout_317.setSpacing(10)
        self.verticalLayout_317.setObjectName("verticalLayout_317")
        self.label_495 = QtWidgets.QLabel(self.widget_12)
        self.label_495.setMaximumSize(QtCore.QSize(16777215, 20))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans Medium")
        font.setPointSize(10)
        self.label_495.setFont(font)
        self.label_495.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_495.setObjectName("label_495")
        self.verticalLayout_317.addWidget(self.label_495)
        self.label_496 = QtWidgets.QLabel(self.widget_12)
        self.label_496.setMaximumSize(QtCore.QSize(16777215, 18))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans Medium")
        font.setPointSize(10)
        self.label_496.setFont(font)
        self.label_496.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_496.setObjectName("label_496")
        self.verticalLayout_317.addWidget(self.label_496)
        self.verticalLayout_316.addLayout(self.verticalLayout_317)
        self.verticalLayout_316.setStretch(0, 5)
        self.horizontalLayout_39.addLayout(self.verticalLayout_316)
        self.verticalLayout_318 = QtWidgets.QVBoxLayout()
        self.verticalLayout_318.setSpacing(5)
        self.verticalLayout_318.setObjectName("verticalLayout_318")
        self.label_497 = QtWidgets.QLabel(self.widget_12)
        self.label_497.setMinimumSize(QtCore.QSize(100, 100))
        self.label_497.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.label_497.setStyleSheet("background-color: rgb(186, 105, 51);\n"
"border-radius:10px;")
        self.label_497.setText("")
        self.label_497.setObjectName("label_497")
        self.verticalLayout_318.addWidget(self.label_497)
        self.verticalLayout_319 = QtWidgets.QVBoxLayout()
        self.verticalLayout_319.setContentsMargins(-1, 0, -1, 10)
        self.verticalLayout_319.setSpacing(10)
        self.verticalLayout_319.setObjectName("verticalLayout_319")
        self.label_498 = QtWidgets.QLabel(self.widget_12)
        self.label_498.setMaximumSize(QtCore.QSize(16777215, 20))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans Medium")
        font.setPointSize(10)
        self.label_498.setFont(font)
        self.label_498.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_498.setObjectName("label_498")
        self.verticalLayout_319.addWidget(self.label_498)
        self.label_499 = QtWidgets.QLabel(self.widget_12)
        self.label_499.setMaximumSize(QtCore.QSize(16777215, 18))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans Medium")
        font.setPointSize(10)
        self.label_499.setFont(font)
        self.label_499.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_499.setObjectName("label_499")
        self.verticalLayout_319.addWidget(self.label_499)
        self.verticalLayout_319.setStretch(0, 1)
        self.verticalLayout_319.setStretch(1, 1)
        self.verticalLayout_318.addLayout(self.verticalLayout_319)
        self.verticalLayout_318.setStretch(0, 6)
        self.horizontalLayout_39.addLayout(self.verticalLayout_318)
        self.verticalLayout_320 = QtWidgets.QVBoxLayout()
        self.verticalLayout_320.setSpacing(5)
        self.verticalLayout_320.setObjectName("verticalLayout_320")
        self.label_500 = QtWidgets.QLabel(self.widget_12)
        self.label_500.setMinimumSize(QtCore.QSize(100, 100))
        self.label_500.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.label_500.setStyleSheet("background-color: rgb(186, 105, 51);\n"
"border-radius:10px;")
        self.label_500.setText("")
        self.label_500.setObjectName("label_500")
        self.verticalLayout_320.addWidget(self.label_500)
        self.verticalLayout_321 = QtWidgets.QVBoxLayout()
        self.verticalLayout_321.setContentsMargins(-1, 0, -1, 10)
        self.verticalLayout_321.setSpacing(10)
        self.verticalLayout_321.setObjectName("verticalLayout_321")
        self.label_501 = QtWidgets.QLabel(self.widget_12)
        self.label_501.setMaximumSize(QtCore.QSize(16777215, 20))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans Medium")
        font.setPointSize(10)
        self.label_501.setFont(font)
        self.label_501.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_501.setObjectName("label_501")
        self.verticalLayout_321.addWidget(self.label_501)
        self.label_502 = QtWidgets.QLabel(self.widget_12)
        self.label_502.setMaximumSize(QtCore.QSize(16777215, 18))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans Medium")
        font.setPointSize(10)
        self.label_502.setFont(font)
        self.label_502.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_502.setObjectName("label_502")
        self.verticalLayout_321.addWidget(self.label_502)
        self.verticalLayout_321.setStretch(0, 1)
        self.verticalLayout_321.setStretch(1, 1)
        self.verticalLayout_320.addLayout(self.verticalLayout_321)
        self.verticalLayout_320.setStretch(0, 6)
        self.horizontalLayout_39.addLayout(self.verticalLayout_320)
        self.verticalLayout_322 = QtWidgets.QVBoxLayout()
        self.verticalLayout_322.setSpacing(5)
        self.verticalLayout_322.setObjectName("verticalLayout_322")
        self.label_503 = QtWidgets.QLabel(self.widget_12)
        self.label_503.setMinimumSize(QtCore.QSize(100, 100))
        self.label_503.setMaximumSize(QtCore.QSize(16777215, 500))
        self.label_503.setStyleSheet("background-color: rgb(186, 105, 51);\n"
"border-radius:10px;")
        self.label_503.setText("")
        self.label_503.setObjectName("label_503")
        self.verticalLayout_322.addWidget(self.label_503)
        self.verticalLayout_323 = QtWidgets.QVBoxLayout()
        self.verticalLayout_323.setContentsMargins(-1, 0, -1, 10)
        self.verticalLayout_323.setSpacing(10)
        self.verticalLayout_323.setObjectName("verticalLayout_323")
        self.label_504 = QtWidgets.QLabel(self.widget_12)
        self.label_504.setMaximumSize(QtCore.QSize(16777215, 20))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans Medium")
        font.setPointSize(10)
        self.label_504.setFont(font)
        self.label_504.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_504.setObjectName("label_504")
        self.verticalLayout_323.addWidget(self.label_504)
        self.label_505 = QtWidgets.QLabel(self.widget_12)
        self.label_505.setMaximumSize(QtCore.QSize(16777215, 18))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans Medium")
        font.setPointSize(10)
        self.label_505.setFont(font)
        self.label_505.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_505.setObjectName("label_505")
        self.verticalLayout_323.addWidget(self.label_505)
        self.verticalLayout_323.setStretch(0, 1)
        self.verticalLayout_323.setStretch(1, 1)
        self.verticalLayout_322.addLayout(self.verticalLayout_323)
        self.verticalLayout_322.setStretch(0, 6)
        self.horizontalLayout_39.addLayout(self.verticalLayout_322)
        self.verticalLayout_313.addLayout(self.horizontalLayout_39)
        self.verticalLayout_313.setStretch(0, 1)
        self.verticalLayout_313.setStretch(1, 6)
        self.verticalLayout_9.addWidget(self.widget_12)
        self.verticalLayout_9.setStretch(0, 2)
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.tab_3)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_13 = QtWidgets.QVBoxLayout()
        self.verticalLayout_13.setContentsMargins(15, -1, 5, 5)
        self.verticalLayout_13.setSpacing(15)
        self.verticalLayout_13.setObjectName("verticalLayout_13")
        self.scrollArea = QtWidgets.QScrollArea(self.tab_3)
        self.scrollArea.setStyleSheet("QScrollArea {\n"
"    /* Ensures the scroll area itself is frameless */\n"
"    border: none;\n"
"    background-color: transparent;\n"
"}\n"
"\n"
"/* 1. Base Scroll Bar Styling (The main vertical bar) */\n"
"QScrollBar:vertical {\n"
"    border: none;\n"
"    background: transparent;\n"
"    /* Make the entire area where the scrollbar sits very narrow */\n"
"    width: 8px; \n"
"    /* The arrows aren\'t typically used in this style, so we hide them */\n"
"    margin: 0px 0 0px 0;\n"
"}\n"
"\n"
"/* 2. Scroll Bar Handle (The movable thumb) */\n"
"QScrollBar::handle:vertical {\n"
"    /* Color and rounded edges for the thumb */\n"
"    background: #555555; /* Dark gray color */\n"
"    min-height: 20px;\n"
"    border-radius: 4px; /* Slightly rounded edges */\n"
"}\n"
"\n"
"/* 3. Handle Hover State */\n"
"QScrollBar::handle:vertical:hover {\n"
"    background: #888888; /* Slightly lighter gray on hover */\n"
"}\n"
"\n"
"/* 4. Scroll Bar Track (The background area behind the thumb) */\n"
"QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
"    background: none;\n"
"}\n"
"\n"
"/* 5. Hiding the Arrows (If they appear) */\n"
"QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n"
"    border: none;\n"
"    width: 0px;\n"
"    height: 0px;\n"
"    background: none;\n"
"}\n"
"\n"
"QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {\n"
"    border: none;\n"
"    background: none;\n"
"}")
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollArea.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, -470, 1019, 1930))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_19 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_19.setSpacing(30)
        self.verticalLayout_19.setObjectName("verticalLayout_19")
        self.label_8 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_8.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans ExtraBold")
        font.setPointSize(28)
        self.label_8.setFont(font)
        self.label_8.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_8.setObjectName("label_8")
        self.verticalLayout_19.addWidget(self.label_8)
        self.horizontalLayout_16 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_16.setSpacing(10)
        self.horizontalLayout_16.setObjectName("horizontalLayout_16")
        self.label_81 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_81.setMaximumSize(QtCore.QSize(70, 16777215))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans SemiBold")
        font.setPointSize(13)
        self.label_81.setFont(font)
        self.label_81.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_81.setObjectName("label_81")
        self.horizontalLayout_16.addWidget(self.label_81)
        self.pushButton_11 = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_11.setMinimumSize(QtCore.QSize(150, 150))
        self.pushButton_11.setMaximumSize(QtCore.QSize(150, 150))
        self.pushButton_11.setStyleSheet("background-color: rgb(186, 105, 51);\n"
"border-radius:5px;")
        self.pushButton_11.setText("")
        self.pushButton_11.setObjectName("pushButton_11")
        self.horizontalLayout_16.addWidget(self.pushButton_11)
        self.verticalLayout_25 = QtWidgets.QVBoxLayout()
        self.verticalLayout_25.setContentsMargins(-1, 20, -1, 20)
        self.verticalLayout_25.setSpacing(0)
        self.verticalLayout_25.setObjectName("verticalLayout_25")
        self.label_22 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_22.setMinimumSize(QtCore.QSize(0, 50))
        self.label_22.setMaximumSize(QtCore.QSize(16777215, 100))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans SemiBold")
        font.setPointSize(15)
        self.label_22.setFont(font)
        self.label_22.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_22.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.label_22.setObjectName("label_22")
        self.verticalLayout_25.addWidget(self.label_22)
        self.label_29 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_29.setMaximumSize(QtCore.QSize(16777215, 100))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans Medium")
        font.setPointSize(10)
        self.label_29.setFont(font)
        self.label_29.setStyleSheet("color: rgb(196, 196, 196);")
        self.label_29.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_29.setObjectName("label_29")
        self.verticalLayout_25.addWidget(self.label_29)
        self.horizontalLayout_16.addLayout(self.verticalLayout_25)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_16.addItem(spacerItem5)
        self.label_30 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_30.setMaximumSize(QtCore.QSize(100, 50))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans Medium")
        font.setPointSize(9)
        self.label_30.setFont(font)
        self.label_30.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_30.setObjectName("label_30")
        self.horizontalLayout_16.addWidget(self.label_30)
        self.horizontalLayout_16.setStretch(0, 1)
        self.horizontalLayout_16.setStretch(1, 3)
        self.horizontalLayout_16.setStretch(2, 3)
        self.horizontalLayout_16.setStretch(3, 1)
        self.horizontalLayout_16.setStretch(4, 1)
        self.verticalLayout_19.addLayout(self.horizontalLayout_16)
        self.horizontalLayout_20 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_20.setSpacing(10)
        self.horizontalLayout_20.setObjectName("horizontalLayout_20")
        self.label_82 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_82.setMaximumSize(QtCore.QSize(70, 16777215))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans SemiBold")
        font.setPointSize(13)
        self.label_82.setFont(font)
        self.label_82.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_82.setObjectName("label_82")
        self.horizontalLayout_20.addWidget(self.label_82)
        self.pushButton_15 = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_15.setMinimumSize(QtCore.QSize(150, 150))
        self.pushButton_15.setMaximumSize(QtCore.QSize(150, 150))
        self.pushButton_15.setStyleSheet("background-color: rgb(186, 105, 51);\n"
"border-radius:5px;")
        self.pushButton_15.setText("")
        self.pushButton_15.setObjectName("pushButton_15")
        self.horizontalLayout_20.addWidget(self.pushButton_15)
        self.verticalLayout_37 = QtWidgets.QVBoxLayout()
        self.verticalLayout_37.setContentsMargins(-1, 20, -1, 20)
        self.verticalLayout_37.setSpacing(0)
        self.verticalLayout_37.setObjectName("verticalLayout_37")
        self.label_50 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_50.setMinimumSize(QtCore.QSize(0, 50))
        self.label_50.setMaximumSize(QtCore.QSize(16777215, 100))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans SemiBold")
        font.setPointSize(15)
        self.label_50.setFont(font)
        self.label_50.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_50.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.label_50.setObjectName("label_50")
        self.verticalLayout_37.addWidget(self.label_50)
        self.label_51 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_51.setMaximumSize(QtCore.QSize(16777215, 100))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans Medium")
        font.setPointSize(10)
        self.label_51.setFont(font)
        self.label_51.setStyleSheet("color: rgb(196, 196, 196);")
        self.label_51.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_51.setObjectName("label_51")
        self.verticalLayout_37.addWidget(self.label_51)
        self.horizontalLayout_20.addLayout(self.verticalLayout_37)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_20.addItem(spacerItem6)
        self.label_68 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_68.setMaximumSize(QtCore.QSize(100, 50))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans Medium")
        font.setPointSize(9)
        self.label_68.setFont(font)
        self.label_68.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_68.setObjectName("label_68")
        self.horizontalLayout_20.addWidget(self.label_68)
        self.horizontalLayout_20.setStretch(0, 1)
        self.horizontalLayout_20.setStretch(1, 12)
        self.horizontalLayout_20.setStretch(2, 3)
        self.horizontalLayout_20.setStretch(3, 1)
        self.horizontalLayout_20.setStretch(4, 1)
        self.verticalLayout_19.addLayout(self.horizontalLayout_20)
        self.horizontalLayout_19 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_19.setSpacing(8)
        self.horizontalLayout_19.setObjectName("horizontalLayout_19")
        self.label_83 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_83.setMaximumSize(QtCore.QSize(70, 16777215))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans SemiBold")
        font.setPointSize(13)
        self.label_83.setFont(font)
        self.label_83.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_83.setObjectName("label_83")
        self.horizontalLayout_19.addWidget(self.label_83)
        self.pushButton_14 = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_14.setMinimumSize(QtCore.QSize(150, 150))
        self.pushButton_14.setMaximumSize(QtCore.QSize(150, 150))
        self.pushButton_14.setStyleSheet("background-color: rgb(186, 105, 51);\n"
"border-radius:5px;")
        self.pushButton_14.setText("")
        self.pushButton_14.setObjectName("pushButton_14")
        self.horizontalLayout_19.addWidget(self.pushButton_14)
        self.verticalLayout_36 = QtWidgets.QVBoxLayout()
        self.verticalLayout_36.setContentsMargins(-1, 20, -1, 20)
        self.verticalLayout_36.setSpacing(0)
        self.verticalLayout_36.setObjectName("verticalLayout_36")
        self.label_47 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_47.setMinimumSize(QtCore.QSize(0, 50))
        self.label_47.setMaximumSize(QtCore.QSize(16777215, 100))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans SemiBold")
        font.setPointSize(15)
        self.label_47.setFont(font)
        self.label_47.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_47.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.label_47.setObjectName("label_47")
        self.verticalLayout_36.addWidget(self.label_47)
        self.label_48 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_48.setMaximumSize(QtCore.QSize(16777215, 100))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans Medium")
        font.setPointSize(10)
        self.label_48.setFont(font)
        self.label_48.setStyleSheet("color: rgb(196, 196, 196);")
        self.label_48.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_48.setObjectName("label_48")
        self.verticalLayout_36.addWidget(self.label_48)
        self.horizontalLayout_19.addLayout(self.verticalLayout_36)
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_19.addItem(spacerItem7)
        self.label_49 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_49.setMaximumSize(QtCore.QSize(100, 50))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans Medium")
        font.setPointSize(9)
        self.label_49.setFont(font)
        self.label_49.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_49.setObjectName("label_49")
        self.horizontalLayout_19.addWidget(self.label_49)
        self.horizontalLayout_19.setStretch(0, 1)
        self.horizontalLayout_19.setStretch(1, 12)
        self.horizontalLayout_19.setStretch(2, 3)
        self.horizontalLayout_19.setStretch(3, 1)
        self.horizontalLayout_19.setStretch(4, 1)
        self.verticalLayout_19.addLayout(self.horizontalLayout_19)
        self.horizontalLayout_29 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_29.setSpacing(8)
        self.horizontalLayout_29.setObjectName("horizontalLayout_29")
        self.label_84 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_84.setMaximumSize(QtCore.QSize(70, 16777215))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans SemiBold")
        font.setPointSize(13)
        self.label_84.setFont(font)
        self.label_84.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_84.setObjectName("label_84")
        self.horizontalLayout_29.addWidget(self.label_84)
        self.pushButton_24 = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_24.setMinimumSize(QtCore.QSize(150, 150))
        self.pushButton_24.setMaximumSize(QtCore.QSize(150, 150))
        self.pushButton_24.setStyleSheet("background-color: rgb(186, 105, 51);\n"
"border-radius:5px;")
        self.pushButton_24.setText("")
        self.pushButton_24.setObjectName("pushButton_24")
        self.horizontalLayout_29.addWidget(self.pushButton_24)
        self.verticalLayout_41 = QtWidgets.QVBoxLayout()
        self.verticalLayout_41.setContentsMargins(-1, 20, -1, 20)
        self.verticalLayout_41.setSpacing(0)
        self.verticalLayout_41.setObjectName("verticalLayout_41")
        self.label_78 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_78.setMinimumSize(QtCore.QSize(0, 50))
        self.label_78.setMaximumSize(QtCore.QSize(16777215, 100))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans SemiBold")
        font.setPointSize(15)
        self.label_78.setFont(font)
        self.label_78.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_78.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.label_78.setObjectName("label_78")
        self.verticalLayout_41.addWidget(self.label_78)
        self.label_79 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_79.setMaximumSize(QtCore.QSize(16777215, 100))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans Medium")
        font.setPointSize(10)
        self.label_79.setFont(font)
        self.label_79.setStyleSheet("color: rgb(196, 196, 196);")
        self.label_79.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_79.setObjectName("label_79")
        self.verticalLayout_41.addWidget(self.label_79)
        self.horizontalLayout_29.addLayout(self.verticalLayout_41)
        spacerItem8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_29.addItem(spacerItem8)
        self.label_80 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_80.setMaximumSize(QtCore.QSize(100, 50))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans Medium")
        font.setPointSize(9)
        self.label_80.setFont(font)
        self.label_80.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_80.setObjectName("label_80")
        self.horizontalLayout_29.addWidget(self.label_80)
        self.horizontalLayout_29.setStretch(0, 1)
        self.horizontalLayout_29.setStretch(1, 12)
        self.horizontalLayout_29.setStretch(2, 3)
        self.horizontalLayout_29.setStretch(3, 1)
        self.horizontalLayout_29.setStretch(4, 1)
        self.verticalLayout_19.addLayout(self.horizontalLayout_29)
        self.horizontalLayout_28 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_28.setSpacing(8)
        self.horizontalLayout_28.setObjectName("horizontalLayout_28")
        self.label_85 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_85.setMaximumSize(QtCore.QSize(70, 16777215))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans SemiBold")
        font.setPointSize(13)
        self.label_85.setFont(font)
        self.label_85.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_85.setObjectName("label_85")
        self.horizontalLayout_28.addWidget(self.label_85)
        self.pushButton_23 = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_23.setMinimumSize(QtCore.QSize(150, 150))
        self.pushButton_23.setMaximumSize(QtCore.QSize(150, 150))
        self.pushButton_23.setStyleSheet("background-color: rgb(186, 105, 51);\n"
"border-radius:5px;")
        self.pushButton_23.setText("")
        self.pushButton_23.setObjectName("pushButton_23")
        self.horizontalLayout_28.addWidget(self.pushButton_23)
        self.verticalLayout_40 = QtWidgets.QVBoxLayout()
        self.verticalLayout_40.setContentsMargins(-1, 20, -1, 20)
        self.verticalLayout_40.setSpacing(0)
        self.verticalLayout_40.setObjectName("verticalLayout_40")
        self.label_75 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_75.setMinimumSize(QtCore.QSize(0, 50))
        self.label_75.setMaximumSize(QtCore.QSize(16777215, 100))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans SemiBold")
        font.setPointSize(15)
        self.label_75.setFont(font)
        self.label_75.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_75.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.label_75.setObjectName("label_75")
        self.verticalLayout_40.addWidget(self.label_75)
        self.label_76 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_76.setMaximumSize(QtCore.QSize(16777215, 100))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans Medium")
        font.setPointSize(10)
        self.label_76.setFont(font)
        self.label_76.setStyleSheet("color: rgb(196, 196, 196);")
        self.label_76.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_76.setObjectName("label_76")
        self.verticalLayout_40.addWidget(self.label_76)
        self.horizontalLayout_28.addLayout(self.verticalLayout_40)
        spacerItem9 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_28.addItem(spacerItem9)
        self.label_77 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_77.setMaximumSize(QtCore.QSize(100, 50))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans Medium")
        font.setPointSize(9)
        self.label_77.setFont(font)
        self.label_77.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_77.setObjectName("label_77")
        self.horizontalLayout_28.addWidget(self.label_77)
        self.horizontalLayout_28.setStretch(0, 1)
        self.horizontalLayout_28.setStretch(1, 12)
        self.horizontalLayout_28.setStretch(2, 3)
        self.horizontalLayout_28.setStretch(3, 1)
        self.horizontalLayout_28.setStretch(4, 1)
        self.verticalLayout_19.addLayout(self.horizontalLayout_28)
        self.horizontalLayout_27 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_27.setSpacing(8)
        self.horizontalLayout_27.setObjectName("horizontalLayout_27")
        self.label_86 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_86.setMaximumSize(QtCore.QSize(70, 16777215))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans SemiBold")
        font.setPointSize(13)
        self.label_86.setFont(font)
        self.label_86.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_86.setObjectName("label_86")
        self.horizontalLayout_27.addWidget(self.label_86)
        self.pushButton_22 = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_22.setMinimumSize(QtCore.QSize(150, 150))
        self.pushButton_22.setMaximumSize(QtCore.QSize(150, 150))
        self.pushButton_22.setStyleSheet("background-color: rgb(186, 105, 51);\n"
"border-radius:5px;")
        self.pushButton_22.setText("")
        self.pushButton_22.setObjectName("pushButton_22")
        self.horizontalLayout_27.addWidget(self.pushButton_22)
        self.verticalLayout_39 = QtWidgets.QVBoxLayout()
        self.verticalLayout_39.setContentsMargins(-1, 20, -1, 20)
        self.verticalLayout_39.setSpacing(0)
        self.verticalLayout_39.setObjectName("verticalLayout_39")
        self.label_72 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_72.setMinimumSize(QtCore.QSize(0, 50))
        self.label_72.setMaximumSize(QtCore.QSize(16777215, 100))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans SemiBold")
        font.setPointSize(15)
        self.label_72.setFont(font)
        self.label_72.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_72.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.label_72.setObjectName("label_72")
        self.verticalLayout_39.addWidget(self.label_72)
        self.label_73 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_73.setMaximumSize(QtCore.QSize(16777215, 100))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans Medium")
        font.setPointSize(10)
        self.label_73.setFont(font)
        self.label_73.setStyleSheet("color: rgb(196, 196, 196);")
        self.label_73.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_73.setObjectName("label_73")
        self.verticalLayout_39.addWidget(self.label_73)
        self.horizontalLayout_27.addLayout(self.verticalLayout_39)
        spacerItem10 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_27.addItem(spacerItem10)
        self.label_74 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_74.setMaximumSize(QtCore.QSize(100, 50))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans Medium")
        font.setPointSize(9)
        self.label_74.setFont(font)
        self.label_74.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_74.setObjectName("label_74")
        self.horizontalLayout_27.addWidget(self.label_74)
        self.horizontalLayout_27.setStretch(0, 1)
        self.horizontalLayout_27.setStretch(1, 12)
        self.horizontalLayout_27.setStretch(2, 3)
        self.horizontalLayout_27.setStretch(3, 1)
        self.horizontalLayout_27.setStretch(4, 1)
        self.verticalLayout_19.addLayout(self.horizontalLayout_27)
        self.horizontalLayout_26 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_26.setSpacing(8)
        self.horizontalLayout_26.setObjectName("horizontalLayout_26")
        self.label_87 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_87.setMaximumSize(QtCore.QSize(70, 16777215))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans SemiBold")
        font.setPointSize(13)
        self.label_87.setFont(font)
        self.label_87.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_87.setObjectName("label_87")
        self.horizontalLayout_26.addWidget(self.label_87)
        self.pushButton_21 = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_21.setMinimumSize(QtCore.QSize(150, 150))
        self.pushButton_21.setMaximumSize(QtCore.QSize(150, 150))
        self.pushButton_21.setStyleSheet("background-color: rgb(186, 105, 51);\n"
"border-radius:5px;")
        self.pushButton_21.setText("")
        self.pushButton_21.setObjectName("pushButton_21")
        self.horizontalLayout_26.addWidget(self.pushButton_21)
        self.verticalLayout_38 = QtWidgets.QVBoxLayout()
        self.verticalLayout_38.setContentsMargins(-1, 20, -1, 20)
        self.verticalLayout_38.setSpacing(0)
        self.verticalLayout_38.setObjectName("verticalLayout_38")
        self.label_69 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_69.setMinimumSize(QtCore.QSize(0, 50))
        self.label_69.setMaximumSize(QtCore.QSize(16777215, 100))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans SemiBold")
        font.setPointSize(15)
        self.label_69.setFont(font)
        self.label_69.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_69.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.label_69.setObjectName("label_69")
        self.verticalLayout_38.addWidget(self.label_69)
        self.label_70 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_70.setMaximumSize(QtCore.QSize(16777215, 100))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans Medium")
        font.setPointSize(10)
        self.label_70.setFont(font)
        self.label_70.setStyleSheet("color: rgb(196, 196, 196);")
        self.label_70.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_70.setObjectName("label_70")
        self.verticalLayout_38.addWidget(self.label_70)
        self.horizontalLayout_26.addLayout(self.verticalLayout_38)
        spacerItem11 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_26.addItem(spacerItem11)
        self.label_71 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_71.setMaximumSize(QtCore.QSize(100, 50))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans Medium")
        font.setPointSize(9)
        self.label_71.setFont(font)
        self.label_71.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_71.setObjectName("label_71")
        self.horizontalLayout_26.addWidget(self.label_71)
        self.horizontalLayout_26.setStretch(0, 1)
        self.horizontalLayout_26.setStretch(1, 12)
        self.horizontalLayout_26.setStretch(2, 3)
        self.horizontalLayout_26.setStretch(3, 1)
        self.horizontalLayout_26.setStretch(4, 1)
        self.verticalLayout_19.addLayout(self.horizontalLayout_26)
        self.horizontalLayout_18 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_18.setSpacing(8)
        self.horizontalLayout_18.setObjectName("horizontalLayout_18")
        self.label_88 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_88.setMaximumSize(QtCore.QSize(70, 16777215))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans SemiBold")
        font.setPointSize(13)
        self.label_88.setFont(font)
        self.label_88.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_88.setObjectName("label_88")
        self.horizontalLayout_18.addWidget(self.label_88)
        self.pushButton_13 = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_13.setMinimumSize(QtCore.QSize(150, 150))
        self.pushButton_13.setMaximumSize(QtCore.QSize(150, 150))
        self.pushButton_13.setStyleSheet("background-color: rgb(186, 105, 51);\n"
"border-radius:5px;")
        self.pushButton_13.setText("")
        self.pushButton_13.setObjectName("pushButton_13")
        self.horizontalLayout_18.addWidget(self.pushButton_13)
        self.verticalLayout_35 = QtWidgets.QVBoxLayout()
        self.verticalLayout_35.setContentsMargins(-1, 20, -1, 20)
        self.verticalLayout_35.setSpacing(0)
        self.verticalLayout_35.setObjectName("verticalLayout_35")
        self.label_35 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_35.setMinimumSize(QtCore.QSize(0, 50))
        self.label_35.setMaximumSize(QtCore.QSize(16777215, 100))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans SemiBold")
        font.setPointSize(15)
        self.label_35.setFont(font)
        self.label_35.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_35.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.label_35.setObjectName("label_35")
        self.verticalLayout_35.addWidget(self.label_35)
        self.label_45 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_45.setMaximumSize(QtCore.QSize(16777215, 100))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans Medium")
        font.setPointSize(10)
        self.label_45.setFont(font)
        self.label_45.setStyleSheet("color: rgb(196, 196, 196);")
        self.label_45.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_45.setObjectName("label_45")
        self.verticalLayout_35.addWidget(self.label_45)
        self.horizontalLayout_18.addLayout(self.verticalLayout_35)
        spacerItem12 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_18.addItem(spacerItem12)
        self.label_46 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_46.setMaximumSize(QtCore.QSize(100, 50))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans Medium")
        font.setPointSize(9)
        self.label_46.setFont(font)
        self.label_46.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_46.setObjectName("label_46")
        self.horizontalLayout_18.addWidget(self.label_46)
        self.horizontalLayout_18.setStretch(0, 1)
        self.horizontalLayout_18.setStretch(1, 12)
        self.horizontalLayout_18.setStretch(2, 3)
        self.horizontalLayout_18.setStretch(3, 1)
        self.horizontalLayout_18.setStretch(4, 1)
        self.verticalLayout_19.addLayout(self.horizontalLayout_18)
        self.horizontalLayout_17 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_17.setSpacing(8)
        self.horizontalLayout_17.setObjectName("horizontalLayout_17")
        self.label_89 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_89.setMaximumSize(QtCore.QSize(70, 16777215))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans SemiBold")
        font.setPointSize(13)
        self.label_89.setFont(font)
        self.label_89.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_89.setObjectName("label_89")
        self.horizontalLayout_17.addWidget(self.label_89)
        self.pushButton_12 = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_12.setMinimumSize(QtCore.QSize(150, 150))
        self.pushButton_12.setMaximumSize(QtCore.QSize(150, 150))
        self.pushButton_12.setStyleSheet("background-color: rgb(186, 105, 51);\n"
"border-radius:5px;")
        self.pushButton_12.setText("")
        self.pushButton_12.setObjectName("pushButton_12")
        self.horizontalLayout_17.addWidget(self.pushButton_12)
        self.verticalLayout_34 = QtWidgets.QVBoxLayout()
        self.verticalLayout_34.setContentsMargins(-1, 20, -1, 20)
        self.verticalLayout_34.setSpacing(0)
        self.verticalLayout_34.setObjectName("verticalLayout_34")
        self.label_31 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_31.setMinimumSize(QtCore.QSize(0, 50))
        self.label_31.setMaximumSize(QtCore.QSize(16777215, 100))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans SemiBold")
        font.setPointSize(15)
        self.label_31.setFont(font)
        self.label_31.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_31.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.label_31.setObjectName("label_31")
        self.verticalLayout_34.addWidget(self.label_31)
        self.label_32 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_32.setMaximumSize(QtCore.QSize(16777215, 100))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans Medium")
        font.setPointSize(10)
        self.label_32.setFont(font)
        self.label_32.setStyleSheet("color: rgb(196, 196, 196);")
        self.label_32.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_32.setObjectName("label_32")
        self.verticalLayout_34.addWidget(self.label_32)
        self.horizontalLayout_17.addLayout(self.verticalLayout_34)
        spacerItem13 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_17.addItem(spacerItem13)
        self.label_34 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_34.setMaximumSize(QtCore.QSize(100, 50))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans Medium")
        font.setPointSize(9)
        self.label_34.setFont(font)
        self.label_34.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_34.setObjectName("label_34")
        self.horizontalLayout_17.addWidget(self.label_34)
        self.horizontalLayout_17.setStretch(0, 1)
        self.horizontalLayout_17.setStretch(1, 12)
        self.horizontalLayout_17.setStretch(2, 3)
        self.horizontalLayout_17.setStretch(3, 1)
        self.horizontalLayout_17.setStretch(4, 1)
        self.verticalLayout_19.addLayout(self.horizontalLayout_17)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setSpacing(8)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.label_90 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_90.setMaximumSize(QtCore.QSize(70, 16777215))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans SemiBold")
        font.setPointSize(13)
        self.label_90.setFont(font)
        self.label_90.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_90.setObjectName("label_90")
        self.horizontalLayout_9.addWidget(self.label_90)
        self.pushButton_5 = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_5.setMinimumSize(QtCore.QSize(150, 150))
        self.pushButton_5.setMaximumSize(QtCore.QSize(150, 150))
        self.pushButton_5.setStyleSheet("background-color: rgb(186, 105, 51);\n"
"border-radius:5px;")
        self.pushButton_5.setText("")
        self.pushButton_5.setObjectName("pushButton_5")
        self.horizontalLayout_9.addWidget(self.pushButton_5)
        self.verticalLayout_23 = QtWidgets.QVBoxLayout()
        self.verticalLayout_23.setContentsMargins(-1, 20, -1, 20)
        self.verticalLayout_23.setSpacing(0)
        self.verticalLayout_23.setObjectName("verticalLayout_23")
        self.label_14 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_14.setMinimumSize(QtCore.QSize(0, 50))
        self.label_14.setMaximumSize(QtCore.QSize(16777215, 100))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans SemiBold")
        font.setPointSize(15)
        self.label_14.setFont(font)
        self.label_14.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_14.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.label_14.setObjectName("label_14")
        self.verticalLayout_23.addWidget(self.label_14)
        self.label_15 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_15.setMaximumSize(QtCore.QSize(16777215, 100))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans Medium")
        font.setPointSize(10)
        self.label_15.setFont(font)
        self.label_15.setStyleSheet("color: rgb(196, 196, 196);")
        self.label_15.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_15.setObjectName("label_15")
        self.verticalLayout_23.addWidget(self.label_15)
        self.horizontalLayout_9.addLayout(self.verticalLayout_23)
        spacerItem14 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem14)
        self.label_16 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_16.setMaximumSize(QtCore.QSize(100, 50))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans Medium")
        font.setPointSize(9)
        self.label_16.setFont(font)
        self.label_16.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_16.setObjectName("label_16")
        self.horizontalLayout_9.addWidget(self.label_16)
        self.horizontalLayout_9.setStretch(0, 1)
        self.horizontalLayout_9.setStretch(1, 12)
        self.horizontalLayout_9.setStretch(2, 3)
        self.horizontalLayout_9.setStretch(3, 1)
        self.horizontalLayout_9.setStretch(4, 1)
        self.verticalLayout_19.addLayout(self.horizontalLayout_9)
        self.verticalLayout_19.setStretch(0, 5)
        self.verticalLayout_19.setStretch(1, 1)
        self.verticalLayout_19.setStretch(2, 1)
        self.verticalLayout_19.setStretch(3, 1)
        self.verticalLayout_19.setStretch(4, 1)
        self.verticalLayout_19.setStretch(5, 1)
        self.verticalLayout_19.setStretch(6, 1)
        self.verticalLayout_19.setStretch(7, 1)
        self.verticalLayout_19.setStretch(8, 1)
        self.verticalLayout_19.setStretch(9, 1)
        self.verticalLayout_19.setStretch(10, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_13.addWidget(self.scrollArea)
        self.verticalLayout.addLayout(self.verticalLayout_13)
        self.tabWidget.addTab(self.tab_3, "")
        self.verticalLayout_11.addWidget(self.tabWidget)
        self.horizontalLayout_2.addLayout(self.verticalLayout_11)
        self.verticalLayout_12 = QtWidgets.QVBoxLayout()
        self.verticalLayout_12.setContentsMargins(-1, 0, -1, -1)
        self.verticalLayout_12.setSpacing(15)
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.tabWidget_2 = QtWidgets.QTabWidget(Form)
        self.tabWidget_2.setStyleSheet("QTabWidget::pane {\n"
"    background: rgb(20, 20, 20);\n"
"}\n"
"\n"
"QTabBar::tab {\n"
"    height: 0px;       /* hides the tabs completely */\n"
"    width: 0px;\n"
"    margin: 0px;\n"
"    padding: 0px;\n"
"    border: none;\n"
"}\n"
"\n"
"\n"
"QTabBar::tab:selected {\n"
"    background: rgb(45, 45, 45);\n"
"    color: white;\n"
"}\n"
"\n"
"QTabBar::tab:hover {\n"
"    background: rgb(60, 60, 60);\n"
"}")
        self.tabWidget_2.setObjectName("tabWidget_2")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.verticalLayout_20 = QtWidgets.QVBoxLayout(self.tab_4)
        self.verticalLayout_20.setSpacing(20)
        self.verticalLayout_20.setObjectName("verticalLayout_20")
        spacerItem15 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_20.addItem(spacerItem15)
        self.label_7 = QtWidgets.QLabel(self.tab_4)
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans ExtraBold")
        font.setPointSize(15)
        self.label_7.setFont(font)
        self.label_7.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.verticalLayout_20.addWidget(self.label_7)
        self.pushButton_3 = QtWidgets.QPushButton(self.tab_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_3.sizePolicy().hasHeightForWidth())
        self.pushButton_3.setSizePolicy(sizePolicy)
        self.pushButton_3.setMinimumSize(QtCore.QSize(180, 44))
        self.pushButton_3.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans SemiBold")
        font.setPointSize(9)
        font.setKerning(True)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setStyleSheet("color: rgb(255, 255, 255);\n"
"border: 2px solid rgb(255, 255, 255);\n"
"border-radius: 22px;\n"
"")
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout_20.addWidget(self.pushButton_3, 0, QtCore.Qt.AlignHCenter)
        spacerItem16 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_20.addItem(spacerItem16)
        self.verticalLayout_20.setStretch(0, 1)
        self.verticalLayout_20.setStretch(2, 2)
        self.verticalLayout_20.setStretch(3, 1)
        self.tabWidget_2.addTab(self.tab_4, "")
        self.tab_5 = QtWidgets.QWidget()
        self.tab_5.setObjectName("tab_5")
        self.verticalLayout_33 = QtWidgets.QVBoxLayout(self.tab_5)
        self.verticalLayout_33.setObjectName("verticalLayout_33")
        self.widget_8 = QtWidgets.QWidget(self.tab_5)
        self.widget_8.setStyleSheet("background-color:rgb(33, 33, 33);\n"
"border-radius:15px;")
        self.widget_8.setObjectName("widget_8")
        self.verticalLayout_26 = QtWidgets.QVBoxLayout(self.widget_8)
        self.verticalLayout_26.setContentsMargins(-1, 12, -1, -1)
        self.verticalLayout_26.setObjectName("verticalLayout_26")
        self.label_52 = QtWidgets.QLabel(self.widget_8)
        self.label_52.setMinimumSize(QtCore.QSize(210, 210))
        self.label_52.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.label_52.setStyleSheet("background-color: rgb(235, 235, 235);\n"
"border-radius:10px;")
        self.label_52.setText("")
        self.label_52.setScaledContents(True)
        self.label_52.setObjectName("label_52")
        self.verticalLayout_26.addWidget(self.label_52)
        self.label_53 = QtWidgets.QLabel(self.widget_8)
        self.label_53.setMaximumSize(QtCore.QSize(16777215, 37))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans ExtraBold")
        font.setPointSize(14)
        self.label_53.setFont(font)
        self.label_53.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_53.setObjectName("label_53")
        self.verticalLayout_26.addWidget(self.label_53)
        self.label_54 = QtWidgets.QLabel(self.widget_8)
        self.label_54.setMaximumSize(QtCore.QSize(16777215, 20))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans Medium")
        font.setPointSize(8)
        self.label_54.setFont(font)
        self.label_54.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_54.setObjectName("label_54")
        self.verticalLayout_26.addWidget(self.label_54)
        self.verticalLayout_26.setStretch(0, 6)
        self.verticalLayout_26.setStretch(1, 1)
        self.verticalLayout_26.setStretch(2, 1)
        self.verticalLayout_33.addWidget(self.widget_8)
        self.widget_9 = QtWidgets.QWidget(self.tab_5)
        self.widget_9.setStyleSheet("background-color:rgb(33, 33, 33);\n"
"border-radius:15px;")
        self.widget_9.setObjectName("widget_9")
        self.verticalLayout_27 = QtWidgets.QVBoxLayout(self.widget_9)
        self.verticalLayout_27.setContentsMargins(15, -1, 15, 30)
        self.verticalLayout_27.setSpacing(15)
        self.verticalLayout_27.setObjectName("verticalLayout_27")
        self.label_55 = QtWidgets.QLabel(self.widget_9)
        self.label_55.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans SemiBold")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_55.setFont(font)
        self.label_55.setStyleSheet("color:rgb(255, 255, 255);")
        self.label_55.setObjectName("label_55")
        self.verticalLayout_27.addWidget(self.label_55)
        self.horizontalLayout_21 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_21.setSpacing(15)
        self.horizontalLayout_21.setObjectName("horizontalLayout_21")
        self.pushButton_16 = QtWidgets.QPushButton(self.widget_9)
        self.pushButton_16.setMinimumSize(QtCore.QSize(65, 65))
        self.pushButton_16.setMaximumSize(QtCore.QSize(70, 80))
        self.pushButton_16.setStyleSheet("background-color: transparent;\n"
"border-radius:5px;")
        self.pushButton_16.setText("")
        self.pushButton_16.setObjectName("pushButton_16")
        self.horizontalLayout_21.addWidget(self.pushButton_16)
        self.verticalLayout_28 = QtWidgets.QVBoxLayout()
        self.verticalLayout_28.setSpacing(0)
        self.verticalLayout_28.setObjectName("verticalLayout_28")
        self.label_56 = QtWidgets.QLabel(self.widget_9)
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans SemiBold")
        font.setPointSize(10)
        self.label_56.setFont(font)
        self.label_56.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_56.setObjectName("label_56")
        self.verticalLayout_28.addWidget(self.label_56)
        self.label_57 = QtWidgets.QLabel(self.widget_9)
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans Medium")
        font.setPointSize(8)
        self.label_57.setFont(font)
        self.label_57.setStyleSheet("color: rgb(196, 196, 196);")
        self.label_57.setObjectName("label_57")
        self.verticalLayout_28.addWidget(self.label_57)
        self.horizontalLayout_21.addLayout(self.verticalLayout_28)
        spacerItem17 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_21.addItem(spacerItem17)
        self.horizontalLayout_21.setStretch(0, 1)
        self.horizontalLayout_21.setStretch(1, 2)
        self.horizontalLayout_21.setStretch(2, 3)
        self.verticalLayout_27.addLayout(self.horizontalLayout_21)
        self.horizontalLayout_22 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_22.setSpacing(15)
        self.horizontalLayout_22.setObjectName("horizontalLayout_22")
        self.pushButton_17 = QtWidgets.QPushButton(self.widget_9)
        self.pushButton_17.setMinimumSize(QtCore.QSize(65, 65))
        self.pushButton_17.setMaximumSize(QtCore.QSize(70, 80))
        self.pushButton_17.setStyleSheet("background-color: transparent;\n"
"border-radius:5px;")
        self.pushButton_17.setText("")
        self.pushButton_17.setObjectName("pushButton_17")
        self.horizontalLayout_22.addWidget(self.pushButton_17)
        self.verticalLayout_29 = QtWidgets.QVBoxLayout()
        self.verticalLayout_29.setSpacing(0)
        self.verticalLayout_29.setObjectName("verticalLayout_29")
        self.label_58 = QtWidgets.QLabel(self.widget_9)
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans SemiBold")
        font.setPointSize(10)
        self.label_58.setFont(font)
        self.label_58.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_58.setObjectName("label_58")
        self.verticalLayout_29.addWidget(self.label_58)
        self.label_59 = QtWidgets.QLabel(self.widget_9)
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans Medium")
        font.setPointSize(8)
        self.label_59.setFont(font)
        self.label_59.setStyleSheet("color: rgb(196, 196, 196);")
        self.label_59.setObjectName("label_59")
        self.verticalLayout_29.addWidget(self.label_59)
        self.horizontalLayout_22.addLayout(self.verticalLayout_29)
        spacerItem18 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_22.addItem(spacerItem18)
        self.horizontalLayout_22.setStretch(0, 1)
        self.horizontalLayout_22.setStretch(1, 2)
        self.horizontalLayout_22.setStretch(2, 3)
        self.verticalLayout_27.addLayout(self.horizontalLayout_22)
        self.horizontalLayout_23 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_23.setSpacing(15)
        self.horizontalLayout_23.setObjectName("horizontalLayout_23")
        self.pushButton_18 = QtWidgets.QPushButton(self.widget_9)
        self.pushButton_18.setMinimumSize(QtCore.QSize(65, 65))
        self.pushButton_18.setMaximumSize(QtCore.QSize(70, 80))
        self.pushButton_18.setStyleSheet("background-color: transparent;\n"
"border-radius:5px;")
        self.pushButton_18.setText("")
        self.pushButton_18.setObjectName("pushButton_18")
        self.horizontalLayout_23.addWidget(self.pushButton_18)
        self.verticalLayout_30 = QtWidgets.QVBoxLayout()
        self.verticalLayout_30.setSpacing(0)
        self.verticalLayout_30.setObjectName("verticalLayout_30")
        self.label_60 = QtWidgets.QLabel(self.widget_9)
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans SemiBold")
        font.setPointSize(10)
        self.label_60.setFont(font)
        self.label_60.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_60.setObjectName("label_60")
        self.verticalLayout_30.addWidget(self.label_60)
        self.label_62 = QtWidgets.QLabel(self.widget_9)
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans Medium")
        font.setPointSize(8)
        self.label_62.setFont(font)
        self.label_62.setStyleSheet("color: rgb(196, 196, 196);")
        self.label_62.setObjectName("label_62")
        self.verticalLayout_30.addWidget(self.label_62)
        self.horizontalLayout_23.addLayout(self.verticalLayout_30)
        spacerItem19 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_23.addItem(spacerItem19)
        self.horizontalLayout_23.setStretch(0, 1)
        self.horizontalLayout_23.setStretch(1, 2)
        self.horizontalLayout_23.setStretch(2, 3)
        self.verticalLayout_27.addLayout(self.horizontalLayout_23)
        self.horizontalLayout_24 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_24.setSpacing(15)
        self.horizontalLayout_24.setObjectName("horizontalLayout_24")
        self.pushButton_19 = QtWidgets.QPushButton(self.widget_9)
        self.pushButton_19.setMinimumSize(QtCore.QSize(65, 65))
        self.pushButton_19.setMaximumSize(QtCore.QSize(70, 80))
        self.pushButton_19.setStyleSheet("background-color: transparent;\n"
"border-radius:5px;")
        self.pushButton_19.setText("")
        self.pushButton_19.setObjectName("pushButton_19")
        self.horizontalLayout_24.addWidget(self.pushButton_19)
        self.verticalLayout_31 = QtWidgets.QVBoxLayout()
        self.verticalLayout_31.setSpacing(0)
        self.verticalLayout_31.setObjectName("verticalLayout_31")
        self.label_63 = QtWidgets.QLabel(self.widget_9)
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans SemiBold")
        font.setPointSize(10)
        self.label_63.setFont(font)
        self.label_63.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_63.setObjectName("label_63")
        self.verticalLayout_31.addWidget(self.label_63)
        self.label_64 = QtWidgets.QLabel(self.widget_9)
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans Medium")
        font.setPointSize(8)
        self.label_64.setFont(font)
        self.label_64.setStyleSheet("color: rgb(196, 196, 196);")
        self.label_64.setObjectName("label_64")
        self.verticalLayout_31.addWidget(self.label_64)
        self.horizontalLayout_24.addLayout(self.verticalLayout_31)
        spacerItem20 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_24.addItem(spacerItem20)
        self.horizontalLayout_24.setStretch(0, 1)
        self.horizontalLayout_24.setStretch(1, 2)
        self.horizontalLayout_24.setStretch(2, 3)
        self.verticalLayout_27.addLayout(self.horizontalLayout_24)
        self.horizontalLayout_25 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_25.setSpacing(15)
        self.horizontalLayout_25.setObjectName("horizontalLayout_25")
        self.pushButton_20 = QtWidgets.QPushButton(self.widget_9)
        self.pushButton_20.setMinimumSize(QtCore.QSize(65, 65))
        self.pushButton_20.setMaximumSize(QtCore.QSize(70, 80))
        self.pushButton_20.setStyleSheet("background-color: transparent;\n"
"border-radius:5px;")
        self.pushButton_20.setText("")
        self.pushButton_20.setObjectName("pushButton_20")
        self.horizontalLayout_25.addWidget(self.pushButton_20)
        self.verticalLayout_32 = QtWidgets.QVBoxLayout()
        self.verticalLayout_32.setSpacing(0)
        self.verticalLayout_32.setObjectName("verticalLayout_32")
        self.label_65 = QtWidgets.QLabel(self.widget_9)
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans SemiBold")
        font.setPointSize(10)
        self.label_65.setFont(font)
        self.label_65.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_65.setObjectName("label_65")
        self.verticalLayout_32.addWidget(self.label_65)
        self.label_67 = QtWidgets.QLabel(self.widget_9)
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans Medium")
        font.setPointSize(8)
        self.label_67.setFont(font)
        self.label_67.setStyleSheet("color: rgb(196, 196, 196);")
        self.label_67.setObjectName("label_67")
        self.verticalLayout_32.addWidget(self.label_67)
        self.horizontalLayout_25.addLayout(self.verticalLayout_32)
        spacerItem21 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_25.addItem(spacerItem21)
        self.horizontalLayout_25.setStretch(0, 1)
        self.horizontalLayout_25.setStretch(1, 2)
        self.horizontalLayout_25.setStretch(2, 3)
        self.verticalLayout_27.addLayout(self.horizontalLayout_25)
        self.verticalLayout_27.setStretch(0, 1)
        self.verticalLayout_33.addWidget(self.widget_9)
        self.tabWidget_2.addTab(self.tab_5, "")
        self.verticalLayout_12.addWidget(self.tabWidget_2)
        self.horizontalLayout_2.addLayout(self.verticalLayout_12)
        self.horizontalLayout_2.setStretch(0, 8)
        self.horizontalLayout_2.setStretch(1, 1)
        self.verticalLayout_6.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_13.setContentsMargins(6, -1, -1, -1)
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setMinimumSize(QtCore.QSize(80, 80))
        self.pushButton.setMaximumSize(QtCore.QSize(80, 80))
        self.pushButton.setStyleSheet("background-color: rgb(186, 105, 51);\n"
"border-radius:5px;")
        self.pushButton.setText("")
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(lambda: self.tabWidget_2.setCurrentIndex(1))
        self.horizontalLayout_13.addWidget(self.pushButton)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setContentsMargins(5, 0, -1, 10)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        spacerItem22 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem22)
        self.label_4 = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans Medium")
        font.setPointSize(9)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_4.setObjectName("label_4")
        self.verticalLayout_4.addWidget(self.label_4)
        self.label_5 = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans Medium")
        font.setPointSize(8)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_5.setObjectName("label_5")
        self.verticalLayout_4.addWidget(self.label_5)
        spacerItem23 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem23)
        self.verticalLayout_4.setStretch(1, 1)
        self.verticalLayout_4.setStretch(2, 1)
        self.horizontalLayout_13.addLayout(self.verticalLayout_4)
        self.horizontalLayout_13.setStretch(0, 2)
        self.horizontalLayout_13.setStretch(1, 1)
        self.horizontalLayout_7.addLayout(self.horizontalLayout_13)
        self.verticalLayout_8 = QtWidgets.QVBoxLayout()
        self.verticalLayout_8.setContentsMargins(-1, -1, 0, -1)
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setContentsMargins(-1, 2, 0, 5)
        self.horizontalLayout_8.setSpacing(30)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        spacerItem24 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem24)
        self.random = QtWidgets.QLabel(Form)
        self.random.setMaximumSize(QtCore.QSize(30, 30))
        self.random.setText("")
        self.random.setPixmap(QtGui.QPixmap(os.path.join(self.media_path, "shuffle.png")))
        self.random.setScaledContents(True)
        self.random.setObjectName("random")
        self.horizontalLayout_8.addWidget(self.random)
        self.backward = QtWidgets.QLabel(Form)
        self.backward.setMaximumSize(QtCore.QSize(40, 40))
        self.backward.setText("")
        self.backward.setPixmap(QtGui.QPixmap(os.path.join(self.media_path, "backward.png")))
        self.backward.setScaledContents(True)
        self.backward.setObjectName("backward")
        self.horizontalLayout_8.addWidget(self.backward)
        self.pause_play = QtWidgets.QLabel(Form)
        self.pause_play.setMaximumSize(QtCore.QSize(40, 40))
        self.pause_play.setText("")
        self.pause_play.setPixmap(QtGui.QPixmap(os.path.join(self.media_path, "pause_button.png")))
        self.pause_play.setScaledContents(True)
        self.pause_play.setObjectName("pause_play")
        self.horizontalLayout_8.addWidget(self.pause_play)
        self.fastforward = QtWidgets.QLabel(Form)
        self.fastforward.setMaximumSize(QtCore.QSize(40, 40))
        self.fastforward.setText("")
        self.fastforward.setPixmap(QtGui.QPixmap(os.path.join(self.media_path, "forward_button.png")))
        self.fastforward.setScaledContents(True)
        self.fastforward.setObjectName("fastforward")
        self.horizontalLayout_8.addWidget(self.fastforward)
        self.repeat = QtWidgets.QLabel(Form)
        self.repeat.setMaximumSize(QtCore.QSize(30, 30))
        self.repeat.setText("")
        self.repeat.setPixmap(QtGui.QPixmap(os.path.join(self.media_path, "repeat.png")))
        self.repeat.setScaledContents(True)
        self.repeat.setObjectName("repeat")
        self.horizontalLayout_8.addWidget(self.repeat)
        spacerItem25 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem25)
        self.horizontalLayout_8.setStretch(0, 1)
        self.horizontalLayout_8.setStretch(1, 1)
        self.horizontalLayout_8.setStretch(2, 1)
        self.horizontalLayout_8.setStretch(3, 1)
        self.horizontalLayout_8.setStretch(4, 1)
        self.horizontalLayout_8.setStretch(5, 1)
        self.horizontalLayout_8.setStretch(6, 1)
        self.verticalLayout_8.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setContentsMargins(-1, -1, -1, 0)
        self.horizontalLayout_10.setSpacing(16)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        spacerItem26 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem26)
        self.label_66 = QtWidgets.QLabel(Form)
        self.label_66.setMaximumSize(QtCore.QSize(48, 16777215))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans Medium")
        font.setPointSize(8)
        font.setBold(False)
        font.setWeight(50)
        self.label_66.setFont(font)
        self.label_66.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_66.setObjectName("label_66")
        self.horizontalLayout_10.addWidget(self.label_66)
        self.Musicslider = QtWidgets.QSlider(Form)
        self.Musicslider.setMinimumSize(QtCore.QSize(500, 0))
        self.Musicslider.setMaximumSize(QtCore.QSize(600, 20))
        self.Musicslider.setStyleSheet("QSlider::groove:horizontal {\n"
"    background: #282828;\n"
"    height: 4px;\n"
"    border-radius: 2px;\n"
"}\n"
"\n"
"QSlider::sub-page:horizontal {\n"
"    background: #FFFFFF;\n"
"    height: 4px;\n"
"    border-radius: 2px;\n"
"}\n"
"\n"
"QSlider::add-page:horizontal {\n"
"    background: #606060;\n"
"    height: 4px;\n"
"    border-radius: 2px;\n"
"}\n"
"\n"
"QSlider::handle:horizontal {\n"
"    background: #FFFFFF;\n"
"    border: 1px solid #FFFFFF;\n"
"    width: 12px;\n"
"    height: 12px;\n"
"    margin: -5px 0;\n"
"    border-radius: 6px;\n"
"}\n"
"\n"
"QSlider::handle:horizontal:hover {\n"
"    background: #F0F0F0;\n"
"    width: 14px;\n"
"    height: 14px;\n"
"    margin: -6px 0;\n"
"}")
        self.Musicslider.setOrientation(QtCore.Qt.Horizontal)
        self.Musicslider.setObjectName("Musicslider")
        self.horizontalLayout_10.addWidget(self.Musicslider)
        self.maxduration = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans Medium")
        font.setPointSize(8)
        font.setBold(False)
        font.setWeight(50)
        self.maxduration.setFont(font)
        self.maxduration.setStyleSheet("color: rgb(255, 255, 255);")
        self.maxduration.setObjectName("maxduration")
        self.horizontalLayout_10.addWidget(self.maxduration)
        spacerItem27 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem27)
        self.horizontalLayout_10.setStretch(0, 1)
        self.horizontalLayout_10.setStretch(1, 1)
        self.horizontalLayout_10.setStretch(2, 1)
        self.horizontalLayout_10.setStretch(3, 1)
        self.verticalLayout_8.addLayout(self.horizontalLayout_10)
        self.verticalLayout_8.setStretch(0, 3)
        self.verticalLayout_8.setStretch(1, 2)
        self.horizontalLayout_7.addLayout(self.verticalLayout_8)
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_12.setContentsMargins(-1, -1, 10, -1)
        self.horizontalLayout_12.setSpacing(10)
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.volumeicon = QtWidgets.QLabel(Form)
        self.volumeicon.setMaximumSize(QtCore.QSize(30, 30))
        self.volumeicon.setSizeIncrement(QtCore.QSize(10, 0))
        self.volumeicon.setText("")
        self.volumeicon.setPixmap(QtGui.QPixmap(os.path.join(self.media_path, "volume.svg")))
        self.volumeicon.setScaledContents(True)
        self.volumeicon.setObjectName("volumeicon")
        self.horizontalLayout_12.addWidget(self.volumeicon)
        self.Volumeslider = QtWidgets.QSlider(Form)
        self.Volumeslider.setMaximumSize(QtCore.QSize(150, 20))
        self.Volumeslider.setSizeIncrement(QtCore.QSize(0, 0))
        self.Volumeslider.setStyleSheet("QSlider::groove:horizontal {\n"
"    background: #282828;\n"
"    height: 4px;\n"
"    border-radius: 2px;\n"
"}\n"
"\n"
"QSlider::sub-page:horizontal {\n"
"    background: #FFFFFF;\n"
"    height: 4px;\n"
"    border-radius: 2px;\n"
"}\n"
"\n"
"QSlider::add-page:horizontal {\n"
"    background: #606060;\n"
"    height: 4px;\n"
"    border-radius: 2px;\n"
"}\n"
"\n"
"QSlider::handle:horizontal {\n"
"    background: #FFFFFF;\n"
"    border: 1px solid #FFFFFF;\n"
"    width: 12px;\n"
"    height: 12px;\n"
"    margin: -5px 0;\n"
"    border-radius: 6px;\n"
"}\n"
"\n"
"QSlider::handle:horizontal:hover {\n"
"    background: #F0F0F0;\n"
"    width: 14px;\n"
"    height: 14px;\n"
"    margin: -6px 0;\n"
"}")
        self.Volumeslider.setOrientation(QtCore.Qt.Horizontal)
        self.Volumeslider.setObjectName("Volumeslider")
        self.horizontalLayout_12.addWidget(self.Volumeslider)
        self.label_61 = QtWidgets.QLabel(Form)
        self.label_61.setMaximumSize(QtCore.QSize(40, 30))
        self.label_61.setText("")
        self.label_61.setPixmap(QtGui.QPixmap(os.path.join(self.media_path, "fullscreen.svg")))
        self.label_61.setScaledContents(True)
        self.label_61.setObjectName("label_61")
        self.horizontalLayout_12.addWidget(self.label_61)
        self.horizontalLayout_7.addLayout(self.horizontalLayout_12)
        self.horizontalLayout_7.setStretch(0, 1)
        self.horizontalLayout_7.setStretch(1, 5)
        self.horizontalLayout_7.setStretch(2, 1)
        self.verticalLayout_6.addLayout(self.horizontalLayout_7)
        self.verticalLayout_6.setStretch(0, 1)
        self.verticalLayout_6.setStretch(1, 8)
        self.verticalLayout_6.setStretch(2, 1)
        self.gridLayout.addLayout(self.verticalLayout_6, 0, 0, 1, 1)

        self.fullscreen = False  # Track fullscreen state

        def toggle_fullscreen():
            if self.fullscreen:
                Form.showMaximized()
                self.fullscreen = False
                # Change fullscreen icon back to fullscreen.svg
                self.label_61.setPixmap(QtGui.QPixmap(os.path.join(self.media_path, "fullscreen.svg")))
            else:
                Form.showFullScreen()
                self.fullscreen = True
                # Change fullscreen icon to restore.svg or similar
                self.label_61.setPixmap(QtGui.QPixmap(os.path.join(self.media_path, "normal.png")))

        self.label_61.mousePressEvent = lambda event: toggle_fullscreen() if event.button() == QtCore.Qt.LeftButton else None

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget_2.setCurrentIndex(0)

        # Connect search button click to switch to tab 2 in tabWidget_2
        self.pushButton_3.clicked.connect(lambda: self.tabWidget_2.setCurrentIndex(1))

        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton_9.setToolTip(_translate("Form", "home"))
        self.pushButton_10.setToolTip(_translate("Form", "Detection"))
        self.random.setToolTip(_translate("Form", "Random"))
        self.backward.setToolTip(_translate("Form", "previous"))
        self.repeat.setToolTip(_translate("Form", "repeat"))
        self.backward.setToolTip(_translate("Form", "previous"))
        self.lineEdit_2.setPlaceholderText(_translate("Form", "Search by Song"))
        self.label_41.setText(_translate("Form", "Made for you"))
        self.label_447.setText(_translate("Form", "Title"))
        self.label_448.setText(_translate("Form", "Artist"))
        self.label_450.setText(_translate("Form", "Title"))
        self.label_451.setText(_translate("Form", "Artist"))
        self.label_453.setText(_translate("Form", "Title"))
        self.label_454.setText(_translate("Form", "Artist"))
        self.label_456.setText(_translate("Form", "Title"))
        self.label_457.setText(_translate("Form", "Artist"))
        self.label_459.setText(_translate("Form", "Title"))
        self.label_460.setText(_translate("Form", "Artist"))
        self.label_40.setText(_translate("Form", "Recommended for today"))
        self.label_432.setText(_translate("Form", "Title"))
        self.label_433.setText(_translate("Form", "Artist"))
        self.label_435.setText(_translate("Form", "Title"))
        self.label_436.setText(_translate("Form", "Artist"))
        self.label_438.setText(_translate("Form", "Title"))
        self.label_439.setText(_translate("Form", "Artist"))
        self.label_441.setText(_translate("Form", "Title"))
        self.label_442.setText(_translate("Form", "Artist"))
        self.label_444.setText(_translate("Form", "Title"))
        self.label_445.setText(_translate("Form", "Artist"))
        self.label_36.setText(_translate("Form", "Based on your recent listening"))
        self.label_372.setText(_translate("Form", "Title"))
        self.label_373.setText(_translate("Form", "Artist"))
        self.label_375.setText(_translate("Form", "Title"))
        self.label_376.setText(_translate("Form", "Artist"))
        self.label_378.setText(_translate("Form", "Title"))
        self.label_379.setText(_translate("Form", "Artist"))
        self.label_381.setText(_translate("Form", "Title"))
        self.label_382.setText(_translate("Form", "Artist"))
        self.label_384.setText(_translate("Form", "Title"))
        self.label_385.setText(_translate("Form", "Artist"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Form", "Tab 1"))
        self.label.setText(_translate("Form", "Top Result"))
        self.label_2.setText(_translate("Form", "Title"))
        self.label_3.setText(_translate("Form", "Artist"))
        self.label_6.setText(_translate("Form", "Songs"))
        self.label_24.setText(_translate("Form", "Title"))
        self.label_28.setText(_translate("Form", "Artist"))
        self.label_33.setText(_translate("Form", "0:00"))
        self.label_20.setText(_translate("Form", "Title"))
        self.label_21.setText(_translate("Form", "Artist"))
        self.label_23.setText(_translate("Form", "0:00"))
        self.label_17.setText(_translate("Form", "Title"))
        self.label_18.setText(_translate("Form", "Artist"))
        self.label_19.setText(_translate("Form", "0:00"))
        self.label_11.setText(_translate("Form", "Title"))
        self.label_12.setText(_translate("Form", "Artist"))
        self.label_13.setText(_translate("Form", "0:00"))
        self.label_44.setText(_translate("Form", "Songs that you might like"))
        self.label_492.setText(_translate("Form", "Title"))
        self.label_493.setText(_translate("Form", "Artist"))
        self.label_495.setText(_translate("Form", "Title"))
        self.label_496.setText(_translate("Form", "Artist"))
        self.label_498.setText(_translate("Form", "Title"))
        self.label_499.setText(_translate("Form", "Artist"))
        self.label_501.setText(_translate("Form", "Title"))
        self.label_502.setText(_translate("Form", "Artist"))
        self.label_504.setText(_translate("Form", "Title"))
        self.label_505.setText(_translate("Form", "Artist"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Form", "Tab 2"))
        self.label_8.setText(_translate("Form", "Songs"))
        self.label_81.setText(_translate("Form", "1"))
        self.label_22.setText(_translate("Form", "Title"))
        self.label_29.setText(_translate("Form", "Artist"))
        self.label_30.setText(_translate("Form", "0:00"))
        self.label_82.setText(_translate("Form", "2"))
        self.label_50.setText(_translate("Form", "Title"))
        self.label_51.setText(_translate("Form", "Artist"))
        self.label_68.setText(_translate("Form", "0:00"))
        self.label_83.setText(_translate("Form", "3"))
        self.label_47.setText(_translate("Form", "Title"))
        self.label_48.setText(_translate("Form", "Artist"))
        self.label_49.setText(_translate("Form", "0:00"))
        self.label_84.setText(_translate("Form", "4"))
        self.label_78.setText(_translate("Form", "Title"))
        self.label_79.setText(_translate("Form", "Artist"))
        self.label_80.setText(_translate("Form", "0:00"))
        self.label_85.setText(_translate("Form", "5"))
        self.label_75.setText(_translate("Form", "Title"))
        self.label_76.setText(_translate("Form", "Artist"))
        self.label_77.setText(_translate("Form", "0:00"))
        self.label_86.setText(_translate("Form", "6"))
        self.label_72.setText(_translate("Form", "Title"))
        self.label_73.setText(_translate("Form", "Artist"))
        self.label_74.setText(_translate("Form", "0:00"))
        self.label_87.setText(_translate("Form", "7"))
        self.label_69.setText(_translate("Form", "Title"))
        self.label_70.setText(_translate("Form", "Artist"))
        self.label_71.setText(_translate("Form", "0:00"))
        self.label_88.setText(_translate("Form", "8"))
        self.label_35.setText(_translate("Form", "Title"))
        self.label_45.setText(_translate("Form", "Artist"))
        self.label_46.setText(_translate("Form", "0:00"))
        self.label_89.setText(_translate("Form", "9"))
        self.label_31.setText(_translate("Form", "Title"))
        self.label_32.setText(_translate("Form", "Artist"))
        self.label_34.setText(_translate("Form", "0:00"))
        self.label_90.setText(_translate("Form", "10"))
        self.label_14.setText(_translate("Form", "Title"))
        self.label_15.setText(_translate("Form", "Artist"))
        self.label_16.setText(_translate("Form", "0:00"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("Form", "Tab 3"))
        self.label_7.setText(_translate("Form", "<html><head/><body><p align=\"center\">Search songs to play</p></body></html>"))
        self.pushButton_3.setText(_translate("Form", "Search"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_4), _translate("Form", "Tab 1"))
        self.label_53.setText(_translate("Form", "TITLE"))
        self.label_54.setText(_translate("Form", "ARTIST"))
        self.label_55.setText(_translate("Form", "Up next"))
        self.label_56.setText(_translate("Form", "Title"))
        self.label_57.setText(_translate("Form", "Artist"))
        self.label_58.setText(_translate("Form", "Title"))
        self.label_59.setText(_translate("Form", "Artist"))
        self.label_60.setText(_translate("Form", "Title"))
        self.label_62.setText(_translate("Form", "Artist"))
        self.label_63.setText(_translate("Form", "Title"))
        self.label_64.setText(_translate("Form", "Artist"))
        self.label_65.setText(_translate("Form", "Title"))
        self.label_67.setText(_translate("Form", "Artist"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_5), _translate("Form", "Tab 2"))
        self.label_4.setText(_translate("Form", "Music1"))
        self.label_5.setText(_translate("Form", "Artist"))
        self.label_66.setText(_translate("Form", "-:--"))
        self.maxduration.setText(_translate("Form", "-:--"))

class DashboardWindow(QtWidgets.QWidget):
    def __init__(self, user_id=None, cloud_services=None, dashboard=None, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # --------------------- User / Dashboard ---------------------
        self.user_id = user_id
        self.cloud_services = cloud_services
        self.dashboard = dashboard
        self._cover_widgets = {}
        self._queued_cover_ids = set()
        self._cover_thread_pool = QtCore.QThreadPool(self)
        self._cover_thread_pool.setMaxThreadCount(4)

        # --------------------- VLC Player ---------------------------
        instance = vlc.Instance('--no-plugins-cache', '--aout=directsound')
        self.player = instance.media_player_new()
        self.is_paused = True
        self.repeat_mode = False
        self.user_seeking = False

        # --------------------- Playlists ---------------------------
        self.playlist = []
        self.home_playlist = []
        self.recommended_playlist = []
        self.current_index = 0

        # --------------------- Timer -------------------------------
        self.timer = QtCore.QTimer(interval=300)
        self.timer.timeout.connect(self.update_progress)

        # --------------------- Volume ------------------------------
        self.ui.Volumeslider.setValue(50)
        self.player.audio_set_volume(50)
        self.ui.Volumeslider.valueChanged.connect(self.change_volume)

        # --------------------- Initial Load ------------------------
        self.load_playlist()
        self.master_playlist = self.playlist.copy()  # master copy for searching
        self.setup_home_playlist()
        self.setup_search_completer()
        self.setup_controls()
        self.setup_slider_events()
        self.setup_home_clickables()
        self.setup_hover_effects()
        self.load_home_display(self.home_playlist)

        if self.playlist:
            self.recommended_playlist = self.playlist.copy()
            self.display_song_metadata(self.playlist[self.current_index])
            self.update_up_next()
            QtCore.QTimer.singleShot(0, self.queue_visible_covers)


        # --------------------- Events -----------------------------
        self.ui.pushButton_10.clicked.connect(self.open_recognition)
        self.ui.pushButton_2.clicked.connect(self.play_search_song)
        self.player.event_manager().event_attach(
            vlc.EventType.MediaPlayerEndReached, self.on_song_end
        )

    # =====================================================================
    #                            INITIAL SETUP
    # =====================================================================

    def setup_controls(self):
        controls = {
            self.ui.pause_play: self.toggle_play_pause,
            self.ui.fastforward: self.next_song,
            self.ui.backward: self.previous_song,
            self.ui.random: self.shuffle_song,
            self.ui.repeat: self.repeat_song
        }
        for btn, func in controls.items():
            btn.mousePressEvent = lambda e, f=func: f() if e.button() == QtCore.Qt.LeftButton else None

    def setup_slider_events(self):
        slider = self.ui.Musicslider
        slider.sliderPressed.connect(self.slider_pressed)
        slider.sliderReleased.connect(self.slider_released)
        slider.valueChanged.connect(self.slider_moved)
        slider.mousePressEvent = self.slider_clicked

    def slider_clicked(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            slider = self.ui.Musicslider
            pos = event.position().x() if hasattr(event, "position") else event.x()
            value = round(slider.minimum() + (slider.maximum() - slider.minimum()) * pos / slider.width())
            slider.setValue(min(value, slider.maximum()))
            self.player.set_time(value)
        QtWidgets.QSlider.mousePressEvent(self.ui.Musicslider, event)

    def setup_home_playlist(self):
        import random
        self.home_playlist = self.playlist.copy()
        random.shuffle(self.home_playlist)

    def setup_hover_effects(self):
        self._hover_filter = HoverAccentFilter(self)
        interactive = list(self.findChildren(QtWidgets.QPushButton))
        interactive.extend(
            [
                self.ui.label_25,
                self.ui.label_26,
                self.ui.label_27,
                self.ui.pause_play,
                self.ui.fastforward,
                self.ui.backward,
                self.ui.random,
                self.ui.repeat,
                *self.home_images,
                *self.home_titles,
                *self.special_covers,
                *self.special_titles,
            ]
        )
        for widget in dict.fromkeys(interactive):
            widget.setCursor(QtCore.Qt.PointingHandCursor)
            widget.installEventFilter(self._hover_filter)

    # ------------------- Home Clickable Elements -------------------
    def setup_home_clickables(self):
        
        # ------------------- Remaining home songs -------------------
        self.home_images = [
            self.ui.label_431, self.ui.label_434, self.ui.label_437, self.ui.label_440, self.ui.label_443,
            self.ui.label_371, self.ui.label_374, self.ui.label_377, self.ui.label_380, self.ui.label_383,
            self.ui.label_446, self.ui.label_449, self.ui.label_452, self.ui.label_455, self.ui.label_458,
            self.ui.label_491, self.ui.label_494, self.ui.label_497, self.ui.label_500, self.ui.label_503
        ]
        self.home_titles = [
            self.ui.label_432, self.ui.label_435, self.ui.label_438, self.ui.label_441, self.ui.label_444,
            self.ui.label_372, self.ui.label_375, self.ui.label_378, self.ui.label_381, self.ui.label_384,
            self.ui.label_447, self.ui.label_450, self.ui.label_453, self.ui.label_456, self.ui.label_459,
            self.ui.label_492, self.ui.label_495, self.ui.label_498, self.ui.label_501, self.ui.label_504
        ]
        self.home_artists = [
            self.ui.label_433, self.ui.label_436, self.ui.label_439, self.ui.label_442, self.ui.label_445,
            self.ui.label_373, self.ui.label_376, self.ui.label_379, self.ui.label_382, self.ui.label_385,
            self.ui.label_448, self.ui.label_451, self.ui.label_454, self.ui.label_457, self.ui.label_460,
            self.ui.label_493, self.ui.label_496, self.ui.label_499, self.ui.label_502, self.ui.label_505
        ]
        # ------------------- Special first 4 home songs -------------------
        self.special_covers = [
            self.ui.pushButton_8, self.ui.pushButton_7, self.ui.pushButton_6, self.ui.pushButton_4,
            self.ui.pushButton_11, self.ui.pushButton_15, self.ui.pushButton_14, self.ui.pushButton_24,
            self.ui.pushButton_23, self.ui.pushButton_22, self.ui.pushButton_21, self.ui.pushButton_13,
            self.ui.pushButton_12, self.ui.pushButton_5
        ]
        self.special_titles = [
            self.ui.label_24, self.ui.label_20, self.ui.label_17, self.ui.label_11,
            self.ui.label_22, self.ui.label_50, self.ui.label_47, self.ui.label_78,
            self.ui.label_75, self.ui.label_72, self.ui.label_69, self.ui.label_35,
            self.ui.label_31, self.ui.label_14  
        ]
        self.special_artists = [
            self.ui.label_28, self.ui.label_21, self.ui.label_18, self.ui.label_12,
            self.ui.label_29, self.ui.label_51, self.ui.label_48, self.ui.label_79,
            self.ui.label_76, self.ui.label_73, self.ui.label_70, self.ui.label_45,
            self.ui.label_32, self.ui.label_15

        ]
        self.special_max_duration = [
            self.ui.label_33, self.ui.label_23, self.ui.label_19, self.ui.label_13,
            self.ui.label_30, self.ui.label_68, self.ui.label_49, self.ui.label_80,
            self.ui.label_77, self.ui.label_74, self.ui.label_71, self.ui.label_46,
            self.ui.label_34, self.ui.label_16
        ]


# ------------------- Load special first songs with proper scaling -------------------
        for idx, (title_label, cover_label) in enumerate(zip(self.home_titles, self.home_images)):
            # Bind the current index as default arg to avoid closure issues
            title_label.mousePressEvent = lambda e, i=idx: self.play_home_song(i) if e.button() == QtCore.Qt.LeftButton else None
            cover_label.mousePressEvent = lambda e, i=idx: self.play_home_song(i) if e.button() == QtCore.Qt.LeftButton else None

        # ------------------- Load special covers like before -------------------
        placeholder = os.path.join(self.ui.media_path, "default_cover.png")
        for i in range(min(len(self.special_covers), len(self.home_playlist))):
            song = self.home_playlist[i]
            self.register_cover_widget(song, self.special_covers[i])
            cover_path = self.cover_path_for(song, placeholder)
            self.render_cover_widget(self.special_covers[i], cover_path)


            # ------------------- Title & Artist -------------------
            self.special_titles[i].setText(song.title or "Unknown Title")
            self.special_artists[i].setText(song.artist or "Unknown Artist")

            # ------------------- Max Duration -------------------
            duration = getattr(song, "duration", None)
            self.special_max_duration[i].setText(
                self.format_time(int(duration)) if duration else "-:--"
            )

            # ------------------- Click Event -------------------
            func = lambda e, idx=i: self.play_home_song(idx) if e.button() == QtCore.Qt.LeftButton else None
            self.special_titles[i].mousePressEvent = func
            self.special_covers[i].mousePressEvent = func
        # ------------------- Load remaining home songs -------------------
        self.load_home_display(self.home_playlist[4:])

    def load_home_display(self, songs):
        placeholder = os.path.join(self.ui.media_path, "default_cover.png")

        for i, widget in enumerate(self.home_images):
            if i >= len(songs):
                self.home_titles[i].clear()
                self.home_artists[i].clear()
                if i < len(self.home_max_duration):
                    self.home_max_duration[i].setText("-:--")
                if isinstance(widget, QtWidgets.QLabel):
                    widget.setPixmap(QtGui.QPixmap())
                continue

            song = songs[i]

            # Cover
            cover_path = self.cover_path_for(song, placeholder)
            pixmap = QtGui.QPixmap(cover_path)
            pixmap = pixmap.scaled(widget.width(), widget.height(),
                                QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
            if isinstance(widget, QtWidgets.QLabel):
                widget.setPixmap(pixmap)
                widget.setScaledContents(True)

            # Title & Artist
            self.home_titles[i].setText(getattr(song, 'title', 'Unknown Title'))
            self.home_artists[i].setText(getattr(song, 'artist', 'Unknown Artist'))

            # Max duration
            if i < len(self.home_max_duration):
                duration = getattr(song, "duration", None)
                self.home_max_duration[i].setText(
                    self.format_time(int(duration)) if duration else "-:--"
                )


    # ------------------- Cloud catalog -------------------
    def load_playlist(self):
        if not self.cloud_services:
            self.playlist = []
            return
        self.playlist = list(self.cloud_services.load_catalog())

    def cover_path_for(self, song, fallback):
        cover_path = getattr(song, "cover_path", None)
        if cover_path and os.path.exists(cover_path):
            return str(cover_path)
        return str(fallback)

    @staticmethod
    def cover_id(song):
        return str(
            getattr(song, "id", "")
            or getattr(song, "cover_object_key", "")
            or id(song)
        )

    def register_cover_widget(self, song, widget):
        widgets = self._cover_widgets.setdefault(DashboardWindow.cover_id(song), [])
        if widget not in widgets:
            widgets.append(widget)

    def render_cover_widget(self, widget, cover_path):
        pixmap = QtGui.QPixmap(str(cover_path))
        if pixmap.isNull():
            return
        scaled = pixmap.scaled(
            widget.size(),
            QtCore.Qt.KeepAspectRatioByExpanding,
            QtCore.Qt.SmoothTransformation,
        )
        crop_x = max(0, (scaled.width() - widget.width()) // 2)
        crop_y = max(0, (scaled.height() - widget.height()) // 2)
        scaled = scaled.copy(crop_x, crop_y, widget.width(), widget.height())
        if isinstance(widget, QtWidgets.QPushButton):
            widget.setIcon(QtGui.QIcon(scaled))
            widget.setIconSize(widget.size())
            widget.setStyleSheet(
                "QPushButton { background-color: transparent; padding: 0px; "
                "border: none; border-radius: 5px; }"
            )
        else:
            widget.setPixmap(scaled)
            widget.setScaledContents(True)

    def queue_visible_covers(self):
        visible_songs = self.home_playlist[: len(self.special_covers) + len(self.home_images)]
        for song in visible_songs:
            self.queue_cover_download(song)

    def queue_cover_download(self, song):
        cover_path = getattr(song, "cover_path", "")
        cover_key = getattr(song, "cover_object_key", "")
        checksum = getattr(song, "cover_checksum_sha256", "")
        cover_id = DashboardWindow.cover_id(song)
        placeholder = os.path.normcase(
            os.path.abspath(os.path.join(self.ui.media_path, "default_cover.png"))
        )
        local_cover_ready = bool(
            cover_path
            and os.path.exists(cover_path)
            and os.path.normcase(os.path.abspath(str(cover_path))) != placeholder
        )
        if (
            not self.cloud_services
            or local_cover_ready
            or not cover_key
            or not checksum
            or cover_id in self._queued_cover_ids
        ):
            return

        self._queued_cover_ids.add(cover_id)
        task = CoverDownloadTask(self.cloud_services, song)
        task.signals.downloaded.connect(self.cover_downloaded)
        task.signals.failed.connect(self.cover_download_failed)
        self._cover_thread_pool.start(task)

    def cover_downloaded(self, song, cover_path):
        cover_id = DashboardWindow.cover_id(song)
        self._queued_cover_ids.discard(cover_id)
        song.cover_path = str(cover_path)
        for widget in self._cover_widgets.get(cover_id, []):
            self.render_cover_widget(widget, song.cover_path)

    def cover_download_failed(self, song, error):
        self._queued_cover_ids.discard(DashboardWindow.cover_id(song))
        print(f"Could not prepare cover for {getattr(song, 'title', 'song')}: {error}")

    def prepare_song_for_playback(self, song):
        file_path = getattr(song, "file_path", "")
        if (
            self.cloud_services
            and getattr(song, "track_object_key", None)
            and not (file_path and os.path.exists(file_path))
        ):
            song.file_path = str(self.cloud_services.prepare_track(song))
        return song

    # ------------------- Display -------------------
    def load_home_display(self, songs):
        placeholder = os.path.join(self.ui.media_path, "default_cover.png")
        for i, widget in enumerate(self.home_images):
            if i >= len(songs):
                self.home_titles[i].clear()
                self.home_artists[i].clear()
                if isinstance(widget, QtWidgets.QPushButton):
                    widget.setIcon(QtGui.QIcon())
                else:
                    widget.setPixmap(QtGui.QPixmap())
                continue

            song = songs[i]
            self.home_titles[i].setText(song.title or "Unknown Title")
            self.home_artists[i].setText(song.artist or "Unknown Artist")

            self.register_cover_widget(song, widget)
            cover_path = self.cover_path_for(song, placeholder)
            self.render_cover_widget(widget, cover_path)

    # =====================================================================
    #                           PLAYER
    # =====================================================================
    def display_song_metadata(self, song):
        placeholder = os.path.join(self.ui.media_path, "default_cover.png")
        self.register_cover_widget(song, self.ui.label_52)
        self.render_cover_widget(self.ui.label_52, self.cover_path_for(song, placeholder))
        self.queue_cover_download(song)
        self.ui.label_4.setText(song.title or "Unknown Title")
        self.ui.label_5.setText(song.artist or "Unknown Artist")
        self.ui.label_54.setText(song.artist or "Unknown Artist")
        self.ui.label_53.setText(
            getattr(song, "recommendation_reason", "") or song.title or "Unknown Title"
        )
        duration = getattr(song, "duration", None)
        self.ui.maxduration.setText(
            self.format_time(int(duration)) if duration else "-:--"
        )
        self.ui.tabWidget_2.setCurrentWidget(self.ui.tab_5)

    def load_song(self, song, play_after_load=False):
        """Loads a song into the player and updates UI labels."""
        try:
            song = self.prepare_song_for_playback(song)
        except Exception as exc:
            QtWidgets.QMessageBox.warning(
                self,
                "Playback Unavailable",
                f"MyRhythm could not prepare {getattr(song, 'title', 'this track')}.\n\n"
                f"Details: {exc}",
            )
            return False
        self.player.set_media(vlc.Media(song.file_path))

        placeholder = os.path.join(self.ui.media_path, "default_cover.png")
        cover_path = self.cover_path_for(song, placeholder)
        self.register_cover_widget(song, self.ui.label_52)
        self.render_cover_widget(self.ui.label_52, cover_path)

        # Mini player button
        if hasattr(self.ui, 'pushButton'):
            self.register_cover_widget(song, self.ui.pushButton)
            self.render_cover_widget(self.ui.pushButton, cover_path)
        self.queue_cover_download(song)

        # Update main labels
        self.ui.label_4.setText(song.title or "Unknown Title")
        self.ui.label_5.setText(song.artist or "Unknown Artist")

        # Update "Up Next" current song labels
        self.ui.label_54.setText(song.artist or "Unknown Artist")
        reason = getattr(song, "recommendation_reason", "")
        if reason:
            self.ui.label_53.setText(reason)
        else:
            self.ui.label_53.setText(song.title or "Unknown Title")

        # Reset slider
        self.ui.Musicslider.blockSignals(True)
        self.ui.Musicslider.setValue(0)
        self.ui.Musicslider.blockSignals(False)
        self.ui.label_66.setText("0:00")
        self.ui.maxduration.setText("-:--")

        # Play if required
        self.is_paused = not play_after_load
        icon = "pause_button.png" if play_after_load else "play_button.png"
        self.ui.pause_play.setPixmap(QtGui.QPixmap(os.path.join(self.ui.media_path, icon)))
        if play_after_load:
            self.player.play()
            self.timer.start()

        # Update Up Next section
        self.update_up_next()

        # Update max duration
        def set_max_duration(attempt=0):
            length = self.player.get_length()
            if length > 0:
                self.ui.Musicslider.setMaximum(length)
                self.ui.maxduration.setText(self.format_time(length // 1000))
            elif attempt < 20:
                QtCore.QTimer.singleShot(
                    100,
                    lambda: set_max_duration(attempt + 1),
                )
        set_max_duration()
        self.ui.tabWidget_2.setCurrentWidget(self.ui.tab_5)

    def play_current_song(self):
        self.load_song(self.playlist[self.current_index], play_after_load=True)

    def toggle_play_pause(self):
        if self.player.get_media() is None:
            if self.playlist:
                self.play_current_song()
            return
        if self.is_paused:
            self.player.play()
            self.is_paused = False
            self.timer.start()
            icon = "pause_button.png"
        else:
            self.player.pause()
            self.is_paused = True
            self.timer.stop()
            icon = "play_button.png"
        self.ui.pause_play.setPixmap(QtGui.QPixmap(os.path.join(self.ui.media_path, icon)))

    def next_song(self):
        if not self.playlist:
            return
        self.current_index = (self.current_index + 1) % len(self.playlist)
        self.play_current_song()  # This will call update_up_next automatically


    def previous_song(self):
        if not self.playlist:
            return
        self.current_index = (self.current_index - 1) % len(self.playlist)
        self.play_current_song()  # This will call update_up_next automatically


    def shuffle_song(self):
        if not self.playlist:
            return
        import random
        upcoming = self.playlist[self.current_index + 1:]
        random.shuffle(upcoming)
        self.playlist = self.playlist[:self.current_index + 1] + upcoming
        self.update_up_next()

    def repeat_song(self):
        self.repeat_mode = not self.repeat_mode

    # =====================================================================
    #                           SLIDER
    # =====================================================================
    def slider_pressed(self):
        self.user_seeking = True
        self.player.pause()
        self.timer.stop()

    def slider_released(self):
        value = self.ui.Musicslider.value()
        self.player.set_time(value)
        self.user_seeking = False
        self.is_paused = False
        self.player.play()
        self.timer.start()
        self.ui.pause_play.setPixmap(QtGui.QPixmap(os.path.join(self.ui.media_path, "pause_button.png")))

    def slider_moved(self, value):
        self.ui.label_66.setText(self.format_time(value // 1000))
        if self.user_seeking:
            self.player.set_time(value)

    # =====================================================================
    #                           PROGRESS / SONG END
    # =====================================================================
    def update_progress(self):
        if self.user_seeking:
            return
        current_time = self.player.get_time()
        if current_time >= 0:
            self.ui.Musicslider.blockSignals(True)
            self.ui.Musicslider.setValue(current_time)
            self.ui.Musicslider.blockSignals(False)
            self.ui.label_66.setText(self.format_time(current_time // 1000))

    def on_song_end(self, event):
        QtCore.QTimer.singleShot(0, self.handle_song_end)

    def handle_song_end(self):
        if self.user_seeking:
            return
        if self.repeat_mode:
            self.play_current_song()
        else:
            self.next_song()

    # =====================================================================
    #                           UP NEXT
    # =====================================================================

    def update_up_next(self):
        """
        Updates the Up Next sidebar labels and buttons.
        Shows up to five next songs and collapses unused rows.
        """
        up_next_titles = [self.ui.label_56, self.ui.label_58, self.ui.label_60,
                        self.ui.label_63, self.ui.label_65]
        up_next_artists = [self.ui.label_57, self.ui.label_59, self.ui.label_62,
                        self.ui.label_64, self.ui.label_67]
        up_next_buttons = [self.ui.pushButton_16, self.ui.pushButton_17, self.ui.pushButton_18,
                        self.ui.pushButton_19, self.ui.pushButton_20]
        up_next_layouts = [self.ui.horizontalLayout_21, self.ui.horizontalLayout_22,
                        self.ui.horizontalLayout_23, self.ui.horizontalLayout_24,
                        self.ui.horizontalLayout_25]

        placeholder = os.path.join(self.ui.media_path, "default_cover.png")
        idx = getattr(self, "current_index", 0)

        # Use current playlist as the source
        next_songs = self.playlist[idx + 1: idx + 6]
        self.ui.widget_9.setVisible(bool(next_songs))
        if next_songs:
            card_height = 75 + (len(next_songs) * 80)
            self.ui.widget_9.setFixedHeight(card_height)

        for i in range(5):
            if i >= len(next_songs):
                up_next_titles[i].setText("")
                up_next_artists[i].setText("")
                up_next_buttons[i].setIcon(QtGui.QIcon())
                for widget in (up_next_buttons[i], up_next_titles[i], up_next_artists[i]):
                    widget.setVisible(False)
                spacer = up_next_layouts[i].itemAt(2).spacerItem()
                if spacer:
                    spacer.changeSize(0, 0, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
                continue

            song = next_songs[i]
            title = getattr(song, "title", "Unknown Title")
            artist = getattr(song, "artist", "Unknown Artist")
            cover_path = self.cover_path_for(song, placeholder)

            up_next_titles[i].setText(title)
            up_next_artists[i].setText(artist)
            for widget in (up_next_buttons[i], up_next_titles[i], up_next_artists[i]):
                widget.setVisible(True)
            spacer = up_next_layouts[i].itemAt(2).spacerItem()
            if spacer:
                spacer.changeSize(
                    40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
                )
            self.register_cover_widget(song, up_next_buttons[i])
            self.render_cover_widget(up_next_buttons[i], cover_path)
            self.queue_cover_download(song)

            # Bind click to play the correct song in playlist
            def make_handler(index):
                return lambda e, idx=index: self._play_up_next_at(idx) if e.button() == QtCore.Qt.LeftButton else None

            up_next_buttons[i].mousePressEvent = make_handler(i)
            up_next_titles[i].mousePressEvent = make_handler(i)
            up_next_artists[i].mousePressEvent = make_handler(i)

    # Helper used by click handlers in update_up_next
    def _play_up_next_at(self, up_next_index):
        """
        Play the nth song in the Next list (0 = the first "next" song).
        This maps the up_next_index to the playlist index and plays it.
        """
        playlist_idx = self.current_index + 1 + up_next_index
        if playlist_idx < 0 or playlist_idx >= len(self.playlist):
            return
        self.current_index = playlist_idx
        self.play_current_song()


    # =====================================================================
    #                           HELPERS
    # =====================================================================
    def change_volume(self, value):
        self.player.audio_set_volume(value)

    def format_time(self, seconds):
        m, s = divmod(seconds, 60)
        return f"{m}:{s:02d}"

    def play_home_song(self, index):
        """Play a song from the Home playlist independently of recommendations."""
        if index >= len(self.home_playlist):
            return

        home_song = self.home_playlist[index]

        # Override the current playlist to become the home playlist
        self.playlist = self.home_playlist
        self.current_index = index

        print(f"[HOME] Playing: {home_song.title} by {home_song.artist}")

        # Update recommended_playlist to match current playlist
        self.recommended_playlist = self.playlist.copy()

        self.play_current_song()

    # ------------------- PLAY RECOMMENDED SONG -------------------
    def load_recommended_songs(self, songs):
        """
        Receives a list of recommended songs (dicts) from Recognition.py
        Converts them to song objects, replaces the playlist, plays the first song,
        and updates Up Next properly.
        """
        if not songs:
            print("[load_recommended_songs] No recommendations received.")
            return

        from types import SimpleNamespace
        converted = []
        for s in songs:
            temp_song = SimpleNamespace(
                id=s.get("song_id"),
                title=s.get("title") or "Unknown Title",
                artist=s.get("artist") or "Unknown Artist",
                genre=s.get("genre") or "Unknown Genre",
                file_path=s.get("file_path") or "",
                cover_path=(
                    ""
                    if s.get("cover_object_key")
                    and os.path.basename(str(s.get("cover_path") or "")) == "default_cover.png"
                    else s.get("cover_path") or ""
                ),
                track_object_key=s.get("track_object_key"),
                track_checksum_sha256=s.get("track_checksum_sha256"),
                track_content_type=s.get("track_content_type"),
                track_byte_size=s.get("track_byte_size"),
                cover_object_key=s.get("cover_object_key"),
                cover_checksum_sha256=s.get("cover_checksum_sha256"),
                cover_content_type=s.get("cover_content_type"),
                cover_byte_size=s.get("cover_byte_size"),
                recommendation_reason=s.get("recommendation_reason", ""),
            )
            converted.append(temp_song)

        # Set recommended_playlist and playlist
        self.recommended_playlist = converted.copy()
        self.playlist = converted.copy()

        # Start playback at first recommended song
        self.current_index = 0
        self.play_current_song()

    def play_recommended_song(self, song_dict):
        """
        Converts a recommended song dict into a song object and plays it.
        This supports clicking an Up Next item (or external calls).
        """
        from types import SimpleNamespace
        import os

        if not song_dict:
            return

        # Accept both dict and already-converted objects
        if isinstance(song_dict, dict):
            file_path = song_dict.get("file_path") or ""
            cover_path = song_dict.get("cover_path") or song_dict.get("cover") or ""
            if (
                song_dict.get("cover_object_key")
                and os.path.basename(str(cover_path)) == "default_cover.png"
            ):
                cover_path = ""
            temp_song = SimpleNamespace(
                id=song_dict.get("song_id") or song_dict.get("id"),
                title=song_dict.get("title", "Unknown Title"),
                artist=song_dict.get("artist", "Unknown Artist"),
                genre=song_dict.get("genre", "Unknown Genre"),
                file_path=file_path,
                cover_path=cover_path,
                track_object_key=song_dict.get("track_object_key"),
                track_checksum_sha256=song_dict.get("track_checksum_sha256"),
                track_content_type=song_dict.get("track_content_type"),
                track_byte_size=song_dict.get("track_byte_size"),
                cover_object_key=song_dict.get("cover_object_key"),
                cover_checksum_sha256=song_dict.get("cover_checksum_sha256"),
                cover_content_type=song_dict.get("cover_content_type"),
                cover_byte_size=song_dict.get("cover_byte_size"),
                recommendation_reason=song_dict.get("recommendation_reason", ""),
            )
        else:
            # assume object with appropriate attributes
            temp_song = song_dict

        # Replace current song in playlist (or set playlist if empty)
        if not hasattr(self, "playlist") or not self.playlist:
            self.playlist = [temp_song]
            self.current_index = 0
        else:
            # replace the current index entry so play_current_song() uses this item
            self.playlist[self.current_index] = temp_song

        # Play it
        self.play_current_song()

    # =====================================================================
    #                           EXTRA WINDOWS
    # =====================================================================
    def open_recognition(self):
        if self.cloud_services:
            try:
                result = self.cloud_services.provision_models()
                if result.failures:
                    QtWidgets.QMessageBox.warning(
                        self,
                        "Recognition Models Limited",
                        "Some recognition models could not be prepared. "
                        "Available modes can still be used.\n\n"
                        + "\n".join(
                            f"{name}: {message}"
                            for name, message in result.failures.items()
                        ),
                    )
            except Exception as exc:
                QtWidgets.QMessageBox.warning(
                    self,
                    "Recognition Models Unavailable",
                    f"Recognition models could not be prepared.\n\nDetails: {exc}",
                )
        engine_factory = (
            self.cloud_services.recommendation_engine
            if self.cloud_services
            else None
        )
        self.recognition_window = Ui_Recognition(
            user_id=self.user_id,
            dashboard=self,
            recommendation_engine_factory=engine_factory,
        )
        self.recognition_window.show()

    # =====================================================================
    #                           SEARCH
    # =====================================================================
    def setup_search_completer(self):
        song_titles = [song.title for song in self.master_playlist]  # <-- changed
        self.completer = QCompleter(song_titles)
        self.completer.setCaseSensitivity(False)
        self.ui.lineEdit_2.setCompleter(self.completer)

        popup = self.completer.popup()
        popup.setStyleSheet(self._get_completer_style())

        self.ui.lineEdit_2.returnPressed.connect(self.handle_search_enter)
        self.ui.pushButton_2.clicked.connect(self.play_search_song)
        self.ui.label_2.mousePressEvent = lambda e: self.play_search_song() if e.button() == QtCore.Qt.LeftButton else None
        self.ui.label_10.mousePressEvent = self.handle_label10_click

    def _get_completer_style(self):
        return """
QAbstractItemView {
    background-color: rgba(18, 18, 18, 200);
    color: #FFFFFF;
    border: 1px solid #333333;
    border-radius: 15px;
    font-family: "Plus Jakarta Sans SemiBold";
    font-size: 20px;
    padding: 5px;
    spacing: 30px;
}
QScrollBar:vertical {
    border: none; background: transparent; width: 8px; margin: 0;
}
QScrollBar::handle:vertical { background: #555555; min-height: 20px; border-radius: 4px; }
QScrollBar::handle:vertical:hover { background: #888888; }
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: none; }
QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical { border: none; width: 0; height: 0; background: none; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { border: none; background: none; }
"""

    def handle_search_enter(self):
        self.update_tab2_search()

    def handle_label10_click(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.update_tab2_search()

    def update_tab2_search(self):
        text = self.ui.lineEdit_2.text().strip()
        if not text:
            return

        norm_text = normalize_text(text)

        # Partial match search in home playlist
        song = next(
            (s for s in self.home_playlist if norm_text in normalize_text(s.title)),
            None
        )

        if song:
            self.ui.tabWidget.setCurrentWidget(self.ui.tab_2)
            self.ui.label_2.setText(song.title)
            self.ui.label_3.setText(song.artist)

            placeholder = os.path.join(self.ui.media_path, "default_cover.png")
            cover_path = self.cover_path_for(song, placeholder)
            pixmap = QtGui.QPixmap(cover_path).scaled(
                self.ui.pushButton_2.width(),
                self.ui.pushButton_2.height(),
                QtCore.Qt.KeepAspectRatio,
                QtCore.Qt.SmoothTransformation
            )
            self.ui.pushButton_2.setIcon(QtGui.QIcon(pixmap))
            self.ui.pushButton_2.setIconSize(QtCore.QSize(self.ui.pushButton_2.width(), self.ui.pushButton_2.height()))

            # Store current search song
            self.current_search_song = song

    # Play happens only when user clicks pushButton_2
    def play_search_song(self):
        if hasattr(self, 'current_search_song') and self.current_search_song:
            # Reset playlist to the main DB playlist before playing search
            self.playlist = self.home_playlist if hasattr(self, "home_playlist") else self.playlist
            try:
                self.current_index = self.playlist.index(self.current_search_song)
            except ValueError:
                self.current_index = 0
            self.play_current_song()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = DashboardWindow()
    window.show()
    sys.exit(app.exec_())

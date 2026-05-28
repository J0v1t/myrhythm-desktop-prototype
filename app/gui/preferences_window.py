import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from PyQt5 import QtWidgets, QtCore, QtGui
from app.gui.preferences1 import Ui_Form as Ui_Form1
from app.gui.preferences2 import Ui_Form as Ui_Form2
from app.gui.preferences3 import Ui_Form as Ui_Form3
from app.gui.dashboard2 import DashboardWindow
from app.database.models.preference import UserPreferences
from app.database.schema import db

class PreferencesWindow(QtWidgets.QMainWindow):
    def __init__(self, user, parent=None):
        super().__init__(parent)
        self.user = user
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.resize(1100, 928)

        # Center window
        screen = QtWidgets.QApplication.desktop().screenGeometry()
        self.move((screen.width() - 1100) // 2, (screen.height() - 928) // 2)

        self.current_step = 1
        self.selected_genres = []
        self.selected_artists = []
        self.dragging = False
        self.drag_start_position = None

        # Genres and Artists
        self.genres = ["HIP-HOP", "ELECTRONIC", "FOLK", "ROCK", "INSTRUMENTAL",
                       "INTERNATIONAL", "ACOUSTIC", "EXPERIMENTAL", "POP"]
        self.artists = ["ARTIST A", "ARTIST B", "ARTIST C", "ARTIST D",
                        "ARTIST E", "ARTIST F", "ARTIST G", "ARTIST H", "ARTIST I"]

        # Setup widgets
        self.widget1 = QtWidgets.QWidget(self)
        self.ui1 = Ui_Form1()
        self.ui1.setupUi(self.widget1)
        self.widget1.show()

        self.widget2 = QtWidgets.QWidget(self)
        self.ui2 = Ui_Form2()
        self.ui2.setupUi(self.widget2)
        self.widget2.hide()

        self.widget3 = QtWidgets.QWidget(self)
        self.ui3 = Ui_Form3()
        self.ui3.setupUi(self.widget3)
        self.widget3.hide()

        # --- Genre labels ---
        self.genre_labels = [
            self.ui1.hiphop, self.ui1.electronic, self.ui1.folk,
            self.ui1.rock, self.ui1.instrumental, self.ui1.international,
            self.ui1.label_10, self.ui1.experimental, self.ui1.pop
        ]
        self.genre_labels = [lbl for lbl in self.genre_labels if lbl is not None]

        # --- Artist labels ---
        self.artist_labels = [
            self.ui2.angry1, self.ui2.angry2, self.ui2.happy1,
            self.ui2.happy2, self.ui2.neutral1, self.ui2.neutral2,
            self.ui2.sad1, self.ui2.sad2, self.ui2.sad3
        ]

        # Store original styles
        for label in self.genre_labels + self.artist_labels:
            label.setProperty("original_style", label.styleSheet())
            label.setCursor(QtCore.Qt.PointingHandCursor)
            label.installEventFilter(self)

        # --- Connect navigation buttons ---
        self.ui1.pushButton.clicked.connect(self.next_step)
        self.ui2.pushButton.clicked.connect(self.next_step)
        self.ui2.label_13.installEventFilter(self)  # Back arrow
        self.ui3.pushButton.clicked.connect(self.go_to_dashboard2)

    # --- Event filter ---
    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.MouseButtonPress:
            if obj in self.genre_labels:
                index = self.genre_labels.index(obj)
                self.toggle_genre(obj, self.genres[index])
                return True
            elif obj in self.artist_labels:
                index = self.artist_labels.index(obj)
                self.toggle_artist(obj, self.artists[index])
                return True
            elif obj == self.ui2.label_13:
                self.go_back_to_preferences1()
                return True
        return super().eventFilter(obj, event)

    # --- Toggle genre selection with white border + glow ---
    def toggle_genre(self, label, genre):
        if genre in self.selected_genres:
            self.selected_genres.remove(genre)
            label.setGraphicsEffect(None)
            label.setStyleSheet(label.property("original_style"))  # restore original
        else:
            self.selected_genres.append(genre)
            glow = QtWidgets.QGraphicsDropShadowEffect()
            glow.setColor(QtCore.Qt.white)
            glow.setBlurRadius(20)
            glow.setOffset(0, 0)
            label.setGraphicsEffect(glow)
            label.setStyleSheet(label.property("original_style") + "; border: 3px solid white; border-radius: 15px;")

    # --- Toggle artist selection with glow only, no border radius change ---
    def toggle_artist(self, label, artist):
        if artist in self.selected_artists:
            self.selected_artists.remove(artist)
            label.setGraphicsEffect(None)
            label.setStyleSheet(label.property("original_style"))
        else:
            self.selected_artists.append(artist)
            glow = QtWidgets.QGraphicsDropShadowEffect()
            glow.setColor(QtCore.Qt.white)
            glow.setBlurRadius(15)  # smaller blur to reduce rounded look
            glow.setOffset(0, 0)
            label.setGraphicsEffect(glow)
        # Force rectangular appearance
            label.setStyleSheet(label.property("original_style") + "; border-radius: 0;")

    # --- Navigation ---
    def next_step(self):
        if self.current_step == 1:
            if not self.selected_genres:
                QtWidgets.QMessageBox.warning(self, "Selection Required", "Please select at least 1 genre.")
                return
            self.widget1.hide()
            self.widget2.show()
            self.current_step = 2
        elif self.current_step == 2:
            if not self.selected_artists:
                QtWidgets.QMessageBox.warning(self, "Selection Required", "Please select at least 1 artist.")
                return
            self.save_preferences()
            self.widget2.hide()
            self.widget3.show()
            self.current_step = 3

    def go_back_to_preferences1(self):
        self.widget2.hide()
        self.widget1.show()
        self.current_step = 1

    # --- Save preferences ---
    def save_preferences(self):
        if self.user:
            preferences = UserPreferences(
                user_id=self.user.id,
                favorite_genres=','.join(self.selected_genres),
                favorite_artists=','.join(self.selected_artists)
            )
            db.add(preferences)
            db.commit()

    # --- Drag ---
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.dragging = True
            self.drag_start_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self.dragging and event.buttons() == QtCore.Qt.LeftButton:
            self.move(event.globalPos() - self.drag_start_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.dragging = False
            event.accept()

    # --- Dashboard ---
    def go_to_dashboard2(self):
        self.dashboard_window = DashboardWindow(self.user.id if self.user else None)
        self.dashboard_window.show()
        self.close()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = PreferencesWindow(user=None)
    window.show()
    sys.exit(app.exec_())

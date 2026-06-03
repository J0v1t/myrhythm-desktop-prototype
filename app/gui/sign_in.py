from PyQt5 import QtCore, QtGui, QtWidgets
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import res

class Ui_Form(object):
    def __init__(self):
        self.current_color = [45, 45, 45]
        self.target_color = [45, 45, 45]
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_color)
        self.timer.setInterval(10)
        self.password_hidden = True

    def close_app(self):
        QtWidgets.QApplication.instance().quit()

    def update_color(self):
        for i in range(3):
            if self.current_color[i] < self.target_color[i]:
                self.current_color[i] += 1
            elif self.current_color[i] > self.target_color[i]:
                self.current_color[i] -= 1
        palette = self.pushButton_2.palette()
        palette.setColor(QtGui.QPalette.Button, QtGui.QColor(*self.current_color))
        self.pushButton_2.setPalette(palette)
        if self.current_color == self.target_color:
            self.timer.stop()

    def start_animation(self, target):
        self.target_color = target
        self.timer.start()

    def toggle_password_visibility(self):
        if self.password_hidden:
            self.lineEdit_8.setEchoMode(QtWidgets.QLineEdit.Normal)
            self.label_14.setIcon(QtGui.QIcon(os.path.join(self.media_path, "eye-closed.svg")))
            self.password_hidden = False
        else:
            self.lineEdit_8.setEchoMode(QtWidgets.QLineEdit.Password)
            self.label_14.setIcon(QtGui.QIcon(os.path.join(self.media_path, "eye.svg")))
            self.password_hidden = True

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1027, 731)
        Form.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        Form.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        base_path = os.path.dirname(__file__)  # app/ui/
        media_path = os.path.abspath(os.path.join(base_path, "..", "..", "media"))
        self.media_path = media_path

        self.widget_2 = QtWidgets.QWidget(Form)
        self.widget_2.setGeometry(QtCore.QRect(50, 60, 881, 581))
        font = QtGui.QFont()
        font.setFamily("Noto Sans JP DemiLight")
        font.setBold(False)
        font.setWeight(50)
        self.widget_2.setFont(font)
        self.widget_2.setObjectName("widget_2")

        # Existing labels and buttons
        self.label_11 = QtWidgets.QLabel(self.widget_2)
        self.label_11.setGeometry(QtCore.QRect(410, 40, 441, 521))
        font = QtGui.QFont()
        font.setFamily("Noto Sans JP DemiLight")
        font.setBold(False)
        font.setWeight(50)
        self.label_11.setFont(font)
        self.label_11.setStyleSheet("background-color:rgba(255,255,255,255);\n"
"\n"
"border-bottom-right-radius:40px;\n"
"border-top-right-radius:40px;")
        self.label_11.setText("")
        self.label_11.setObjectName("label_11")

        self.label_12 = QtWidgets.QLabel(self.widget_2)
        self.label_12.setGeometry(QtCore.QRect(80, 40, 331, 521))
        self.label_12.setStyleSheet("QWidget {\n"
"    border-top-left-radius: 40px;\n"
"    border-bottom-left-radius: 40px;\n"
"}\n"
"\n"
"\n"
"")
        self.label_12.setText("")
        self.label_12.setPixmap(QtGui.QPixmap(os.path.join(media_path, "auth_hero.png")))
        self.label_12.setScaledContents(True)
        self.label_12.setAlignment(QtCore.Qt.AlignCenter)
        self.label_12.setWordWrap(False)
        self.label_12.setObjectName("label_12")

        self.label_13 = QtWidgets.QLabel(self.widget_2)
        self.label_13.setGeometry(QtCore.QRect(450, 90, 131, 51))
        font = QtGui.QFont()
        font.setFamily("Noto Sans JP Medium")
        font.setPointSize(15)
        font.setBold(False)
        font.setWeight(50)
        self.label_13.setFont(font)
        self.label_13.setObjectName("label_13")

        self.pushButton_2 = QtWidgets.QPushButton(self.widget_2)
        self.pushButton_2.setGeometry(QtCore.QRect(450, 400, 351, 51))
        font = QtGui.QFont()
        font.setFamily("Noto Sans JP DemiLight")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setStyleSheet("QPushButton {\n"
"    background-color: rgb(45,45,45);\n"
"    color: white;\n"
"    border: none;\n"
"    border-radius: 5px;\n"
"    padding: 6px 12px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #1a1a1a; /* slightly darker black */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #333333; /* even darker when pressed */\n"
"}")
        self.pushButton_2.setObjectName("pushButton_2")

        self.label_16 = QtWidgets.QLabel(self.widget_2)
        self.label_16.setGeometry(QtCore.QRect(510, 470, 181, 31))
        font = QtGui.QFont()
        font.setFamily("Noto Sans JP DemiLight")
        font.setBold(False)
        font.setWeight(50)
        self.label_16.setFont(font)
        self.label_16.setObjectName("label_16")

        self.lineEdit_7 = QtWidgets.QLineEdit(self.widget_2)
        self.lineEdit_7.setGeometry(QtCore.QRect(450, 210, 351, 31))
        font = QtGui.QFont()
        font.setFamily("Noto Sans JP DemiLight")
        font.setBold(False)
        font.setWeight(50)
        self.lineEdit_7.setFont(font)
        self.lineEdit_7.setStyleSheet("QLineEdit {\n"
"    border:1px solid lightgray;\n"
"    border-radius:5px;\n"
"    padding:4px;\n"
"}\n"
"\n"
"QLineEdit:hover {\n"
"    border:1px solid gray;\n"
"}")
        self.lineEdit_7.setObjectName("lineEdit_7")

        self.label_17 = QtWidgets.QLabel(self.widget_2)
        self.label_17.setGeometry(QtCore.QRect(450, 170, 71, 31))
        font = QtGui.QFont()
        font.setFamily("Noto Sans JP DemiLight")
        font.setPointSize(8)
        font.setBold(False)
        font.setWeight(50)
        self.label_17.setFont(font)
        self.label_17.setObjectName("label_17")

        self.lineEdit_8 = QtWidgets.QLineEdit(self.widget_2)
        self.lineEdit_8.setGeometry(QtCore.QRect(450, 300, 351, 31))
        font = QtGui.QFont()
        font.setFamily("Noto Sans JP DemiLight")
        font.setBold(False)
        font.setWeight(50)
        self.lineEdit_8.setFont(font)
        self.lineEdit_8.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_8.setStyleSheet("QLineEdit {\n"
"    border:1px solid lightgray;\n"
"    border-radius:5px;\n"
"    padding:4px;\n"
"}\n"
"\n"
"QLineEdit:hover {\n"
"    border:1px solid gray;\n"
"}")
        self.lineEdit_8.setObjectName("lineEdit_8")

        self.label_18 = QtWidgets.QLabel(self.widget_2)
        self.label_18.setGeometry(QtCore.QRect(450, 270, 111, 31))
        font = QtGui.QFont()
        font.setFamily("Noto Sans JP DemiLight")
        font.setPointSize(8)
        font.setBold(False)
        font.setWeight(50)
        self.label_18.setFont(font)
        self.label_18.setObjectName("label_18")

        self.label_19 = QtWidgets.QLabel(self.widget_2)
        self.label_19.setGeometry(QtCore.QRect(90, 40, 311, 291))
        self.label_19.setText("")
        self.label_19.setPixmap(QtGui.QPixmap(os.path.join(media_path, "myrhythm_logo.svg")))
        self.label_19.setScaledContents(True)
        self.label_19.setVisible(False)
        self.label_19.setObjectName("label_19")

        self.pushButton = QtWidgets.QPushButton(self.widget_2)
        self.pushButton.setGeometry(QtCore.QRect(660, 470, 81, 32))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("QPushButton {\n"
"    background-color: transparent;\n"
"    border: none;\n"
"    color: rgb(45, 45, 45);\n"
"    font-weight: bold;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    color: rgb(20, 20, 20);\n"
"    text-decoration: underline;\n"
"}")
        self.pushButton.setObjectName("pushButton")

        self.error = QtWidgets.QLabel(self.widget_2)
        self.error.setGeometry(QtCore.QRect(450, 340, 231, 18))
        font = QtGui.QFont()
        font.setStrikeOut(False)
        self.error.setFont(font)
        self.error.setStyleSheet("color: rgb(210, 15, 77);")
        self.error.setObjectName("error")

        # --- NEW ICONS ---
        self.label_14 = QtWidgets.QPushButton(self.widget_2)
        self.label_14.setGeometry(QtCore.QRect(770, 306, 20, 20))
        self.label_14.setIcon(QtGui.QIcon(os.path.join(media_path, "eye.svg")))
        self.label_14.setIconSize(QtCore.QSize(20, 20))
        self.label_14.setFlat(True)
        self.label_14.setStyleSheet("QPushButton { background-color: transparent; border: none; }")
        self.label_14.clicked.connect(self.toggle_password_visibility)
        self.label_14.setObjectName("label_14")

        self.label_5 = QtWidgets.QPushButton(self.widget_2)
        self.label_5.setGeometry(QtCore.QRect(790, 60, 31, 31))
        self.label_5.setIcon(QtGui.QIcon(os.path.join(media_path, "x_black.svg")))
        self.label_5.setIconSize(QtCore.QSize(31, 31))
        self.label_5.setFlat(True)
        self.label_5.setStyleSheet("QPushButton { background-color: transparent; border: none; }")
        self.label_5.clicked.connect(self.close_app)
        self.label_5.setObjectName("label_5")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_13.setText(_translate("Form", "Sign In"))
        self.pushButton_2.setText(_translate("Form", "Sign In"))
        self.label_16.setText(_translate("Form", "Don't have an account?"))
        self.label_17.setText(_translate("Form", "Email"))
        self.label_18.setText(_translate("Form", "Password"))
        self.pushButton.setText(_translate("Form", "Sign Up"))
        self.error.setText(_translate("Form", "Invalid email and/or password"))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

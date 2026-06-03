from PyQt5 import QtCore, QtGui, QtWidgets
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import res  # your resource file

class Ui_Form(object):
    def __init__(self):
        self.password_hidden = True

    def close_app(self):
        QtWidgets.QApplication.instance().quit()

    def toggle_password_visibility(self):
        if self.password_hidden:
            self.lineEdit_4.setEchoMode(QtWidgets.QLineEdit.Normal)
            self.label_11.setIcon(QtGui.QIcon(os.path.join(self.media_path, "eye-closed.svg")))
            self.password_hidden = False
        else:
            self.lineEdit_4.setEchoMode(QtWidgets.QLineEdit.Password)
            self.label_11.setIcon(QtGui.QIcon(os.path.join(self.media_path, "eye.svg")))
            self.password_hidden = True

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1032, 731)
        Form.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        Form.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        base_path = os.path.dirname(__file__)
        media_path = os.path.abspath(os.path.join(base_path, "..", "..", "media"))
        self.media_path = media_path

        # Main widget
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setGeometry(QtCore.QRect(60, 60, 881, 581))
        font = QtGui.QFont()
        font.setFamily("Noto Sans JP DemiLight")
        font.setBold(False)
        font.setWeight(50)
        self.widget.setFont(font)
        self.widget.setObjectName("widget")

        # Right panel (white)
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setGeometry(QtCore.QRect(400, 40, 441, 521))
        font.setFamily("Noto Sans JP DemiLight")
        self.label.setFont(font)
        self.label.setStyleSheet(
            "background-color:rgba(255,255,255,255);\n"
            "border-bottom-right-radius:40px;\n"
            "border-top-right-radius:40px;"
        )
        self.label.setText("")
        self.label.setObjectName("label")

        # Left panel (background image)
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setGeometry(QtCore.QRect(70, 40, 331, 521))
        self.label_3.setStyleSheet(
            "background-color:rgb(45, 45, 45);\n"
            "border-top-left-radius:40px;\n"
            "border-bottom-left-radius:40px;"
        )
        self.label_3.setText("")
        self.label_3.setPixmap(QtGui.QPixmap(os.path.join(media_path, "auth_hero.png")))
        self.label_3.setScaledContents(True)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")

        # "Sign Up" title
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setGeometry(QtCore.QRect(440, 80, 131, 51))
        font = QtGui.QFont()
        font.setFamily("Noto Sans JP Medium")
        font.setPointSize(15)
        font.setBold(False)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")

        # Sign Up button
        self.pushButton = QtWidgets.QPushButton(self.widget)
        self.pushButton.setGeometry(QtCore.QRect(440, 440, 341, 51))
        font = QtGui.QFont()
        font.setFamily("Noto Sans JP DemiLight")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet(
            "QPushButton {\n"
            "    background-color: rgb(45,45,45);\n"
            "    color: white;\n"
            "    border: none;\n"
            "    border-radius: 5px;\n"
            "    padding: 6px 12px;\n"
            "}\n"
            "QPushButton:hover {\n"
            "    background-color: #1a1a1a;\n"
            "}\n"
            "QPushButton:pressed {\n"
            "    background-color: #333333;\n"
            "}"
        )
        self.pushButton.setObjectName("pushButton")

        # Labels and LineEdits
        def create_label(x, y, w, h, text, pointsize=8):
            label = QtWidgets.QLabel(self.widget)
            label.setGeometry(QtCore.QRect(x, y, w, h))
            font = QtGui.QFont()
            font.setFamily("Noto Sans JP DemiLight")
            font.setPointSize(pointsize)
            label.setFont(font)
            label.setText(text)
            return label

        def create_lineedit(x, y, w, h):
            line = QtWidgets.QLineEdit(self.widget)
            line.setGeometry(QtCore.QRect(x, y, w, h))
            font = QtGui.QFont()
            font.setFamily("Noto Sans JP DemiLight")
            line.setFont(font)
            line.setStyleSheet(
                "QLineEdit {\n"
                "    border:1px solid lightgray;\n"
                "    border-radius:5px;\n"
                "    padding:4px;\n"
                "}\n"
                "QLineEdit:hover {\n"
                "    border:1px solid gray;\n"
                "}"
            )
            return line

        self.label_4 = create_label(440, 150, 131, 31, "Username")
        self.lineEdit = create_lineedit(440, 180, 341, 31)

        self.label_7 = create_label(440, 230, 71, 31, "Email")
        self.lineEdit_3 = create_lineedit(440, 260, 341, 31)

        self.label_8 = create_label(440, 330, 111, 31, "Password")
        self.lineEdit_4 = create_lineedit(440, 360, 341, 31)
        self.lineEdit_4.setEchoMode(QtWidgets.QLineEdit.Password)

        # Logo
        self.label_9 = QtWidgets.QLabel(self.widget)
        self.label_9.setGeometry(QtCore.QRect(80, 40, 311, 291))
        self.label_9.setPixmap(QtGui.QPixmap(os.path.join(media_path, "myrhythm_logo.svg")))
        self.label_9.setScaledContents(True)
        self.label_9.setVisible(False)
        self.label_9.setObjectName("label_9")

        # Eye icon for password
        self.label_11 = QtWidgets.QPushButton(self.widget)
        self.label_11.setGeometry(QtCore.QRect(750, 366, 21, 20))
        self.label_11.setIcon(QtGui.QIcon(os.path.join(media_path, "eye.svg")))
        self.label_11.setIconSize(QtCore.QSize(21, 20))
        self.label_11.setFlat(True)
        self.label_11.setStyleSheet("QPushButton { background-color: transparent; border: none; }")
        self.label_11.clicked.connect(self.toggle_password_visibility)
        self.label_11.setObjectName("label_11")

        # Close button (X)
        self.label_5 = QtWidgets.QPushButton(self.widget)
        self.label_5.setGeometry(QtCore.QRect(780, 60, 31, 31))
        self.label_5.setIcon(QtGui.QIcon(os.path.join(media_path, "x_black.svg")))
        self.label_5.setIconSize(QtCore.QSize(31, 31))
        self.label_5.setFlat(True)
        self.label_5.setStyleSheet("QPushButton { background-color: transparent; border: none; }")
        self.label_5.clicked.connect(self.close_app)
        self.label_5.setObjectName("label_5")

        # "Already have an account?" and Sign In button
        self.label_6 = create_label(490, 500, 181, 31, "Already have an account?")
        self.pushButton_3 = QtWidgets.QPushButton(self.widget)
        self.pushButton_3.setGeometry(QtCore.QRect(650, 500, 81, 32))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setStyleSheet(
            "QPushButton {\n"
            "    background-color: transparent;\n"
            "    border: none;\n"
            "    color: rgb(45, 45, 45);\n"
            "    font-weight: bold;\n"
            "}\n"
            "QPushButton:hover {\n"
            "    color: rgb(20, 20, 20);\n"
            "    text-decoration: underline;\n"
            "}"
        )
        self.pushButton_3.setObjectName("pushButton_3")

        # Error labels
        self.error = QtWidgets.QLabel(self.widget)
        self.error.setGeometry(QtCore.QRect(440, 400, 251, 18))
        self.error.setFont(QtGui.QFont("Noto Sans JP DemiLight"))
        self.error.setStyleSheet("color: rgb(210, 15, 77);")
        self.error.setObjectName("error")

        self.error_2 = QtWidgets.QLabel(self.widget)
        self.error_2.setGeometry(QtCore.QRect(440, 300, 251, 18))
        self.error_2.setFont(QtGui.QFont("Noto Sans JP DemiLight"))
        self.error_2.setStyleSheet("color: rgb(210, 15, 77);")
        self.error_2.setObjectName("error_2")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_2.setText(_translate("Form", "Sign Up"))
        self.pushButton.setText(_translate("Form", "Sign Up"))
        self.pushButton_3.setText(_translate("Form", "Sign In"))
        self.error.setText(_translate("Form", "The password field is required"))
        self.error_2.setText(_translate("Form", "Enter a valid email address"))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

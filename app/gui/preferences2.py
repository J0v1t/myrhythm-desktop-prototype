from PyQt5 import QtCore, QtGui, QtWidgets
import sys, os

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(597, 801)
        Form.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        Form.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        base_path = os.path.dirname(__file__)  # app/gui/
        media_path = os.path.abspath(os.path.join(base_path, "..", "..", "media"))
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(Form)
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans ExtraBold")
        font.setPointSize(9)
        self.frame.setFont(font)
        self.frame.setStyleSheet("background-color: rgb(8, 8, 8);\n"
"border-radius:20px;\n"
"")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setGeometry(QtCore.QRect(30, 70, 426, 46))
        self.label_2.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans ExtraBold")
        font.setPointSize(15)
        font.setBold(False)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_2.setObjectName("label_2")
        self.pushButton = QtWidgets.QPushButton(self.frame)
        self.pushButton.setGeometry(QtCore.QRect(12, 690, 540, 70))
        self.pushButton.setMinimumSize(QtCore.QSize(0, 70))
        self.pushButton.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans SemiBold")
        font.setPointSize(12)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border-radius:30px;")
        self.pushButton.setObjectName("pushButton")
        self.label_15 = QtWidgets.QLabel(self.frame)
        self.label_15.setGeometry(QtCore.QRect(40, 250, 111, 31))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans ExtraBold")
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.label_15.setFont(font)
        self.label_15.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: transparent;")
        self.label_15.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_15.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
        self.label_15.setObjectName("label_15")
        self.label_16 = QtWidgets.QLabel(self.frame)
        self.label_16.setGeometry(QtCore.QRect(220, 250, 131, 31))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans ExtraBold")
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.label_16.setFont(font)
        self.label_16.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: transparent;")
        self.label_16.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_16.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
        self.label_16.setObjectName("label_16")
        self.label_17 = QtWidgets.QLabel(self.frame)
        self.label_17.setGeometry(QtCore.QRect(397, 250, 141, 31))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans ExtraBold")
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.label_17.setFont(font)
        self.label_17.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: transparent;")
        self.label_17.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_17.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
        self.label_17.setObjectName("label_17")
        self.label_18 = QtWidgets.QLabel(self.frame)
        self.label_18.setGeometry(QtCore.QRect(40, 430, 131, 31))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans ExtraBold")
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.label_18.setFont(font)
        self.label_18.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: transparent;")
        self.label_18.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_18.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
        self.label_18.setObjectName("label_18")
        self.label_19 = QtWidgets.QLabel(self.frame)
        self.label_19.setGeometry(QtCore.QRect(214, 430, 151, 31))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans ExtraBold")
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.label_19.setFont(font)
        self.label_19.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: transparent;")
        self.label_19.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_19.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
        self.label_19.setObjectName("label_19")
        self.label_20 = QtWidgets.QLabel(self.frame)
        self.label_20.setGeometry(QtCore.QRect(214, 610, 151, 31))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans ExtraBold")
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.label_20.setFont(font)
        self.label_20.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: transparent;")
        self.label_20.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_20.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
        self.label_20.setObjectName("label_20")
        self.label_21 = QtWidgets.QLabel(self.frame)
        self.label_21.setGeometry(QtCore.QRect(397, 610, 121, 31))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans ExtraBold")
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.label_21.setFont(font)
        self.label_21.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: transparent;")
        self.label_21.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_21.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
        self.label_21.setObjectName("label_21")
        self.label_22 = QtWidgets.QLabel(self.frame)
        self.label_22.setGeometry(QtCore.QRect(36, 610, 131, 31))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans ExtraBold")
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.label_22.setFont(font)
        self.label_22.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: transparent;")
        self.label_22.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_22.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
        self.label_22.setObjectName("label_22")
        self.label_23 = QtWidgets.QLabel(self.frame)
        self.label_23.setGeometry(QtCore.QRect(400, 430, 131, 31))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans ExtraBold")
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.label_23.setFont(font)
        self.label_23.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: transparent;")
        self.label_23.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_23.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
        self.label_23.setObjectName("label_23")
        self.happy2 = QtWidgets.QLabel(self.frame)
        self.happy2.setGeometry(QtCore.QRect(390, 140, 150, 150))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans ExtraBold")
        font.setPointSize(9)
        self.happy2.setFont(font)
        self.happy2.setStyleSheet("QLabel {\n"
"    color: white;\n"
"    padding: 1px;\n"
"}\n"
"\n"
"QLabel:hover {\n"
"    border: 1px solid white;\n"
"    border-radius: 0;  /* Remove rounding on hover */\n"
"}\n"
"")
        self.happy2.setText("")
        self.happy2.setPixmap(QtGui.QPixmap(os.path.join(media_path, "default_cover.png")))
        self.happy2.setScaledContents(True)
        self.happy2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.happy2.setObjectName("happy2")
        self.sad2 = QtWidgets.QLabel(self.frame)
        self.sad2.setGeometry(QtCore.QRect(210, 140, 150, 150))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans ExtraBold")
        font.setPointSize(9)
        self.sad2.setFont(font)
        self.sad2.setStyleSheet("QLabel {\n"
"    color: white;\n"
"    padding: 1px;\n"
"}\n"
"\n"
"QLabel:hover {\n"
"    border: 1px solid white;\n"
"    border-radius: 0;  /* Remove rounding on hover */\n"
"}\n"
"")
        self.sad2.setText("")
        self.sad2.setPixmap(QtGui.QPixmap(os.path.join(media_path, "default_cover.png")))
        self.sad2.setScaledContents(True)
        self.sad2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.sad2.setObjectName("sad2")
        self.happy1 = QtWidgets.QLabel(self.frame)
        self.happy1.setGeometry(QtCore.QRect(30, 140, 150, 150))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans ExtraBold")
        font.setPointSize(9)
        self.happy1.setFont(font)
        self.happy1.setStyleSheet("QLabel {\n"
"    color: white;\n"
"    padding: 1px;\n"
"}\n"
"\n"
"QLabel:hover {\n"
"    border: 1px solid white;\n"
"    border-radius: 0;  /* Remove rounding on hover */\n"
"}\n"
"")
        self.happy1.setText("")
        self.happy1.setPixmap(QtGui.QPixmap(os.path.join(media_path, "default_cover.png")))
        self.happy1.setScaledContents(True)
        self.happy1.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.happy1.setObjectName("happy1")
        self.angry1 = QtWidgets.QLabel(self.frame)
        self.angry1.setGeometry(QtCore.QRect(30, 320, 150, 150))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans ExtraBold")
        font.setPointSize(9)
        self.angry1.setFont(font)
        self.angry1.setStyleSheet("QLabel {\n"
"    color: white;\n"
"    padding: 1px;\n"
"}\n"
"\n"
"QLabel:hover {\n"
"    border: 1px solid white;\n"
"    border-radius: 0;  /* Remove rounding on hover */\n"
"}\n"
"")
        self.angry1.setText("")
        self.angry1.setPixmap(QtGui.QPixmap(os.path.join(media_path, "default_cover.png")))
        self.angry1.setScaledContents(True)
        self.angry1.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.angry1.setObjectName("angry1")
        self.sad3 = QtWidgets.QLabel(self.frame)
        self.sad3.setGeometry(QtCore.QRect(210, 320, 150, 150))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans ExtraBold")
        font.setPointSize(9)
        self.sad3.setFont(font)
        self.sad3.setStyleSheet("QLabel {\n"
"    color: white;\n"
"    padding: 1px;\n"
"}\n"
"\n"
"QLabel:hover {\n"
"    border: 1px solid white;\n"
"    border-radius: 0;  /* Remove rounding on hover */\n"
"}\n"
"")
        self.sad3.setText("")
        self.sad3.setPixmap(QtGui.QPixmap(os.path.join(media_path, "default_cover.png")))
        self.sad3.setScaledContents(True)
        self.sad3.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.sad3.setObjectName("sad3")
        self.neutral1 = QtWidgets.QLabel(self.frame)
        self.neutral1.setGeometry(QtCore.QRect(390, 320, 150, 150))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans ExtraBold")
        font.setPointSize(9)
        self.neutral1.setFont(font)
        self.neutral1.setStyleSheet("QLabel {\n"
"    color: white;\n"
"    padding: 1px;\n"
"}\n"
"\n"
"QLabel:hover {\n"
"    border: 1px solid white;\n"
"    border-radius: 0;  /* Remove rounding on hover */\n"
"}\n"
"")
        self.neutral1.setText("")
        self.neutral1.setPixmap(QtGui.QPixmap(os.path.join(media_path, "default_cover.png")))
        self.neutral1.setScaledContents(True)
        self.neutral1.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.neutral1.setObjectName("neutral1")
        self.neutral2 = QtWidgets.QLabel(self.frame)
        self.neutral2.setGeometry(QtCore.QRect(30, 500, 150, 150))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans ExtraBold")
        font.setPointSize(9)
        self.neutral2.setFont(font)
        self.neutral2.setStyleSheet("QLabel {\n"
"    color: white;\n"
"    padding: 1px;\n"
"}\n"
"\n"
"QLabel:hover {\n"
"    border: 1px solid white;\n"
"    border-radius: 0;  /* Remove rounding on hover */\n"
"}\n"
"")
        self.neutral2.setText("")
        self.neutral2.setPixmap(QtGui.QPixmap(os.path.join(media_path, "default_cover.png")))
        self.neutral2.setScaledContents(True)
        self.neutral2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.neutral2.setObjectName("neutral2")
        self.sad1 = QtWidgets.QLabel(self.frame)
        self.sad1.setGeometry(QtCore.QRect(210, 500, 150, 150))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans ExtraBold")
        font.setPointSize(9)
        self.sad1.setFont(font)
        self.sad1.setStyleSheet("QLabel {\n"
"    color: white;\n"
"    padding: 1px;\n"
"}\n"
"\n"
"QLabel:hover {\n"
"    border: 1px solid white;\n"
"    border-radius: 0;  /* Remove rounding on hover */\n"
"}\n"
"")
        self.sad1.setText("")
        self.sad1.setPixmap(QtGui.QPixmap(os.path.join(media_path, "default_cover.png")))
        self.sad1.setScaledContents(True)
        self.sad1.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.sad1.setObjectName("sad1")
        self.angry2 = QtWidgets.QLabel(self.frame)
        self.angry2.setGeometry(QtCore.QRect(390, 500, 150, 150))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans ExtraBold")
        font.setPointSize(9)
        self.angry2.setFont(font)
        self.angry2.setStyleSheet("QLabel {\n"
"    color: white;\n"
"    padding: 1px;\n"
"}\n"
"\n"
"QLabel:hover {\n"
"    border: 1px solid white;\n"
"    border-radius: 0;  /* Remove rounding on hover */\n"
"}\n"
"")
        self.angry2.setText("")
        self.angry2.setPixmap(QtGui.QPixmap(os.path.join(media_path, "default_cover.png")))
        self.angry2.setScaledContents(True)
        self.angry2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.angry2.setObjectName("angry2")
        self.label_13 = QtWidgets.QLabel(self.frame)
        self.label_13.setGeometry(QtCore.QRect(510, 30, 41, 41))
        self.label_13.setText("")
        self.label_13.setPixmap(QtGui.QPixmap(os.path.join(media_path, "arrow-left.svg")))
        self.label_13.setScaledContents(True)
        self.label_13.setObjectName("label_13")
        self.angry2.raise_()
        self.sad1.raise_()
        self.neutral2.raise_()
        self.neutral1.raise_()
        self.sad3.raise_()
        self.angry1.raise_()
        self.happy1.raise_()
        self.sad2.raise_()
        self.happy2.raise_()
        self.label_2.raise_()
        self.pushButton.raise_()
        self.label_15.raise_()
        self.label_16.raise_()
        self.label_17.raise_()
        self.label_18.raise_()
        self.label_19.raise_()
        self.label_20.raise_()
        self.label_21.raise_()
        self.label_22.raise_()
        self.label_23.raise_()
        self.label_13.raise_()
        self.verticalLayout.addWidget(self.frame)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_2.setText(_translate("Form", "What kind of artist do you like?"))
        self.pushButton.setText(_translate("Form", "Next"))
        self.label_15.setText("")
        self.label_16.setText("")
        self.label_17.setText("")
        self.label_18.setText("")
        self.label_19.setText("")
        self.label_20.setText("")
        self.label_21.setText("")
        self.label_22.setText("")
        self.label_23.setText("")

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

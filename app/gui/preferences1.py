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
        font.setPointSize(10)
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
        self.label_15.setGeometry(QtCore.QRect(48, 250, 111, 31))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans ExtraBold")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label_15.setFont(font)
        self.label_15.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: transparent;")
        self.label_15.setAlignment(QtCore.Qt.AlignCenter)
        self.label_15.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
        self.label_15.setObjectName("label_15")
        self.label_16 = QtWidgets.QLabel(self.frame)
        self.label_16.setGeometry(QtCore.QRect(220, 250, 131, 31))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans ExtraBold")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label_16.setFont(font)
        self.label_16.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: transparent;")
        self.label_16.setAlignment(QtCore.Qt.AlignCenter)
        self.label_16.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
        self.label_16.setObjectName("label_16")
        self.label_17 = QtWidgets.QLabel(self.frame)
        self.label_17.setGeometry(QtCore.QRect(410, 250, 111, 31))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans ExtraBold")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label_17.setFont(font)
        self.label_17.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: transparent;")
        self.label_17.setAlignment(QtCore.Qt.AlignCenter)
        self.label_17.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
        self.label_17.setObjectName("label_17")
        self.label_18 = QtWidgets.QLabel(self.frame)
        self.label_18.setGeometry(QtCore.QRect(40, 430, 131, 31))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans ExtraBold")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label_18.setFont(font)
        self.label_18.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: transparent;")
        self.label_18.setAlignment(QtCore.Qt.AlignCenter)
        self.label_18.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
        self.label_18.setObjectName("label_18")
        self.label_19 = QtWidgets.QLabel(self.frame)
        self.label_19.setGeometry(QtCore.QRect(210, 430, 151, 31))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans ExtraBold")
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.label_19.setFont(font)
        self.label_19.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: transparent;")
        self.label_19.setAlignment(QtCore.Qt.AlignCenter)
        self.label_19.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
        self.label_19.setObjectName("label_19")
        self.label_20 = QtWidgets.QLabel(self.frame)
        self.label_20.setGeometry(QtCore.QRect(209, 610, 151, 31))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans ExtraBold")
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.label_20.setFont(font)
        self.label_20.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: transparent;")
        self.label_20.setAlignment(QtCore.Qt.AlignCenter)
        self.label_20.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
        self.label_20.setObjectName("label_20")
        self.label_21 = QtWidgets.QLabel(self.frame)
        self.label_21.setGeometry(QtCore.QRect(401, 610, 121, 31))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans ExtraBold")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label_21.setFont(font)
        self.label_21.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: transparent;")
        self.label_21.setAlignment(QtCore.Qt.AlignCenter)
        self.label_21.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
        self.label_21.setObjectName("label_21")
        self.label_22 = QtWidgets.QLabel(self.frame)
        self.label_22.setGeometry(QtCore.QRect(40, 610, 131, 31))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans ExtraBold")
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.label_22.setFont(font)
        self.label_22.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: transparent;")
        self.label_22.setAlignment(QtCore.Qt.AlignCenter)
        self.label_22.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
        self.label_22.setObjectName("label_22")
        self.label_23 = QtWidgets.QLabel(self.frame)
        self.label_23.setGeometry(QtCore.QRect(400, 430, 131, 31))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans ExtraBold")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label_23.setFont(font)
        self.label_23.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: transparent;")
        self.label_23.setAlignment(QtCore.Qt.AlignCenter)
        self.label_23.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
        self.label_23.setObjectName("label_23")
        self.label_24 = QtWidgets.QLabel(self.frame)
        self.label_24.setGeometry(QtCore.QRect(424, 340, 81, 81))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans ExtraBold")
        font.setPointSize(10)
        self.label_24.setFont(font)
        self.label_24.setStyleSheet("background-color: transparent;")
        self.label_24.setText("")
        self.label_24.setPixmap(QtGui.QPixmap(os.path.join(media_path, "pop.png")))
        self.label_24.setScaledContents(True)
        self.label_24.setObjectName("label_24")
        self.label_24.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)

        self.folk = QtWidgets.QLabel(self.frame)
        self.folk.setGeometry(QtCore.QRect(390, 140, 150, 150))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans ExtraBold")
        font.setPointSize(10)
        self.folk.setFont(font)
        self.folk.setStyleSheet("QLabel {\n"
"    background: qlineargradient(\n"
"        spread:pad,\n"
"        x1:0, y1:0,\n"
"        x2:1, y2:1,\n"
"        stop:0 #5A3E1B,   /* deep earth brown */\n"
"        stop:1 #C9A882    /* warm tan */\n"
"    );\n"
"    color: white;\n"
"    border-radius: 8px;\n"
"    padding: 10px;\n"
"}\n"
"\n"
"QLabel:hover {\n"
"    border: 1px solid white;\n"
"}\n"
"")
        self.folk.setText("")
        self.folk.setObjectName("folk")
        self.electronic = QtWidgets.QLabel(self.frame)
        self.electronic.setGeometry(QtCore.QRect(210, 140, 150, 150))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans ExtraBold")
        font.setPointSize(10)
        self.electronic.setFont(font)
        self.electronic.setStyleSheet("QLabel {\n"
"    background: qlineargradient(\n"
"        spread:pad,\n"
"        x1:0, y1:0,\n"
"        x2:1, y2:1,\n"
"        stop:0 #0A00A2,   /* deep neon blue */\n"
"        stop:1 #8A00FF    /* electric purple */\n"
"    );\n"
"    color: white;\n"
"    border-radius: 8px;\n"
"    padding: 10px;\n"
"}\n"
"\n"
"QLabel:hover {\n"
"    border: 1px solid white;\n"
"}\n"
"")
        self.electronic.setText("")
        self.electronic.setObjectName("electronic")
        self.hiphop = QtWidgets.QLabel(self.frame)
        self.hiphop.setGeometry(QtCore.QRect(30, 140, 150, 150))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans ExtraBold")
        font.setPointSize(10)
        self.hiphop.setFont(font)
        self.hiphop.setStyleSheet("QLabel {\n"
"    background: qlineargradient(\n"
"        spread:pad,\n"
"        x1:0, y1:0,\n"
"        x2:1, y2:1,\n"
"        stop:0 #8C6A03,   /* dark gold */\n"
"        stop:1 #C29B38    /* deep bronze */\n"
"    );\n"
"    color: white;\n"
"    border-radius: 8px;\n"
"    padding: 10px;\n"
"}\n"
"\n"
"QLabel:hover {\n"
"    border: 1px solid white;\n"
"}\n"
"")
        self.hiphop.setText("")
        self.hiphop.setObjectName("hiphop")
        self.rock = QtWidgets.QLabel(self.frame)
        self.rock.setGeometry(QtCore.QRect(30, 320, 150, 150))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans ExtraBold")
        font.setPointSize(10)
        self.rock.setFont(font)
        self.rock.setStyleSheet("QLabel {\n"
"    background: qlineargradient(\n"
"        x1:0, y1:0,\n"
"        x2:1, y2:1,\n"
"        stop:0 #8C2B2B,   /* medium-dark red */\n"
"        stop:1 #D96464    /* medium-light red */\n"
"    );\n"
"    color: white;\n"
"    border-radius: 8px;\n"
"    padding: 10px;\n"
"}\n"
"\n"
"QLabel:hover {\n"
"    border: 1px solid white;\n"
"}\n"
"")
        self.rock.setText("")
        self.rock.setObjectName("rock")
        self.instrumental = QtWidgets.QLabel(self.frame)
        self.instrumental.setGeometry(QtCore.QRect(210, 320, 150, 150))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans ExtraBold")
        font.setPointSize(10)
        self.instrumental.setFont(font)
        self.instrumental.setStyleSheet("QLabel {\n"
"    background: qlineargradient(\n"
"        spread:pad,\n"
"        x1:0, y1:0,\n"
"        x2:1, y2:1,\n"
"        stop:0 #2F4A6A,   /* lighter deep blue */\n"
"        stop:1 #7FB4E8    /* sky blue */\n"
"    );\n"
"    color: white;\n"
"    border-radius: 8px;\n"
"    padding: 10px;\n"
"}\n"
"\n"
"QLabel:hover {\n"
"    border: 1px solid white;\n"
"}\n"
"")
        self.instrumental.setText("")
        self.instrumental.setObjectName("instrumental")
        self.pop = QtWidgets.QLabel(self.frame)
        self.pop.setGeometry(QtCore.QRect(390, 320, 150, 150))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans ExtraBold")
        font.setPointSize(10)
        self.pop.setFont(font)
        self.pop.setStyleSheet("QLabel {\n"
"    background: qlineargradient(\n"
"        spread:pad,\n"
"        x1:0, y1:0,\n"
"        x2:1, y2:1,\n"
"        stop:0 #7028C4,   /* darker purple */\n"
"        stop:1 #C79BFF    /* darker light lavender */\n"
"    );\n"
"    color: white;\n"
"    border-radius: 8px;\n"
"    padding: 10px;\n"
"}\n"
"\n"
"QLabel:hover {\n"
"    border: 1px solid white;\n"
"}\n"
"")
        self.pop.setText("")
        self.pop.setObjectName("pop")
        self.experimental = QtWidgets.QLabel(self.frame)
        self.experimental.setGeometry(QtCore.QRect(30, 500, 150, 150))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans ExtraBold")
        font.setPointSize(10)
        self.experimental.setFont(font)
        self.experimental.setStyleSheet("QLabel {\n"
"    background: qlineargradient(\n"
"        x1:0, y1:0,\n"
"        x2:1, y2:1,\n"
"        stop:0 #0F6A7A,   /* darker teal */\n"
"        stop:1 #7FF5D2    /* light mint glow */\n"
"    );\n"
"    color: white;\n"
"    border-radius: 8px;\n"
"    padding: 10px;\n"
"}\n"
"\n"
"QLabel:hover {\n"
"    border: 1px solid white;\n"
"}\n"
"")
        self.experimental.setText("")
        self.experimental.setObjectName("experimental")
        self.international = QtWidgets.QLabel(self.frame)
        self.international.setGeometry(QtCore.QRect(210, 500, 150, 150))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans ExtraBold")
        font.setPointSize(10)
        self.international.setFont(font)
        self.international.setStyleSheet("QLabel {\n"
"    background: qlineargradient(\n"
"        x1:0, y1:0,\n"
"        x2:1, y2:1,\n"
"        stop:0 #997800,   /* darker golden yellow */\n"
"        stop:1 #FFD966    /* lighter golden yellow */\n"
"    );\n"
"    color: white;\n"
"    border-radius: 8px;\n"
"    padding: 10px;\n"
"}\n"
"\n"
"QLabel:hover {\n"
"    border: 1px solid white;\n"
"}\n"
"")
        self.international.setText("")
        self.international.setObjectName("international")
        self.label_10 = QtWidgets.QLabel(self.frame)
        self.label_10.setGeometry(QtCore.QRect(390, 500, 150, 150))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans ExtraBold")
        font.setPointSize(10)
        self.label_10.setFont(font)
        self.label_10.setStyleSheet("QLabel {\n"
"    background: qlineargradient(\n"
"        x1:0, y1:0,\n"
"        x2:1, y2:1,\n"
"        stop:0 #5E6A3F,   /* soft olive green */\n"
"        stop:1 #E5E2B6    /* very light wheat */\n"
"    );\n"
"    color: white;\n"
"    border-radius: 8px;\n"
"    padding: 10px;\n"
"}\n"
"\n"
"QLabel:hover {\n"
"    border: 1px solid white;\n"
"}\n"
"")
        self.label_10.setText("")
        self.label_10.setObjectName("label_10")
        self.label_25 = QtWidgets.QLabel(self.frame)
        self.label_25.setGeometry(QtCore.QRect(61, 340, 81, 81))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans ExtraBold")
        font.setPointSize(10)
        self.label_25.setFont(font)
        self.label_25.setStyleSheet("background-color: transparent;")
        self.label_25.setText("")
        self.label_25.setPixmap(QtGui.QPixmap(os.path.join(media_path, "rock.png")))
        self.label_25.setScaledContents(True)
        self.label_25.setObjectName("label_25")
        self.label_25.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
        self.label_26 = QtWidgets.QLabel(self.frame)
        self.label_26.setGeometry(QtCore.QRect(246, 340, 81, 81))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans ExtraBold")
        font.setPointSize(10)
        self.label_26.setFont(font)
        self.label_26.setStyleSheet("background-color: transparent;")
        self.label_26.setText("")
        self.label_26.setPixmap(QtGui.QPixmap(os.path.join(media_path, "instrumental.png")))
        self.label_26.setScaledContents(True)
        self.label_26.setObjectName("label_26")
        self.label_26.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
        self.label_27 = QtWidgets.QLabel(self.frame)
        self.label_27.setGeometry(QtCore.QRect(246, 520, 81, 81))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans ExtraBold")
        font.setPointSize(10)
        self.label_27.setFont(font)
        self.label_27.setStyleSheet("background-color: transparent;")
        self.label_27.setText("")
        self.label_27.setPixmap(QtGui.QPixmap(os.path.join(media_path, "international.png")))
        self.label_27.setScaledContents(True)
        self.label_27.setObjectName("label_27")
        self.label_27.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
        self.label_28 = QtWidgets.QLabel(self.frame)
        self.label_28.setGeometry(QtCore.QRect(426, 520, 81, 81))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans ExtraBold")
        font.setPointSize(10)
        self.label_28.setFont(font)
        self.label_28.setStyleSheet("background-color: transparent;")
        self.label_28.setText("")
        self.label_28.setPixmap(QtGui.QPixmap(os.path.join(media_path, "acoustic.png")))
        self.label_28.setScaledContents(True)
        self.label_28.setObjectName("label_28")
        self.label_28.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
        self.label_29 = QtWidgets.QLabel(self.frame)
        self.label_29.setGeometry(QtCore.QRect(66, 520, 81, 81))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans ExtraBold")
        font.setPointSize(10)
        self.label_29.setFont(font)
        self.label_29.setStyleSheet("background-color: transparent;")
        self.label_29.setText("")
        self.label_29.setPixmap(QtGui.QPixmap(os.path.join(media_path, "experimental.png")))
        self.label_29.setScaledContents(True)
        self.label_29.setObjectName("label_29")
        self.label_29.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
        self.label_30 = QtWidgets.QLabel(self.frame)
        self.label_30.setGeometry(QtCore.QRect(70, 160, 71, 81))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans ExtraBold")
        font.setPointSize(10)
        self.label_30.setFont(font)
        self.label_30.setStyleSheet("background-color: transparent;")
        self.label_30.setText("")
        self.label_30.setPixmap(QtGui.QPixmap(os.path.join(media_path, "hip-hop.png")))
        self.label_30.setScaledContents(True)
        self.label_30.setObjectName("label_30")
        self.label_30.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
        self.label_31 = QtWidgets.QLabel(self.frame)
        self.label_31.setGeometry(QtCore.QRect(246, 160, 81, 81))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans ExtraBold")
        font.setPointSize(10)
        self.label_31.setFont(font)
        self.label_31.setStyleSheet("background-color: transparent;")
        self.label_31.setText("")
        self.label_31.setPixmap(QtGui.QPixmap(os.path.join(media_path, "electronic.png")))
        self.label_31.setScaledContents(True)
        self.label_31.setObjectName("label_31")
        self.label_31.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
        self.label_32 = QtWidgets.QLabel(self.frame)
        self.label_32.setGeometry(QtCore.QRect(420, 160, 81, 81))
        font = QtGui.QFont()
        font.setFamily("Plus Jakarta Sans ExtraBold")
        font.setPointSize(10)
        self.label_32.setFont(font)
        self.label_32.setStyleSheet("background-color: transparent;")
        self.label_32.setText("")
        self.label_32.setPixmap(QtGui.QPixmap(os.path.join(media_path, "folk.png")))
        self.label_32.setScaledContents(True)
        self.label_32.setObjectName("label_32")
        self.label_32.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
        self.label_10.raise_()
        self.international.raise_()
        self.experimental.raise_()
        self.pop.raise_()
        self.instrumental.raise_()
        self.rock.raise_()
        self.hiphop.raise_()
        self.electronic.raise_()
        self.folk.raise_()
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
        self.label_24.raise_()
        self.label_25.raise_()
        self.label_26.raise_()
        self.label_27.raise_()
        self.label_28.raise_()
        self.label_29.raise_()
        self.label_30.raise_()
        self.label_31.raise_()
        self.label_32.raise_()
        self.verticalLayout.addWidget(self.frame)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_2.setText(_translate("Form", "What kind of music do you like?"))
        self.pushButton.setText(_translate("Form", "Next"))
        self.label_15.setText(_translate("Form", "HIP-HOP"))
        self.label_16.setText(_translate("Form", "ELECTRONIC"))
        self.label_17.setText(_translate("Form", "FOLK"))
        self.label_18.setText(_translate("Form", "ROCK"))
        self.label_19.setText(_translate("Form", "INSTRUMENTAL"))
        self.label_20.setText(_translate("Form", "INTERNATIONAL"))
        self.label_21.setText(_translate("Form", " ACOUSTIC"))
        self.label_22.setText(_translate("Form", "EXPERIMENTAL"))
        self.label_23.setText(_translate("Form", "POP"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

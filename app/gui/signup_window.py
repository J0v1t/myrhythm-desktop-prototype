"""
Signup window for the MyRhythm desktop application.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from PyQt5.QtWidgets import QDialog, QMessageBox
from app.gui.sign_up import Ui_Form
from app.auth.signup_logic import register_user


class SignupWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.error.hide()
        self.ui.error_2.hide()

        # Connect buttons
        self.ui.pushButton.clicked.connect(self.signup)
        self.ui.pushButton_3.clicked.connect(self.open_signin)

    def open_signin(self):
        from app.gui.login_window import LoginWindow
        self.hide()
        # Dispose any existing login_window to prevent duplicates
        if hasattr(self, 'login_window'):
            self.login_window.deleteLater()
            del self.login_window
        self.login_window = LoginWindow()
        result = self.login_window.exec_()
        if result == QDialog.Accepted:
            self.user = self.login_window.user
            self.accept()
        else:
            # If login rejected, stay in signup
            self.show()

    def signup(self):
        name = self.ui.lineEdit.text().strip()
        email = self.ui.lineEdit_3.text().strip()
        password = self.ui.lineEdit_4.text()

        self.ui.error.hide()
        self.ui.error_2.hide()

        if not name or not email or not password:
            if not password:
                self.ui.error.show()
            if not email or '@' not in email or '.' not in email:
                self.ui.error_2.show()
            return

        success, message = register_user(name, email, password)
        if success:
            QMessageBox.information(self, "Success", message)
            self.open_signin()
        else:
            self.ui.error_2.show()
            self.ui.error_2.setText(message)

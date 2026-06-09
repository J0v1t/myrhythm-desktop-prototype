"""
Login window for the MyRhythm desktop application.
"""

from PyQt5.QtWidgets import QDialog
from app.gui.sign_in import Ui_Form
from app.auth.login_logic import authenticate_user


class LoginWindow(QDialog):
    def __init__(self, prefill_email=None, auth_func=authenticate_user):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.error.hide()
        self.user = None
        self.auth_func = auth_func
        if prefill_email:
            self.ui.lineEdit_7.setText(prefill_email)
            self.ui.lineEdit_8.setFocus()

        # Connect buttons
        self.ui.pushButton.clicked.connect(self.open_signup)
        self.ui.pushButton_2.clicked.connect(self.login)

    def open_signup(self):
        from app.gui.signup_window import SignupWindow
        self.hide()
        # Dispose any existing signup_window to prevent duplicates
        if hasattr(self, 'signup_window'):
            self.signup_window.deleteLater()
            del self.signup_window
        self.signup_window = SignupWindow()
        result = self.signup_window.exec_()
        if result == QDialog.Accepted:
            self.user = self.signup_window.user
            self.accept()
        else:
            self.show()

    def login(self):
        email = self.ui.lineEdit_7.text().strip()
        password = self.ui.lineEdit_8.text()

        if not email or not password:
            self.ui.error.show()
            self.ui.error.setText("Please enter email and password")
            return

        success, result = self.auth_func(email, password)
        if success:
            self.ui.error.hide()
            self.user = result  # Store user object
            self.accept()  # Accept the dialog
        else:
            self.ui.error.show()
            self.ui.error.setText(result)

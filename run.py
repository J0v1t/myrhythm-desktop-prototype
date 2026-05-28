import sys

from PyQt5.QtWidgets import QApplication, QDialog

from app.database.db_init import init_db
from app.database.schema import db
from app.database.models.preference import UserPreferences

from app.gui.agreement import AgreementDialog
from app.gui.login_window import LoginWindow
from app.gui.preferences_window import PreferencesWindow
from app.gui.dashboard2 import DashboardWindow

def main():
    # Initialize the database
    init_db()

    # Create the Qt application
    app = QApplication(sys.argv)

    agreement = AgreementDialog()
    agreement_result = agreement.exec_()

    # If the user does NOT accept → exit app
    if agreement_result != QDialog.Accepted:
        sys.exit(0)
        
    # Show the login window
    login_window = LoginWindow()
    if login_window.exec_() == QDialog.Accepted:
        user = login_window.user

        # Check if user has preferences set
        preferences = db.query(UserPreferences).filter_by(user_id=user.id).first()

        if preferences:
            # User has preferences, go directly to dashboard
            dashboard_window = DashboardWindow(user.id)
            dashboard_window.show()
        else:
            # New user, show preferences first
            preferences_window = PreferencesWindow(user)
            preferences_window.show()

    # Start the event loop
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

import sys

from PyQt5.QtWidgets import QApplication, QDialog

from app.database.db_init import init_db
from app.database.schema import db
from app.database.models.preference import UserPreferences

from app.cloud.supabase_data import SupabaseDataClient
from app.gui.agreement import AgreementDialog
from app.gui.login_window import LoginWindow
from app.gui.preferences_window import PreferencesWindow
from app.gui.dashboard2 import DashboardWindow


def _cloud_data_client_for(user):
    access_token = getattr(user, "access_token", None)
    if not access_token:
        return None
    return SupabaseDataClient.from_auth_user(user)


def _has_local_preferences(user):
    return db.query(UserPreferences).filter_by(user_id=user.id).first() is not None


def _has_cloud_preferences(cloud_client, user):
    preferences = cloud_client.get_user_preferences(user.id)
    return cloud_client.has_completed_preferences(preferences)

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
        cloud_client = _cloud_data_client_for(user)

        # Check if user has preferences set. Supabase Auth users use Supabase
        # profile/preference rows; legacy local users keep the SQLite fallback.
        has_preferences = (
            _has_cloud_preferences(cloud_client, user)
            if cloud_client
            else _has_local_preferences(user)
        )

        if has_preferences:
            # User has preferences, go directly to dashboard
            dashboard_window = DashboardWindow(user.id)
            dashboard_window.show()
        else:
            # New user, show preferences first
            save_preferences_func = (
                cloud_client.save_user_preferences if cloud_client else None
            )
            preferences_window = PreferencesWindow(
                user,
                save_preferences_func=save_preferences_func,
            )
            preferences_window.show()

    # Start the event loop
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

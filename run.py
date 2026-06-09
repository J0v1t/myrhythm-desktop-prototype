import sys

from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox

from app.cloud.reviewer_services import ReviewerCloudServices
from app.config.vlc_runtime import check_vlc_readiness
from app.gui.agreement import AgreementDialog
from app.gui.dashboard2 import DashboardWindow
from app.gui.login_window import LoginWindow
from app.gui.preferences_window import PreferencesWindow


def create_reviewer_window(
    user,
    cloud_services,
    dashboard_factory=DashboardWindow,
    preferences_factory=PreferencesWindow,
):
    cloud_services.load_catalog()
    preferences = cloud_services.load_preferences()
    has_preferences = bool(preferences.get("genres")) and bool(
        preferences.get("artists")
    )

    if has_preferences:
        return dashboard_factory(user.id, cloud_services)
    return preferences_factory(
        user,
        save_preferences_func=cloud_services.save_user_preferences,
        cloud_services=cloud_services,
    )


def main():
    app = QApplication(sys.argv)

    vlc_readiness = check_vlc_readiness()
    if not vlc_readiness.ready:
        detail = f"\n\nDetails: {vlc_readiness.error}" if vlc_readiness.error else ""
        QMessageBox.critical(
            None,
            "VLC Required",
            f"{vlc_readiness.message}{detail}",
        )
        return 1

    agreement = AgreementDialog()
    if agreement.exec_() != QDialog.Accepted:
        return 0

    login_window = LoginWindow()
    if login_window.exec_() != QDialog.Accepted:
        return 0

    try:
        cloud_services = ReviewerCloudServices.from_auth_user(login_window.user)
        reviewer_window = create_reviewer_window(login_window.user, cloud_services)
    except Exception as exc:
        QMessageBox.critical(
            None,
            "Cloud Service Unavailable",
            "MyRhythm could not load the authenticated cloud catalog.\n\n"
            f"Details: {exc}",
        )
        return 1

    reviewer_window.show()
    return app.exec_()


if __name__ == "__main__":
    sys.exit(main())

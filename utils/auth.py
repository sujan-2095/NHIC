from flask_login import LoginManager, UserMixin
from db_handler import fetch_patient_by_id

login_manager = LoginManager()

class User(UserMixin):
    def __init__(self, id: str, role: str):
        self.id = id
        self.role = role


def init_auth(app):
    """Initialize Flask-Login for the app and set up the user_loader."""
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    @login_manager.user_loader
    def load_user(user_id):
        if user_id == "admin":
            return User("admin", "admin")
        patient = fetch_patient_by_id(user_id)
        if patient:
            return User(patient["id"], "patient")
        return None

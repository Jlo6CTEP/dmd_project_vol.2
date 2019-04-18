from backend.users.admin import Admin
from backend.users.principal import Principal
from backend.users.student import Student
from backend.users.teacher import Teacher
from backend.db_manager import db

levels = {x[0]: x[1] for x in enumerate([Student, Teacher, Principal, Admin])}


class Backend:
    user = None

    def __init__(self):
        pass

    def login(self, login, password):
        user_row = db.get_by_credentials(login, password)
        if user_row is None:
            raise AssertionError("Incorrect login/password")
        self.user = levels[user_row['level']]()
        self.user.load_from_dict(user_row)

    def logout(self):
        self.user = None


backend = Backend()

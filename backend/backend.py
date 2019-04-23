from backend.users.users import Admin, Principal, Student, Teacher
from backend.db_manager.db_manager import db


roles = ['student', 'teacher', 'principal', 'admin']

levels = {x[0]: x[1] for x in zip(roles, [Student, Teacher, Principal, Admin])}


class Backend:
    user = None

    def __init__(self):
        pass

    def login(self, login, password):
        user_id, user_row = db.get_user_by_credentials(login, password)
        if user_row is None:
            raise AssertionError("Incorrect login/password")
        self.user = levels[user_row['role']]()
        self.user.load_from_dict(user_row)
        self.user.user_id = user_id

    def logout(self):
        self.user = None


backend = Backend()

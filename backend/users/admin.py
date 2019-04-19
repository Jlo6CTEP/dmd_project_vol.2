from backend.users.base_user import BaseUser


class Admin(BaseUser):
    def __init__(self):
        super().__init__()

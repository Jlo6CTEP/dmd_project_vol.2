from copy import copy


class BaseUser:
    user_id = None
    user_info = None

    def __init__(self):
        pass

    def load_from_dict(self, row):
        self.user_info = copy(row)
        if self.user_info.get('_key', None) is not None:
            self.user_info.pop('_key')


class Student(BaseUser):
    def __init__(self):
        super().__init__()


class Teacher(BaseUser):
    def __init__(self):
        super().__init__()


class Principal(BaseUser):
    def __init__(self):
        super().__init__()


class Admin(BaseUser):
    def __init__(self):
        super().__init__()

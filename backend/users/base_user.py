

class BaseUser:
    user_id = None
    login = None
    name = None
    surname = None
    level = None

    def __init__(self):
        pass

    def load_from_dict(self, row):
        pass

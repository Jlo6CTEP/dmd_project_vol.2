class BaseUser:
    user_id = None
    user_info = None

    def __init__(self):
        pass

    def load_from_dict(self, row):
        self.user_info = row

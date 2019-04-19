from PyQt5.QtWidgets import QPushButton

from frontend.user_pages.base_user_page import BasePage


class TeacherPage(BasePage):
    button2 = None

    def __init__(self, parent, user=None):
        super().__init__(parent, user)

        self.button2 = QPushButton("fuck the teachership")
        self.main_layout.insertWidget(self.main_layout.count() - 1, self.button2)

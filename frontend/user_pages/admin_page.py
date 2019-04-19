from PyQt5.QtWidgets import QPushButton

from frontend.user_pages.base_user_page import BasePage


class AdminPage(BasePage):
    button4 = None

    def __init__(self, parent, user=None):
        super().__init__(parent, user)

        self.button4 = QPushButton("fuck you all")
        self.main_layout.insertWidget(self.main_layout.count() - 1, self.button4)

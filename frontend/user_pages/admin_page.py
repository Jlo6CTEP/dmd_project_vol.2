from PyQt5.QtWidgets import QPushButton

from frontend.user_pages.principal_page import PrincipalPage


class AdminPage(PrincipalPage):
    button4 = None

    def __init__(self):
        super().__init__()

        self.button4 = QPushButton("fuck you all")
        self.layout.insertWidget(self.layout.count() - 1, self.button4)

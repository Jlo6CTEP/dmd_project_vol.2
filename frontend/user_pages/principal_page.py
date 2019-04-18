from PyQt5.QtWidgets import QVBoxLayout, QPushButton

from frontend.user_pages.teacher_page import TeacherPage


class PrincipalPage(TeacherPage):
    button3 = None

    def __init__(self):
        super().__init__()

        self.button3 = QPushButton("fuck life")
        self.layout.insertWidget(self.layout.count() - 1, self.button3)

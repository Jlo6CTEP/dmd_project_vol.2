from PyQt5.QtWidgets import QVBoxLayout, QPushButton

from frontend.user_pages.student_page import StudentPage


class TeacherPage(StudentPage):
    button2 = None

    def __init__(self):
        super().__init__()

        self.button2 = QPushButton("fuck the teachership")
        self.layout.insertWidget(self.layout.count() - 1, self.button2)

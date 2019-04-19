from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel

from frontend.course_widgets.base_course import BaseCourse
from backend.db_manager.db_manager import db


class UnEditableCourse(BaseCourse):

    def __init__(self, course, assessment):
        super().__init__(course, assessment)
        course_info = db.get_course_info(course)[1]
        course_info.pop('name')

        text_info = QVBoxLayout()
        for x in course_info.items():
            line = QHBoxLayout()
            line.addWidget(QLabel(str(x[0]) + ':'))
            line.addWidget(QLabel(', '.join(x[1]) if isinstance(x[1], list) else str(x[1])))
            line.addStretch()
            text_info.addLayout(line)
        self.main_info.setLayout(text_info)

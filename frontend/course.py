from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtWidgets import QWidget, QGroupBox

from backend.db_manager.db_manager import db


class BaseCourse(QWidget):
    additional_field = None
    main_info = None
    assessment_info = None

    def __init__(self, course, assessment):
        super().__init__()
        self.assessment_info = assessment

        self.additional_field = QHBoxLayout()
        self.main_info = QGroupBox('Info')

        main_layout = QHBoxLayout()
        main_layout.addWidget(self.main_info)
        main_layout.addWidget(self.assessment_info)
        main_layout.addLayout(self.additional_field)

        course_box = QGroupBox('Course: ' + course)
        course_box.setLayout(main_layout)

        course_layout = QHBoxLayout()
        course_layout.addWidget(course_box)

        self.setLayout(course_layout)


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
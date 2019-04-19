from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QFrame, QGroupBox
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

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.main_info)
        main_layout.addWidget(self.assessment_info)
        main_layout.addLayout(self.additional_field)

        course_box = QGroupBox('Course: ' + course)
        course_box.setLayout(main_layout)

        course_layout = QHBoxLayout()
        course_layout.addWidget(course_box)

        self.setLayout(course_layout)

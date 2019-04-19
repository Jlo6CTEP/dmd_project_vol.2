from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QVBoxLayout, QFormLayout, QGroupBox

from frontend.assessment_widgets.base_assessment import BaseAssessment
from backend.db_manager.db_manager import db


class StudentAssessment(BaseAssessment):

    def __init__(self, student, course):
        super().__init__()
        self.setTitle('Grades')
        grades_layout = QHBoxLayout()
        for x in db.get_student_assessment(student, course)[1].items():
            grades_layout.addWidget(QLabel(x[0] + ': ' + str(x[1])))
        grades_layout.addStretch()
        self.setLayout(grades_layout)

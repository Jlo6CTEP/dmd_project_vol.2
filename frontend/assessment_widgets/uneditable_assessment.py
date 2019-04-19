from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel

from frontend.assessment_widgets.base_assessment import BaseAssessment
from backend.db_manager.db_manager import db


class UnEditableAssessment(BaseAssessment):

    def __init__(self, course):
        super().__init__()
        for x in db.get_assessment(course):
            self.main_layout.addWidget(QLabel(x))


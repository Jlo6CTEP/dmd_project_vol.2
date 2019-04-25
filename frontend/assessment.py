from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFormLayout, QPushButton, QCheckBox, QVBoxLayout, QLineEdit
from PyQt5.QtWidgets import QGroupBox
from PyQt5.QtWidgets import QHBoxLayout, QLabel

from backend.db_manager.db_manager import db
from frontend.button_blocks import ButtonBlock
from frontend.editable_widget import EditableWidget, edit


class BaseAssessment(QGroupBox):

    def __init__(self):
        super().__init__()


class EditableAssessment(BaseAssessment):
    form = None
    info_list = None

    def __init__(self, course):
        super().__init__()
        self.setTitle('Assessment')

        self.form = QFormLayout()
        self.info_list = []

        for x in db.get_course_assessment(course):
            self.info_list.append((EditableWidget(x), QCheckBox()))
            self.form.addRow(*self.info_list[len(self.info_list) - 1])

        new_assessment = QLineEdit()

        add_button = QPushButton()
        add_button.setFixedSize(new_assessment.sizeHint().height(), new_assessment.sizeHint().height())
        add_button.setIcon(QIcon('./images/add.png'))
        add_button.clicked.connect(lambda: self.insert_new(new_assessment, course))
        self.form.addRow(new_assessment, add_button)

        del_button = QPushButton()
        del_button.setIcon(QIcon('./images/del.png'))
        del_button.clicked.connect(lambda: self.remove(course))

        button_block = ButtonBlock(True)
        button_block.block_layout.insertWidget(3, del_button)
        button_block.edit_button.clicked.connect(lambda: edit([f[0] for f in self.info_list]))
        button_block.save_button.clicked.connect(lambda: self.__save(course))

        v_layout = QVBoxLayout()
        v_layout.addLayout(button_block.block_layout)
        v_layout.addLayout(self.form)

        self.setLayout(v_layout)

    def remove(self, course):
        to_remove = []
        for x in self.info_list:
            if x[1].isChecked():
                db.remove_assessment(course, x[0].text())
                self.form.removeRow(x[1])
                to_remove.append(x)
        for x in to_remove:
            self.info_list.remove(x)

    def __save(self, course):
        for x in self.info_list:
            x[0].push_to_db(x[0].text(), db.update_assessment, [course, x[0].old])

    def insert_new(self, line, course):
        db.add_assessment(course, line.text())
        to_info_list = (EditableWidget(line.text()), QCheckBox())
        self.form.insertRow(0, *to_info_list)
        self.info_list.append(to_info_list)
        line.setText('')


class StudentAssessment(BaseAssessment):

    def __init__(self, student, course):
        super().__init__()
        self.setTitle('Grades')
        grades_layout = QHBoxLayout()
        for x in db.get_student_assessment(student, [course])[course].items():
            grades_layout.addWidget(QLabel(x[0] + ': ' + str(x[1])))
        grades_layout.addStretch()
        self.setLayout(grades_layout)


class UnEditableAssessment(BaseAssessment):

    def __init__(self, course):
        super().__init__()

        self.setTitle('Assessments')
        grades_layout = QHBoxLayout()
        for x in db.get_course_assessment(course):
            grades_layout.addWidget(QLabel(x))
        grades_layout.addStretch()
        self.setLayout(grades_layout)



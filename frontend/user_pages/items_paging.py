from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QWidget, QHBoxLayout, QLabel, QLineEdit, QGroupBox, QFormLayout

from backend.users.users import BaseUser
from frontend.editable_widget import EditableWidget
from frontend.user_pages.information import admin_editable_info
from frontend.user_pages.user_information import EditableUserInfo


class BaseItemsPaging(QWidget):
    size = None
    position = None
    page_counter = None
    values = None
    main_layout = None
    h_students_layout = None
    widget_list = None
    items_per_page = 50

    def __init__(self, values):
        super().__init__()

        self.size = len(values)
        self.values = values
        self.position = 0

        self.main_layout = QVBoxLayout()
        self.page = QWidget()
        self.main_layout.addWidget(self.page)

        page_navigator = QHBoxLayout()

        self.page_counter = QLineEdit('1')
        self.page_counter.adjustSize()

        left_arrow = QPushButton()
        left_arrow.setIcon(QIcon('./images/left_arrow.png'))
        left_arrow.setStyleSheet("QPushButton { border: none; }")
        size = self.page_counter.sizeHint().height()
        left_arrow.setFixedSize(size, size)
        left_arrow.clicked.connect(self.go_left)

        right_arrow = QPushButton()
        right_arrow.setIcon(QIcon('./images/right_arrow.png'))
        right_arrow.setStyleSheet("QPushButton { border: none; }")
        right_arrow.setFixedSize(size, size)
        right_arrow.clicked.connect(self.go_right)

        page_navigator.addStretch()
        page_navigator.addWidget(left_arrow)
        page_navigator.addWidget(QLabel("Page:"))
        page_navigator.addWidget(self.page_counter)
        page_navigator.addWidget(QLabel("of {} pages".format(str((self.size - 1) // self.items_per_page + 1))))
        page_navigator.addWidget(right_arrow)
        page_navigator.addStretch()

        self.main_layout.addLayout(page_navigator)
        self.main_layout.addStretch()

        self.initialize_current()
        self.setLayout(self.main_layout)

    def initialize_current(self):
        pass

    def go_left(self):
        if int(self.page_counter.text()) - 1 <= 0:
            return
        if self.position != int(self.page_counter.text()) - 1:
            self.position = int(self.page_counter.text()) - 1
        else:
            self.position -= 1
            self.page_counter.setText(str(self.position + 1))
        self.initialize_current()

    def go_right(self):
        if int(self.page_counter.text()) >= (self.size - 1) // self.items_per_page + 1:
            return
        if self.position != int(self.page_counter.text()) - 1:
            self.position = int(self.page_counter.text()) - 1
        else:
            self.position += 1
            self.page_counter.setText(str(self.position + 1))
        self.initialize_current()

    def search(self, text, widget_list):
        a = widget_list.get(text, None)
        keys = list(self.values.keys())
        if a is None:
            try:
                user = keys.index(text)
            except ValueError:
                return
            self.page_counter.setText(str((user // self.items_per_page + 1)))
            self.position = max(0, user // self.items_per_page)
            self.initialize_current()
            index = user % self.items_per_page
        else:
            index = self.h_students_layout.indexOf(a)
        first = self.h_students_layout.itemAt(0).widget()
        second = self.h_students_layout.itemAt(index).widget()
        if first == second:
            return
        first.setParent(None)
        second.setParent(None)
        self.h_students_layout.insertWidget(0, second)
        self.h_students_layout.insertWidget(index, first)


class EditableUserInfoPaging(BaseItemsPaging):
    def __init__(self, values):
        super().__init__(values)

    def initialize_current(self):
        if self.h_students_layout is not None:
            self.h_students_layout.deleteLater()
        self.h_students_layout = QVBoxLayout()
        self.widget_list = {}
        for x in list(self.values.items())[self.position * self.items_per_page:
        min((self.position + 1) * self.items_per_page, self.size)]:
            user = BaseUser()
            user.user_id = x[0]
            user.load_from_dict(x[1])
            widget = EditableUserInfo(user, admin_editable_info)
            self.widget_list.update({x[0]: widget})
            self.h_students_layout.addWidget(widget)

        self.main_layout.removeWidget(self.page)
        self.page.deleteLater()
        self.page = QWidget()
        self.page.setLayout(self.h_students_layout)
        self.main_layout.insertWidget(0, self.page)


class TeacherStudentsPaging(BaseItemsPaging):
    widget_list_short = None
    widget_list_long = None
    grade_widget = None

    def __init__(self, values, grade_widget):
        self.grade_widget = grade_widget
        self.widget_list_short = []
        self.widget_list_long = []
        self.widget_list = {}
        super().__init__(values)

    def initialize_current(self):
        self.widget_list_short = []
        self.widget_list_long = []
        self.widget_list = {}
        if self.h_students_layout is not None:
            self.h_students_layout.deleteLater()
        self.h_students_layout = QVBoxLayout()
        for x in list(self.values.items())[self.position * self.items_per_page:
        min((self.position + 1) * self.items_per_page, self.size)]:
            h_assessments_layout = QHBoxLayout()
            for assessments in x[1]['assessments'].items():
                assessment_box = QGroupBox(assessments[0])
                assessment_layout = QHBoxLayout()
                for assessment in assessments[1].items():
                    widget = self.grade_widget(assessment[1])
                    self.widget_list_short.append(widget)
                    self.widget_list_long.append((x[0], (assessment[0], widget, assessments[0])))
                    assessment_layout.addWidget(QLabel(assessment[0] + ':'))
                    assessment_layout.addWidget(widget)
                    assessment_layout.addStretch()
                assessment_box.setLayout(assessment_layout)
                h_assessments_layout.addWidget(assessment_box)
            students_box = QGroupBox(x[1]['name'] + ' ' + x[1]['surname'])
            students_box.setLayout(h_assessments_layout)
            self.widget_list.update({x[0]: students_box})
            self.h_students_layout.addWidget(students_box)

        self.main_layout.removeWidget(self.page)
        self.page.deleteLater()
        self.page = QWidget()
        self.page.setLayout(self.h_students_layout)
        self.main_layout.insertWidget(0, self.page)


class PrincipalUserPaging(BaseItemsPaging):
    user_list = None
    user_list_long = None

    def __init__(self, values):
        self.user_list = []
        self.user_list_long = []
        super().__init__(values)

    def initialize_current(self):
        self.user_list = []
        self.user_list_long = []
        self.widget_list = {}
        if self.h_students_layout is not None:
            self.h_students_layout.deleteLater()
        self.h_students_layout = QVBoxLayout()
        for x in list(self.values.items())[self.position * self.items_per_page:
        min((self.position + 1) * self.items_per_page, self.size)]:
            user_line = EditableWidget(','.join(x[1]['courses']))
            self.user_list.append(user_line)
            self.user_list_long.append((user_line, x[0]))

            user_courses = QFormLayout()
            user_courses.addRow(QLabel('courses: '), user_line)

            user = QGroupBox(x[1]['name'] + ' ' + x[1]['surname'])
            user.setLayout(user_courses)
            self.widget_list.update({x[0]: user})
            self.h_students_layout.addWidget(user)
        self.h_students_layout.addStretch()

        self.main_layout.removeWidget(self.page)
        self.page.deleteLater()
        self.page = QWidget()
        self.page.setLayout(self.h_students_layout)
        self.main_layout.insertWidget(0, self.page)

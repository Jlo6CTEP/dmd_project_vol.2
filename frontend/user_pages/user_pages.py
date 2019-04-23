from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QGroupBox, QLineEdit, QFormLayout, QLabel, QPushButton, QToolTip
from PyQt5.QtWidgets import QSizePolicy, QDesktopWidget, QHBoxLayout, QTabWidget
from PyQt5.QtWidgets import QVBoxLayout, QWidget

from backend.db_manager.db_manager import db
from backend.db_manager.documents_structure import course
from frontend.assessment import EditableAssessment
from frontend.assessment import StudentAssessment
from frontend.button_blocks import ButtonBlock
from frontend.course import UnEditableCourse
from frontend.editable_widget import EditableWidget, edit
from frontend.students_tables import AdminUserTable
from frontend.students_tables import PrincipalStudentsTable
from frontend.students_tables import TeacherStudentsTable
from frontend.user_pages.information import self_editable_info
from frontend.user_pages.user_information import EditableUserInfo
from frontend.user_pages.user_information import UnEditableUserInfo


class BasePage(QWidget):
    parent = None
    pages = None
    main_layout = None
    logout_button = None

    def __init__(self, parent, user=None):
        super().__init__()

        self.parent = parent

        size = QDesktopWidget().screenGeometry(-1)

        self.logout_button = QPushButton()
        self.logout_button.setIcon(QIcon('./images/exit.png'))
        self.logout_button.setFixedSize(size.height() // 32, size.height() // 32)
        self.logout_button.clicked.connect(self.logout)

        self.pages = QTabWidget()
        self.pages.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        toolbar = QHBoxLayout()

        toolbar.addStretch()
        toolbar.addWidget(self.logout_button)

        self.main_layout = QVBoxLayout()
        self.main_layout.addLayout(toolbar)
        self.main_layout.addWidget(self.pages)

        self.setLayout(self.main_layout)

    def logout(self):
        self.parent.logout()


class StudentPage(BasePage):

    def __init__(self, parent, user=None):
        super().__init__(parent, user)

        course_info = db.get_user_courses(user.user_id)
        courses_page = QWidget()
        courses_layout = QVBoxLayout()

        v_layout = QVBoxLayout()
        v_layout.addWidget(UnEditableUserInfo(user))
        v_layout.addStretch()

        user_widget = QWidget()
        user_widget.setLayout(v_layout)

        self.pages.addTab(user_widget, 'Personal Info')

        for x in course_info:
            try:
                assessment = StudentAssessment(user.user_id, x[0])
            except KeyError:
                assessment = QWidget()
            course_widget = UnEditableCourse(x[0], assessment)
            courses_layout.addWidget(course_widget)
        courses_layout.addStretch()
        courses_page.setLayout(courses_layout)
        self.pages.addTab(courses_page, 'My Courses')


class TeacherPage(BasePage):

    def __init__(self, parent, user=None):
        super().__init__(parent, user)

        v_layout = QVBoxLayout()
        v_layout.addWidget(EditableUserInfo(user, self_editable_info))
        v_layout.addStretch()

        user_widget = QWidget()
        user_widget.setLayout(v_layout)

        self.pages.addTab(user_widget, 'Personal Info')
        courses_page = QWidget()
        courses_layout = QVBoxLayout()

        for x in db.get_user_courses(user.user_id):
            assessment = EditableAssessment(x[0])
            course_widget = UnEditableCourse(x[0], assessment)
            courses_layout.addWidget(course_widget)
        courses_layout.addStretch()
        courses_page.setLayout(courses_layout)
        button_block = ButtonBlock()

        students = TeacherStudentsTable(db.get_students_for_teacher(user.user_id), button_block)
        self.pages.addTab(courses_page, 'My Courses')
        self.pages.addTab(students, 'Students')




class PrincipalPage(BasePage):

    def __init__(self, parent, user=None):
        super().__init__(parent, user)

        v_layout = QVBoxLayout()
        v_layout.addWidget(EditableUserInfo(user, self_editable_info))
        v_layout.addStretch()

        user_widget = QWidget()
        user_widget.setLayout(v_layout)

        self.pages.addTab(user_widget, 'Personal Info')
        courses_page = QWidget()
        courses_layout = QVBoxLayout()

        for x in db.get_courses():
            assessment = QWidget()
            course_widget = UnEditableCourse(x['name'], assessment)
            courses_layout.addWidget(course_widget)
        courses_layout.addStretch()
        courses_page.setLayout(courses_layout)

        new_course_form = QFormLayout()
        input_fields = []

        add_button = QPushButton()
        add_button.setIcon(QIcon('./images/add.png'))
        add_button.clicked.connect(lambda: self.add_new(courses_layout, input_fields))

        for x in course:
            line = QLineEdit()
            input_fields.append(line)
            new_course_form.addRow(QLabel(x), line)

        new_course_layout = QVBoxLayout()
        new_course_layout.addLayout(new_course_form)
        new_course_layout.addWidget(add_button)

        new_course = QGroupBox('Add new course')
        new_course.setLayout(new_course_layout)

        courses_layout.insertWidget(0, new_course)

        students = PrincipalStudentsTable(db.get_students_for_teacher(user.user_id))
        self.pages.addTab(courses_page, 'Courses')
        self.pages.addTab(students, 'Students')

        button_block = ButtonBlock()

        teacher_layout = QVBoxLayout()
        teacher_layout.addLayout(button_block)

        teacher_list = []
        teacher_list_long = []

        button_block.edit_button.clicked.connect(lambda: edit(teacher_list))
        button_block.save_button.clicked.connect(lambda: self.__save(teacher_list_long))

        for x in db.get_teachers_and_students():
            teacher_line = EditableWidget(','.join(x['courses']))
            teacher_list.append(teacher_line)
            teacher_list_long.append((teacher_line, x['_key']))

            teacher_courses = QFormLayout()
            teacher_courses.addRow(QLabel('courses: '), teacher_line)

            teacher = QGroupBox(x['name'] + ' ' + x['surname'])
            teacher.setLayout(teacher_courses)
            teacher_layout.addWidget(teacher)
        teacher_layout.addStretch()

        teacher_widget = QWidget()
        teacher_widget.setLayout(teacher_layout)

        self.pages.addTab(teacher_widget, 'Teachers')

    def add_new(self, courses_layout, input_fields):
        try:
            item = {x[0]: x[1].text() for x in zip(course, input_fields)}
            text = [x for x in item['assessment'].replace(' ', '').split(',') if len(x) > 0]
            item['assessment'] = text
            assessment = QWidget()
            db.insert_course(item)
            course_widget = UnEditableCourse(item['name'], assessment)
            courses_layout.insertWidget(1, course_widget)
            QToolTip.showText(self.mapToGlobal(self.main_layout.geometry().topLeft()), 'Course insert succeeded')
        except (KeyError, AssertionError):
            QToolTip.showText(self.mapToGlobal(self.main_layout.geometry().topLeft()), 'Course insert failed')

    def __save(self, teachers):
        try:
            for x in teachers:
                if x[0].text() != x[0].old:
                    text = [x for x in x[0].text().replace(' ', '').split(',') if len(x) > 0]
                    db.edit_user_courses(x[1], text)
                    x[0].old = x[0].text()
            QToolTip.showText(self.mapToGlobal(self.main_layout.geometry().topLeft()), 'Courses edit succeeded')
        except (KeyError, AssertionError):
            QToolTip.showText(self.mapToGlobal(self.main_layout.geometry().topLeft()), 'Courses edit failed')


class AdminPage(BasePage):

    def __init__(self, parent, user=None):
        super().__init__(parent, user)

        v_layout = QVBoxLayout()
        v_layout.addWidget(UnEditableUserInfo(user))
        v_layout.addStretch()

        user_widget = QWidget()
        user_widget.setLayout(v_layout)

        self.pages.addTab(user_widget, 'Personal Info')
        self.pages.addTab(AdminUserTable(), 'Users')
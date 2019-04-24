from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QGroupBox, QLineEdit, QFormLayout, QLabel, QPushButton, QToolTip, QScrollArea
from PyQt5.QtWidgets import QSizePolicy, QDesktopWidget, QHBoxLayout, QTabWidget
from PyQt5.QtWidgets import QVBoxLayout, QWidget

from backend.backend import levels
from backend.db_manager.db_manager import db
from backend.db_manager.documents_structure import course
from frontend.assessment import EditableAssessment
from frontend.assessment import StudentAssessment
from frontend.button_blocks import ButtonBlock
from frontend.course import UnEditableCourse
from frontend.editable_widget import edit
from frontend.students_tables import AdminUserTable
from frontend.students_tables import PrincipalStudentsTable
from frontend.students_tables import TeacherStudentsTable
from frontend.user_pages.information import self_editable_info
from frontend.user_pages.items_paging import PrincipalUserPaging
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
    spatial_search_data = None
    wrapper = None

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

        students = PrincipalStudentsTable(db.get_students())

        courses_scroll = QScrollArea()
        courses_scroll.setWidget(courses_page)
        courses_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        courses_scroll.setWidgetResizable(True)

        self.pages.addTab(courses_scroll, 'Courses')
        self.pages.addTab(students, 'Students')

        paging = PrincipalUserPaging(db.get_teachers_and_students())

        button_block = ButtonBlock()
        button_block.edit_button.clicked.connect(lambda: edit(paging.user_list))
        button_block.save_button.clicked.connect(lambda: self.__save(paging.user_list_long))

        user_layout = QVBoxLayout()
        user_layout.addLayout(button_block)

        scroll = QScrollArea()
        scroll.setWidget(paging)
        scroll.setWidgetResizable(True)

        user_layout.addWidget(scroll)

        teacher_widget = QWidget()
        teacher_widget.setLayout(user_layout)

        self.pages.addTab(teacher_widget, 'User courses')

        spatial_search = QWidget()

        ss_layout = QVBoxLayout()

        result_box = QGroupBox('Result')
        scroll = QScrollArea()
        scroll.setWidget(result_box)
        scroll.setWidgetResizable(True)

        search_line = QLineEdit()
        search_button = QPushButton()
        search_button.setIcon(QIcon('./images/search.png'))
        search_button.setFixedSize(search_line.sizeHint().height(), search_line.sizeHint().height())
        search_button.clicked.connect(lambda: self.spatial_search(search_line))

        search_layout = QHBoxLayout()
        search_layout.addWidget(search_line)
        search_layout.addWidget(search_button)
        search_layout.addStretch()

        self.spatial_search_data = QWidget()
        self.wrapper = QHBoxLayout()
        self.wrapper.addWidget(self.spatial_search_data)

        result_box.setLayout(self.wrapper)

        ss_layout.addLayout(search_layout)
        ss_layout.addWidget(scroll)

        spatial_search.setLayout(ss_layout)

        self.pages.addTab(spatial_search, 'Spatial Search')

    def spatial_search(self, line):
        self.spatial_search_data.deleteLater()

        new_result = QVBoxLayout()

        spatial_searh_data = db.spatial_search(line.text())
        if spatial_searh_data is not None:
            for x in spatial_searh_data:
                x[0].update({'Average_grade': str(x[3])})
                user = levels[x[0]['role']]()
                user.load_from_dict(x[0])
                new_result.addWidget(UnEditableUserInfo(user, ['Average_grade']))
            new_result.addStretch()

        self.wrapper.removeWidget(self.spatial_search_data)
        self.spatial_search_data = QWidget()
        self.spatial_search_data.setLayout(new_result)
        self.wrapper.addWidget(self.spatial_search_data)

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

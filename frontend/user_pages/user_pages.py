from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QGroupBox, QLineEdit, QFormLayout, QLabel, QPushButton, QToolTip, QScrollArea
from PyQt5.QtWidgets import QSizePolicy, QDesktopWidget, QHBoxLayout, QTabWidget
from PyQt5.QtWidgets import QVBoxLayout, QWidget

from backend.backend import levels
from backend.db_manager.db_manager import db
from backend.db_manager.documents_structure import course
from frontend.assessment import EditableAssessment
from frontend.assessment import StudentAssessment
from frontend.button_blocks import ButtonBlock, SearchButtonBlock, SearchBox
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

        students = TeacherStudentsTable(db.get_students_for_teacher(user.user_id))
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

        courses_page.setLayout(courses_layout)

        courses_scroll = QScrollArea()
        courses_scroll.setWidget(courses_page)
        courses_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        courses_scroll.setWidgetResizable(True)

        search_box = SearchBox()

        main_layout = QVBoxLayout()
        main_layout.addLayout(search_box.search_form)
        main_layout.addWidget(new_course)
        main_layout.addWidget(courses_scroll)

        wrapper = QWidget()
        wrapper.setLayout(main_layout)

        self.pages.addTab(wrapper, 'Courses')

        students = PrincipalStudentsTable(db.get_students())
        self.pages.addTab(students, 'Students')

        paging = PrincipalUserPaging(db.get_teachers_and_students())

        utility_box = SearchButtonBlock()
        utility_box.edit_button.clicked.connect(lambda: edit(paging.user_list))
        utility_box.save_button.clicked.connect(lambda: self.__save(paging.user_list_long))

        utility_box.search_button.clicked.connect\
            (lambda: paging.search(utility_box.search_line.text(), paging.widget_list))

        user_layout = QVBoxLayout()
        user_layout.addWidget(utility_box)

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

        search_layout = SearchBox()

        search_layout.search_button.clicked.connect(lambda: self.spatial_search(search_layout.search_line))

        self.spatial_search_data = QWidget()
        self.wrapper = QHBoxLayout()
        self.wrapper.addWidget(self.spatial_search_data)

        result_box.setLayout(self.wrapper)

        ss_layout.addLayout(search_layout.search_form)
        ss_layout.addWidget(scroll)

        spatial_search.setLayout(ss_layout)

        self.pages.addTab(spatial_search, 'Spatial Search')

    def spatial_search(self, line):
        spatial_search_data = db.spatial_search(line.text())
        #try:
        #except KeyError:
        #    QToolTip.showText(self.mapToGlobal(self.main_layout.geometry().topLeft()), 'No such student')
        #    return
        self.spatial_search_data.deleteLater()
        new_result = QVBoxLayout()
        if spatial_search_data is not None:
            for x in spatial_search_data:
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

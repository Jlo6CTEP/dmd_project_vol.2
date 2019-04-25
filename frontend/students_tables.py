from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton, QToolTip, QScrollArea
from PyQt5.QtWidgets import QVBoxLayout, QFormLayout, QLabel, QGroupBox, QLineEdit
from pyArango.theExceptions import DocumentNotFoundError

from backend.db_manager.db_manager import db
from backend.db_manager.documents_structure import student
from frontend.button_blocks import SearchButtonBlock, SearchBox
from frontend.editable_widget import EditableWidget, edit
from frontend.user_pages.items_paging import EditableUserInfoPaging, TeacherStudentsPaging


class AdminUserTable(QGroupBox):

    def __init__(self):
        super().__init__('Users')

        user_info = db.get_users_for_admin()

        main_layout = QVBoxLayout()

        scroll = QScrollArea()

        paging = EditableUserInfoPaging(user_info)

        new_user_form = QFormLayout()
        new_user_layout = QVBoxLayout()

        field_list = []

        add_button = QPushButton()
        add_button.setIcon(QIcon('./images/add.png'))
        add_button.clicked.connect(lambda: self.add_new(field_list, paging))

        for x in student:
            field = QLineEdit()
            field_list.append(field)
            new_user_form.addRow(QLabel(x), field)

        new_user_layout.addLayout(new_user_form)
        new_user_layout.addWidget(add_button, Qt.AlignRight)

        new_item = QGroupBox('Add new user')
        new_item.setLayout(new_user_layout)

        scroll.setWidget(paging)
        scroll.setWidgetResizable(True)

        search_box = SearchBox()
        search_box.search_button.clicked.connect\
            (lambda: paging.search(search_box.search_line.text(), paging.widget_list))

        main_layout.addWidget(new_item)
        main_layout.addLayout(search_box.search_form)
        main_layout.addWidget(scroll)
        main_layout.addStretch()

        self.setLayout(main_layout)

    def add_new(self, field_list, paging):
        try:
            user = {x[0]: x[1].text() for x in zip(student, field_list)}
            key = user['name'][0] + '.' + user['surname']
            user.update({'_key': key})
            user['courses'] = user['courses'].replace(' ', '').split(',')
            db.insert_user(key, user)
            QToolTip.showText(self.mapToGlobal(paging.geometry().topLeft()), 'User successfully added')
            paging.values.insert(paging.items_per_page * paging.position, user)
            paging.initialize_current()
        except (AssertionError, KeyError, DocumentNotFoundError):
            QToolTip.showText(self.mapToGlobal(paging.geometry().topLeft()), 'User insert failed')


class TeacherStudentsTable(QGroupBox):
    grade_widget = EditableWidget
    paging = None

    def __init__(self, user_info):
        super().__init__('Your students')

        self.paging = TeacherStudentsPaging(user_info, self.grade_widget)

        scroll = QScrollArea()

        main_layout = QVBoxLayout()

        utility_box = SearchButtonBlock()
        utility_box.edit_button.clicked.connect(lambda: edit(self.paging.widget_list_short))
        utility_box.save_button.clicked.connect(lambda: self.__save(self.paging.widget_list_long))
        utility_box.search_button.clicked.connect(
            lambda: self.paging.search(utility_box.search_line.text(), self.paging.widget_list))

        scroll.setWidget(self.paging)
        scroll.setWidgetResizable(True)

        main_layout.addWidget(utility_box)
        main_layout.addWidget(scroll)
        self.setLayout(main_layout)

    def __save(self, widget_list):
        for x in widget_list:
            if not x[1][1].isReadOnly():
                x[1][1].push_to_db(x[1][0], db.edit_assessment_grade, [x[0], x[1][2]])


class PrincipalStudentsTable(TeacherStudentsTable):
    grade_widget = QLabel

    def __init__(self, user_info):
        super().__init__(user_info)
        self.setTitle('Students')

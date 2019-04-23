from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton, QToolTip
from PyQt5.QtWidgets import QVBoxLayout, QFormLayout, QLabel, QHBoxLayout, QGroupBox, QLineEdit

from backend.backend import levels
from backend.db_manager.db_manager import db
from backend.db_manager.documents_structure import student
from backend.users.users import BaseUser
from frontend.button_blocks import ButtonBlock
from frontend.button_blocks import SearchButtonBlock
from frontend.editable_widget import EditableWidget, edit
from frontend.user_pages.information import admin_editable_info
from frontend.user_pages.user_information import EditableUserInfo


class AdminUserTable(QGroupBox):

    def __init__(self):
        super().__init__('Users')

        button_block = ButtonBlock()

        del_button = QPushButton()
        del_button.setIcon(QIcon('./images/del.png'))
        button_block.insertWidget(3, del_button)

        user_info = db.get_users_for_admin()

        main_layout = QVBoxLayout()

        for x in user_info:
            user = BaseUser()
            user.user_id = x.pop('_key')
            user.load_from_dict(x)
            main_layout.addWidget(EditableUserInfo(user, admin_editable_info, is_expanded=False))
        main_layout.addStretch()

        new_user_form = QFormLayout()
        new_user_layout = QVBoxLayout()

        field_list = []

        add_button = QPushButton()
        add_button.setIcon(QIcon('./images/add.png'))
        add_button.clicked.connect(lambda: self.add_new(field_list, main_layout))

        for x in student:
            field = QLineEdit()
            field_list.append(field)
            new_user_form.addRow(QLabel(x), field)

        new_user_layout.addLayout(new_user_form)
        new_user_layout.addWidget(add_button, Qt.AlignRight)

        new_item = QGroupBox('Add new user')
        new_item.setLayout(new_user_layout)

        main_layout.insertWidget(0, new_item)

        self.setLayout(main_layout)

    def add_new(self, field_list, main_layout):
        try:
            user = {x[0]: x[1].text() for x in zip(student, field_list)}
            key = user['name'][0] + '.' + user['surname']
            user.update({'_key': key})
            user_object = levels[user['role']]()
            user_object.load_from_dict(user)
            user_object.user_id = key
            db.insert_user(key, user)
            QToolTip.showText(self.mapToGlobal(main_layout.geometry().topLeft()), 'User successfully added')
            main_layout.insertWidget(1, EditableUserInfo(user_object, admin_editable_info,
                                                         is_expanded=False))
        except (AssertionError, KeyError):
            QToolTip.showText(self.mapToGlobal(main_layout.geometry().topLeft()), 'User insert failed')


class TeacherStudentsTable(QGroupBox):
    grade_widget = EditableWidget

    def __init__(self, user_info, button_block=None):
        super().__init__('Your students')

        widget_list_long = []
        widget_list_short = []

        main_layout = QVBoxLayout()

        utility_box = SearchButtonBlock(button_block)
        if button_block:
            button_block.edit_button.clicked.connect(lambda: edit(widget_list_short))
            button_block.save_button.clicked.connect(lambda: self.__save(widget_list_long))

        main_layout.addLayout(utility_box)

        h_students_layout = QVBoxLayout()
        for x in user_info.items():
            h_assessments_layout = QHBoxLayout()
            for assessments in x[1]['assessments'].items():
                assessment_box = QGroupBox(assessments[0])
                assessment_layout = QHBoxLayout()
                for assessment in assessments[1].items():
                    widget = self.grade_widget(assessment[1])
                    widget_list_short.append(widget)
                    widget_list_long.append((x[0], (assessment[0], widget, assessments[0])))
                    assessment_layout.addWidget(QLabel(assessment[0] + ':'))
                    assessment_layout.addWidget(widget)
                    assessment_layout.addStretch()
                assessment_box.setLayout(assessment_layout)
                h_assessments_layout.addWidget(assessment_box)
            students_box = QGroupBox(x[1]['name'] + ' ' + x[1]['surname'])
            students_box.setLayout(h_assessments_layout)
            h_students_layout.addWidget(students_box)
        h_students_layout.addStretch()

        main_layout.addLayout(h_students_layout)
        main_layout.addStretch()
        self.setLayout(main_layout)

    def __save(self, widget_list):
        for x in widget_list:
            if not x[1][1].isReadOnly():
                x[1][1].push_to_db(x[1][0], db.edit_assessment_grade, [x[0], x[1][2]])

    def __search(self, text, widget_list):
        print(widget_list.get(text, None))


class PrincipalStudentsTable(TeacherStudentsTable):
    grade_widget = QLabel

    def __init__(self, user_info, button_block=None):
        super().__init__(user_info, button_block)
        self.setTitle('Students')

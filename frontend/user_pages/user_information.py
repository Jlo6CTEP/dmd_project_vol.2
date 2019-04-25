from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel, QFormLayout
from PyQt5.QtWidgets import QWidget, QGroupBox, QVBoxLayout, QDesktopWidget

from backend.db_manager.db_manager import db
from frontend.button_blocks import ButtonBlock
from frontend.editable_widget import EditableWidget, edit
from frontend.user_pages.information import info_to_show


class BaseUserInfo(QWidget):
    text_info = None
    main_layout = None
    __collapsible_box = None

    def __init__(self, user):
        super().__init__()

        size = QDesktopWidget().screenGeometry(-1)
        user_info = QHBoxLayout()
        pic = QLabel()
        pic.setPixmap(QPixmap('./images/user.png'))

        pic_groupbox = QGroupBox('Profile picture')

        img_layout = QVBoxLayout()
        img_layout.addWidget(pic)

        pic_groupbox.setLayout(img_layout)
        user_info.addWidget(pic_groupbox)

        self.text_info = QVBoxLayout()

        text_groupbox = QGroupBox('Personal information')
        text_groupbox.setLayout(self.text_info)
        user_info.addWidget(text_groupbox)

        self.main_layout = QVBoxLayout()
        self.main_layout.addLayout(user_info)

        self.setLayout(self.main_layout)


class EditableUserInfo(BaseUserInfo):
    def __init__(self, user, editable_info, is_buttons=True):
        super().__init__(user)

        if user is None:
            return

        widgets_list = []
        form = QFormLayout()

        for t in info_to_show:
            data = user.user_info[t]
            widget = EditableWidget(data) if t in editable_info else QLabel(data)
            form.addRow(QLabel(t + ':'), widget)
            widgets_list.append(widget)

        self.text_info.addLayout(form)
        if is_buttons:
            buttons = ButtonBlock()

            buttons.save_button.clicked.connect(lambda: save(user, widgets_list))
            buttons.edit_button.clicked.connect(lambda: edit(widgets_list))
            self.main_layout.insertWidget(0, buttons)


def save(user, widgets_list):
    for widget in zip(info_to_show, [x for x in widgets_list if isinstance(x, EditableWidget)]):
        widget[1].push_to_db(widget[0], db.update_user_info, [user.user_id])


class UnEditableUserInfo(BaseUserInfo):
    def __init__(self, user, additional_fields=None):
        super().__init__(user)

        if user is None:
            return

        if additional_fields is None:
            additional_fields = []

        for x in info_to_show + additional_fields:
            line = QHBoxLayout()
            line.addWidget(QLabel(x + ':'))
            line.addWidget(QLabel(str(user.user_info[x])))
            line.addStretch()
            self.text_info.addLayout(line)
        self.text_info.addStretch()

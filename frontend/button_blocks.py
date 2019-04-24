from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QFormLayout
from PyQt5.QtWidgets import QPushButton


class ButtonBlock(QHBoxLayout):
    save_button = None
    edit_button = None

    def __init__(self, align_left=False):
        super().__init__()

        self.save_button = QPushButton()
        self.save_button.setIcon(QIcon('./images/save.png'))

        self.edit_button = QPushButton()
        self.edit_button.setIcon(QIcon('./images/edit.png'))

        if not align_left:
            self.addStretch()
        self.addWidget(self.save_button)
        self.addWidget(self.edit_button)
        if align_left:
            self.addStretch()


class SearchButtonBlock(QHBoxLayout):
    button_block = None
    search_line = None

    def __init__(self, button_block=None):
        super().__init__()

        self.search_line = QLineEdit()
        label = QLabel()

        pic = QPixmap('./images/search.png')
        pic = pic.scaledToWidth(self.search_line.sizeHint().height())

        label.setPixmap(pic)
        label.setFixedSize(QSize(self.search_line.sizeHint().height(), self.search_line.sizeHint().height()))

        search_form = QFormLayout()
        search_form.addRow(self.search_line, label)

        self.addLayout(search_form)
        self.addStretch()

        if button_block:
            self.button_block = button_block
            self.addLayout(button_block)


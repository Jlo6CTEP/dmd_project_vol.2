from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QFormLayout, QWidget
from PyQt5.QtWidgets import QPushButton


class ButtonBlock(QWidget):
    save_button = None
    edit_button = None
    block_layout = None

    def __init__(self, align_left=False):
        super().__init__()

        self.save_button = QPushButton()
        self.save_button.setIcon(QIcon('./images/save.png'))

        self.edit_button = QPushButton()
        self.edit_button.setIcon(QIcon('./images/edit.png'))

        self.block_layout = QHBoxLayout()

        if not align_left:
            self.block_layout.addStretch()
        self.block_layout.addWidget(self.save_button)
        self.block_layout.addWidget(self.edit_button)
        if align_left:
            self.block_layout.addStretch()


class SearchBox(QWidget):
    search_line = None
    search_button = None
    search_form = None

    def __init__(self):
        super().__init__()

        self.search_line = QLineEdit()
        self.search_button = QPushButton()

        self.search_button.setIcon(QIcon('./images/search.png'))
        self.search_button. \
            setFixedSize(QSize(self.search_line.sizeHint().height(), self.search_line.sizeHint().height()))

        self.search_form = QFormLayout()
        self.search_form.addRow(self.search_line, self.search_button)


class SearchButtonBlock(ButtonBlock, SearchBox, QWidget):

    def __init__(self):
        ButtonBlock.__init__(self, False)
        SearchBox.__init__(self)
        QWidget.__init__(self)

        layout = QHBoxLayout()
        layout.addLayout(self.search_form)
        layout.addLayout(self.block_layout)
        self.setLayout(layout)

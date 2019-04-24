from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import QLineEdit


class EditableWidget(QLineEdit):
    editing = None
    old = None

    def __init__(self, value):
        super().__init__()
        self.old = value

        self.editing = False

        self.setText(value)
        self.toggle_edit()

    def toggle_edit(self):
        if self.isReadOnly():
            self.setReadOnly(False)
            palette = QPalette()
            palette.setColor(QPalette.Base, Qt.white)
            palette.setColor(QPalette.Text, Qt.black)
        else:
            self.setReadOnly(True)
            if self.old != self.text():
                self.setText(self.old)
            palette = QPalette()
            palette.setColor(QPalette.Base, Qt.gray)
            palette.setColor(QPalette.Text, Qt.darkGray)
        self.setPalette(palette)

    def push_to_db(self, key, function, args):
        if self.text() != self.old:
            function(*args, {key: self.text()})
            self.old = self.text()


def edit(widgets_list):
    for widget in widgets_list:
        if isinstance(widget, EditableWidget):
            widget.toggle_edit()

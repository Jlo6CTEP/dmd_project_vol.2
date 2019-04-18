from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import QWidget, QApplication, QDesktopWidget, QMainWindow, QLineEdit, QLabel, QPushButton, \
    QVBoxLayout, QHBoxLayout


class LoginForm(QWidget):
    password_field = None
    login_field = None
    login_button = None
    width, height = None, None

    def __init__(self, width, height, pixmap):
        super().__init__()

        self.width, self.height = width, height
        self.line_field = QLineEdit()

        font = QFont("Times", 20, QFont.Bold)
        font.setUnderline(True)

        text_field = QLabel("ZMSC E-SAS")
        text_field.setFont(font)
        text_field.setAlignment(Qt.AlignCenter)
        text_field.adjustSize()

        self.login_field = QLineEdit()
        self.password_field = QLineEdit()
        self.button = QPushButton("Log in")

        label = QLabel(self)
        label.setPixmap(pixmap)

        v_layout_back = QVBoxLayout()
        v_layout_back.addWidget(text_field)
        v_layout_back.addWidget(label)
        v_layout_back.addStretch()

        frame_layout = QVBoxLayout()
        frame_layout.addWidget(self.login_field)
        frame_layout.addWidget(self.password_field)
        frame_layout.addWidget(self.button)

        frame = QWidget()
        frame.setLayout(frame_layout)
        frame.setAutoFillBackground(True)

        v_layout_front = QVBoxLayout()
        v_layout_front.addStretch()
        v_layout_front.addWidget(frame)
        v_layout_front.addStretch()

        h_layout_back = QHBoxLayout()
        h_layout_back.addStretch()
        h_layout_back.addLayout(v_layout_back)
        h_layout_back.addStretch()

        h_layout_front = QHBoxLayout()
        h_layout_front.addStretch()
        h_layout_front.addLayout(v_layout_front)
        h_layout_front.addStretch()

        widget_wrapper1 = QWidget(self)

        widget_wrapper2 = QWidget(self)
        widget_wrapper2.setFixedSize(self.width, self.height)

        widget_wrapper1.setFixedSize(self.width, self.height)
        widget_wrapper1.raise_()

        widget_wrapper1.setLayout(h_layout_front)
        widget_wrapper2.setLayout(h_layout_back)



from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton


class StudentPage(QWidget):
    button1 = None
    layout = None

    def __init__(self):
        super().__init__()

        self.button1 = QPushButton("fuck the study")

        self.layout = QVBoxLayout()

        self.layout.addStretch()
        self.layout.addWidget(self.button1)
        self.layout.addStretch()

        self.setLayout(self.layout)



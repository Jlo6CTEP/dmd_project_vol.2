from PyQt5.QtWidgets import QWidget, QGridLayout, QVBoxLayout, QHBoxLayout


class CoursePage(QWidget):
    width = None
    x = None
    y = None
    grid = None

    def __init__(self, width):
        super().__init__()

        self.x, self.y = 0, 0
        self.width = width

        self.grid = QGridLayout()

        v_layout = QVBoxLayout()
        h_layout = QHBoxLayout()

        v_layout.addLayout(self.grid)
        v_layout.addStretch()

        h_layout.addLayout(v_layout)
        h_layout.addStretch()

        self.setLayout(h_layout)

    def add_course(self, page):
        self.grid.addWidget(page, self.y, self.x)
        if self.x >= self.width:
            self.x = 0
            self.y += 1
        else:
            self.x += 1

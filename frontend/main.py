import sys

from PyQt5.QtWidgets import QWidget, QApplication, QDesktopWidget, QMainWindow

from frontend.login_form import LoginForm


class RegisterForm(QMainWindow):
    screen = None
    width, height = None, None

    def __init__(self):
        super().__init__()

        size = QDesktopWidget().screenGeometry(-1)
        self.width, self.height = size.width() // 3, size.height() // 1.75
        self.setFixedSize(self.width, self.height)

        qr = self.frameGeometry()
        center = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(center)
        self.move(qr.topLeft())
        self.init_ui()

    def init_ui(self):
        main_widget = LoginForm(self.width, self.height)
        self.setCentralWidget(main_widget)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = RegisterForm()
    sys.exit(app.exec_())

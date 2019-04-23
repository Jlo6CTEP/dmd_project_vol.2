import ctypes
import sys

from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QApplication, QDesktopWidget, QMainWindow, QStackedWidget, \
    QWIDGETSIZE_MAX, QToolTip

from backend.backend import backend, roles
from frontend.login_form import LoginForm
from frontend.user_pages.user_pages import BasePage, PrincipalPage, StudentPage, TeacherPage, AdminPage

levels = {x[0]: x[1] for x in zip(roles, [StudentPage, TeacherPage, PrincipalPage, AdminPage])}


class MainWindow(QMainWindow):
    screen = None
    width, height = None, None
    picture = None
    login_form = None
    user_page = None
    pages = None

    def __init__(self):
        super().__init__()

        if sys.platform != 'linux':
            my_app_id = 'InnoUI.DMD_project.ez_A_for_course.101'  # arbitrary string
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(my_app_id)
        self.setWindowIcon(QIcon("../images/main_logo.png"))

        size = QDesktopWidget().screenGeometry(-1)
        self.width = size.width() // 5
        self.picture = QPixmap("../images/main_logo.png").scaledToWidth(self.width - self.width // 20)

        self.height = self.picture.height() + size.height() // 16
        self.setFixedSize(self.width, self.height)
        self.setWindowTitle('DmD2')
        self.pages = QStackedWidget()

        qr = self.frameGeometry()
        center = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(center)
        self.move(qr.topLeft())
        self.init_ui()

    def login(self, login, password):
        try:
            backend.login(login, password)
        except AssertionError as exception:
            QToolTip.showText(self.mapToGlobal(self.login_form.geometry().center()), 'Invalid credentials')
            return
        self.user_page = levels[backend.user.user_info['role']](self, backend.user)
        self.pages.addWidget(self.user_page)
        self.pages.setCurrentWidget(self.user_page)

        self.repaint()
        self.setMaximumSize(QWIDGETSIZE_MAX, QWIDGETSIZE_MAX)
        self.resize(self.width * 2, self.height * 2)
        qr = self.frameGeometry()
        center = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(center)
        self.move(qr.topLeft())

    def logout(self):
        backend.logout()
        self.pages.setCurrentWidget(self.login_form)
        self.repaint()
        self.setFixedSize(self.width, self.height)
        qr = self.frameGeometry()
        center = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(center)
        self.move(qr.topLeft())
        self.pages.removeWidget(self.user_page)

    def init_ui(self):
        self.login_form = LoginForm(self.width, self.height, self.picture)
        self.user_page = BasePage(self)

        self.pages.addWidget(self.login_form)
        self.pages.setCurrentWidget(self.login_form)

        self.setCentralWidget(self.pages)
        self.login_form.button.clicked.connect(
            lambda: self.login(self.login_form.login_field.text(),
                               self.login_form.password_field.text()))
        self.show()


if __name__ == '__main__':
    print('kek')
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())

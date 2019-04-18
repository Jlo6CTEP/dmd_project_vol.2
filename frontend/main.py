import ctypes
import sys

from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QApplication, QDesktopWidget, QMainWindow, QErrorMessage, QStackedWidget, \
    QWIDGETSIZE_MAX

from backend.backend import backend
from frontend.login_form import LoginForm
from frontend.user_pages.admin_page import AdminPage
from frontend.user_pages.student_page import StudentPage


class MainWindow(QMainWindow):
    error_dialog = None
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
        self.height = self.picture.height() // 0.85
        self.setFixedSize(self.width, self.height)
        self.error_dialog = QErrorMessage()
        self.setWindowTitle('DmD2')
        self.pages = QStackedWidget()

        qr = self.frameGeometry()
        center = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(center)
        self.move(qr.topLeft())
        self.init_ui()

    def collapse_login(self, login, password):
        try:
            backend.login(login, password)
        except AssertionError() as exception:
            self.error_dialog.showMessage(exception)
            return
        self.pages.setCurrentWidget(self.user_page)
        self.repaint()
        self.setMaximumSize(QWIDGETSIZE_MAX, QWIDGETSIZE_MAX)
        self.resize(self.width * 2, self.height * 2)
        qr = self.frameGeometry()
        center = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(center)
        self.move(qr.topLeft())

    def init_ui(self):
        self.login_form = LoginForm(self.width, self.height, self.picture)
        self.user_page = AdminPage()

        self.pages.addWidget(self.user_page)
        self.pages.addWidget(self.login_form)
        self.pages.setCurrentWidget(self.login_form)

        self.setCentralWidget(self.pages)
        self.login_form.button.clicked.connect(
            lambda: self.collapse_login(self.login_form.login_field.text(),
                                        self.login_form.password_field.text()))
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())

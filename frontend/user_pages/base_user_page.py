from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QSizePolicy, QDesktopWidget, \
    QHBoxLayout, QTabWidget, QLabel, QGroupBox

info_to_show = ['login', 'name', 'surname', 'role', 'registration date']


class BasePage(QWidget):
    parent = None
    pages = None
    main_layout = None
    logout_button = None

    def __init__(self, parent, user=None):
        super().__init__()

        self.parent = parent

        size = QDesktopWidget().screenGeometry(-1)

        self.logout_button = QPushButton()
        self.logout_button.setIcon(QIcon('../images/exit.png'))
        self.logout_button.setFixedSize(size.height() // 32, size.height() // 32)
        self.logout_button.clicked.connect(self.logout)

        self.pages = QTabWidget()
        self.pages.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        if user is not None:
            user_info = QHBoxLayout()
            pic = QLabel()
            pic.setPixmap(QPixmap('../images/user.png'))

            pic_groupbox = QGroupBox('Profile picture')

            user_info.addSpacing(size.height() // 32)
            img_layout = QVBoxLayout()
            img_layout.addWidget(pic)

            pic_groupbox.setLayout(img_layout)
            user_info.addWidget(pic_groupbox)

            text_info = QVBoxLayout()
            for x in info_to_show:
                line = QHBoxLayout()
                line.addStretch()
                line.addWidget(QLabel(x + ':'))
                line.addWidget(QLabel(str(user.user_info[x])))
                line.addStretch()
                text_info.addLayout(line)

            text_groupbox = QGroupBox('Personal information')
            text_groupbox.setLayout(text_info)
            user_info.addWidget(text_groupbox)

            v_box = QVBoxLayout()
            v_box.addLayout(user_info)
            v_box.addStretch()
            wrapper = QWidget()
            wrapper.setLayout(v_box)
            self.pages.addTab(wrapper, 'My Profile')

        toolbar = QHBoxLayout()

        toolbar.addStretch()
        toolbar.addWidget(self.logout_button)

        self.main_layout = QVBoxLayout()
        self.main_layout.addLayout(toolbar)
        self.main_layout.addWidget(self.pages)

        self.setLayout(self.main_layout)

    def logout(self):
        self.parent.logout()

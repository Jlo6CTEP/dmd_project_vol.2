from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QLineEdit


class CollapsibleBox(QtWidgets.QWidget):
    __is_expanded = None
    __start_expanded = None

    def __init__(self, is_expanded, title="", parent=None):
        super(CollapsibleBox, self).__init__(parent)

        self.__is_expanded = is_expanded
        self.__start_expanded = is_expanded

        self.setFixedHeight(QLineEdit().sizeHint().height())

        self.toggle_button = QtWidgets.QToolButton(text=title, checkable=True, checked=False)
        self.toggle_button.setStyleSheet("QToolButton { border: none; }")
        self.toggle_button.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.toggle_button.setArrowType(QtCore.Qt.ArrowType.RightArrow)
        self.toggle_button.clicked.connect(self.on_pressed)

        self.toggle_animation = QtCore.QParallelAnimationGroup(self)

        self.content_area = QtWidgets.QScrollArea(maximumHeight=0, minimumHeight=0)
        self.content_area.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.content_area.setFrameShape(QtWidgets.QFrame.NoFrame)

        lay = QtWidgets.QVBoxLayout(self)
        lay.setSpacing(0)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(self.toggle_button)
        lay.addWidget(self.content_area)

        self.toggle_animation.addAnimation(QtCore.QPropertyAnimation(self, b"minimumHeight"))
        self.toggle_animation.addAnimation(QtCore.QPropertyAnimation(self, b"maximumHeight"))
        self.toggle_animation.addAnimation(QtCore.QPropertyAnimation(self.content_area, b"maximumHeight"))
        if is_expanded:
            self.on_pressed()

    @QtCore.pyqtSlot()
    def on_pressed(self):
        checked = self.__is_expanded
        self.toggle_button.setArrowType(
            QtCore.Qt.ArrowType.DownArrow if not checked else QtCore.Qt.ArrowType.RightArrow)
        self.toggle_animation.setDirection(
            QtCore.QAbstractAnimation.Forward if not checked else QtCore.QAbstractAnimation.Backward)
        self.toggle_animation.start()
        self.__is_expanded = not checked

    def set_content_layout(self, layout):
        lay = self.content_area.layout()
        del lay
        self.content_area.setLayout(layout)
        collapsed_height = self.sizeHint().height() - self.content_area.maximumHeight()
        content_height = layout.sizeHint().height()
        for i in range(self.toggle_animation.animationCount()):
            animation = self.toggle_animation.animationAt(i)

            animation.setDuration(10)
            if self.__start_expanded:
                animation.setStartValue(collapsed_height + content_height)
                animation.setEndValue(collapsed_height)
            else:
                animation.setStartValue(collapsed_height)
                animation.setEndValue(collapsed_height + content_height)

        content_animation = self.toggle_animation.animationAt(self.toggle_animation.animationCount() - 1)
        content_animation.setDuration(10)

        if self.__start_expanded:
            content_animation.setStartValue(content_height)
            content_animation.setEndValue(0)
        else:
            content_animation.setStartValue(0)
            content_animation.setEndValue(content_height)

# -*- coding: utf-8 -*-
import sys

################################################################################
## Form generated from reading UI file 'untitled.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
                            QMetaObject, QObject, QPoint, QRect,
                            QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
                           QFont, QFontDatabase, QGradient, QIcon,
                           QImage, QKeySequence, QLinearGradient, QPainter,
                           QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QLayout, QSizePolicy, QToolBox,
                               QWidget)
from gnatwriter import GnatWriter

from definitions import CONFIG_PATH
from widgets.Author import Author
from widgets.CommonTreeView import CommonTreeView
from widgets.Submission import Submission


class Ui_Form(QWidget):
    def __init__(self, gnaw=None):
        super().__init__()

        self.gnaw = gnaw

        self.toolBox = QToolBox()
        self.page = Author()
        self.toolBox.addItem(self.page, u"Page 1")
        self.page_2 = Submission()
        self.toolBox.addItem(self.page_2, u"Page 2")
        self.toolBox.setCurrentIndex(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    gnaw = GnatWriter(CONFIG_PATH)
    window = Ui_Form(gnaw=gnaw)
    window.show()
    sys.exit(app.exec())

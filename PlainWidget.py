import os

from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtGui import QIcon, QFont
from PySide6.QtCore import QSize
import sys

from gnatwriter import GnatWriter

from definitions import ROOT_DIR


class Widget(QWidget):
    def __init__(self, backend=None):
        super().__init__()

        self.gnaw = gnaw if gnaw else None
        self.setWindowTitle("Widget")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    CONFIG_PATH = os.path.join(ROOT_DIR, 'config.cfg')
    gnaw = GnatWriter(CONFIG_PATH)
    window = Widget(backend=gnaw)
    window.show()
    sys.exit(app.exec())

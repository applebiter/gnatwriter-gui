import datetime
import os
import sys
from datetime import date, datetime

from gnatwriter import GnatWriter
from PySide6.QtWidgets import QApplication
import PySide6.QtCore

from definitions import ROOT_DIR
from widgets.Author import Author
from widgets.CommonTreeView import CommonTreeView
from widgets.StoriesListView import StoriesListView
from widgets.StoryLink import StoryLink
from widgets.StoryNote import StoryNote
from widgets.StoryTreeView import StoryTreeView
from widgets.Submission import Submission

# Prints PySide6 version
# print(PySide6.__version__)
# Prints the Qt version used to compile PySide6
# print(PySide6.QtCore.__version__)

CONFIG_PATH = os.path.join(ROOT_DIR, 'config.cfg')
gnaw = GnatWriter(CONFIG_PATH)
# app = QApplication(sys.argv)
# window = CommonTreeView(gnaw=gnaw)
# window.show()
# sys.exit(app.exec())

ref = gnaw("bibliography").create_bibliography(
    story_id=2,
    title="Stuff I Said",
    pages="4-7",
    publication_date=datetime.strptime("2024-07-21", '%Y-%m-%d').date(),
    publisher="Rando Hizzy",
    editor="Gary"
)
print(ref.serialize())

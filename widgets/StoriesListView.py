import os
import sys

from PySide6.QtGui import QStandardItem, QStandardItemModel
from PySide6.QtWidgets import QWidget, QListView, QVBoxLayout, QApplication
from gnatwriter import GnatWriter

from definitions import ROOT_DIR, CONFIG_PATH


class StoriesListView(QWidget):
    def __init__(self, gnaw=None):
        super().__init__()

        # self.setGeometry(200, 200, 700, 400)
        self.setWindowTitle('Stories List View')

        self.model = QStandardItemModel()
        self.gnaw = gnaw
        self.setup_model()

        self.list_view = QListView()
        self.list_view.setModel(self.model)
        self.list_view.selectionModel().selectionChanged.connect(self.item_clicked)

        vbox = QVBoxLayout()
        vbox.addWidget(self.list_view)
        self.setLayout(vbox)

    def setup_model(self):
        stories = self.gnaw("story").get_all_stories()

        for story in stories:
            story_item = QStandardItem(story.title)
            story_item.setData(story.id, 11)
            story_item.setData("Story", 12)
            self.model.appendRow(story_item)

    def item_clicked(self, selected, deselected):
        indexes = selected.indexes()

        for index in indexes:
            item = self.model.itemFromIndex(index)
            print(f"{item.data(12)} {item.data(11)} - {item.text()}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    gnaw = GnatWriter(CONFIG_PATH)
    window = StoriesListView(gnaw=gnaw)
    window.show()
    sys.exit(app.exec())

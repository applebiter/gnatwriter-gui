import os
import sys

from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QWidget, QTreeView, QVBoxLayout, QApplication
from gnatwriter import GnatWriter

from definitions import ROOT_DIR, CONFIG_PATH


class StoryTreeView(QWidget):
    def __init__(self, story_id: int, gnaw=None):
        super().__init__()

        # self.setGeometry(200, 200, 700, 400)
        self.setWindowTitle('Story Tree View')
        self.story_id = story_id
        self.model = QStandardItemModel()
        self.gnaw = gnaw
        self.root_item = self.model.invisibleRootItem()
        self.setup_model()

        self.tree_view = QTreeView()
        self.tree_view.setIndentation(16)
        self.tree_view.setUniformRowHeights(True)
        self.tree_view.setModel(self.model)
        self.tree_view.selectionModel().selectionChanged.connect(self.item_clicked)

        vbox = QVBoxLayout()
        vbox.addWidget(self.tree_view)
        self.setLayout(vbox)

    def setup_model(self):
        self.model.setHorizontalHeaderLabels(['Story Tree View'])

        story = self.gnaw("story").get_story_by_id(story_id=self.story_id)
        story_root = QStandardItem(story.title)
        story_root.setData(story.id, 11)
        story_root.setData("Story", 12)

        for chapter in story.chapters:
            chapter_item = QStandardItem(chapter.title)
            chapter_item.setData(chapter.id, 11)
            chapter_item.setData("Chapter", 12)
            story_root.appendRow(chapter_item)

            for scene in chapter.scenes:
                scene_item = QStandardItem(scene.title)
                scene_item.setData(scene.id, 11)
                scene_item.setData("Scene", 12)
                chapter_item.appendRow(scene_item)

        self.root_item.appendRow(story_root)

    def item_clicked(self, selected, deselected):
        indexes = selected.indexes()

        for index in indexes:
            item = self.model.itemFromIndex(index)
            print(f"{item.data(12)} {item.data(11)} - {item.text()}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    gnaw = GnatWriter(CONFIG_PATH)
    window = StoryTreeView(story_id=1, gnaw=gnaw)
    window.show()
    sys.exit(app.exec())

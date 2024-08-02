import os
import sys

from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QTreeView, QVBoxLayout, QApplication, QWidget
from gnatwriter import GnatWriter

from definitions import ROOT_DIR, CONFIG_PATH


class CommonTreeView(QWidget):
    def __init__(self, gnaw=None):
        super().__init__()

        self.setWindowTitle('Tree View')

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
        self.model.setHorizontalHeaderLabels(['Tree View'])

        stories = self.gnaw("story").get_all_stories()
        stories_item = QStandardItem('Stories')
        self.root_item.appendRow(stories_item)

        for story in stories:
            story_item = QStandardItem(story.title)
            story_item.setData(story.id, 11)
            story_item.setData("Story", 12)
            stories_item.appendRow(story_item)

            for chapter in story.chapters:
                chapter_item = QStandardItem(chapter.title)
                chapter_item.setData(chapter.id, 11)
                chapter_item.setData("Chapter", 12)
                story_item.appendRow(chapter_item)

                for scene in chapter.scenes:
                    scene_item = QStandardItem(scene.title)
                    scene_item.setData(scene.id, 11)
                    scene_item.setData("Scene", 12)
                    chapter_item.appendRow(scene_item)

        characters = self.gnaw("character").get_all_characters()
        characters_item = QStandardItem('Characters')
        self.root_item.appendRow(characters_item)

        for character in characters:
            character_item = QStandardItem(character.full_name)
            character_item.setData(character.id, 11)
            character_item.setData("Character", 12)
            characters_item.appendRow(character_item)

        events = self.gnaw("event").get_all_events()
        events_item = QStandardItem('Events')
        self.root_item.appendRow(events_item)

        for event in events:
            event_item = QStandardItem(event.title)
            event_item.setData(event.id, 11)
            event_item.setData("Event", 12)
            events_item.appendRow(event_item)

        locations = self.gnaw("location").get_all_locations()
        locations_item = QStandardItem('Locations')
        self.root_item.appendRow(locations_item)

        for location in locations:
            location_item = QStandardItem(location.title)
            location_item.setData(location.id, 11)
            location_item.setData("Location", 12)
            locations_item.appendRow(location_item)

    def item_clicked(self, selected, deselected):
        indexes = selected.indexes()

        for index in indexes:
            item = self.model.itemFromIndex(index)
            print(f"{item.data(12)} {item.data(11)} - {item.text()}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    gnaw = GnatWriter(CONFIG_PATH)
    window = CommonTreeView(gnaw=gnaw)
    window.show()
    sys.exit(app.exec())

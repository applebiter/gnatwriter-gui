import sys
import webbrowser

from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtWidgets import (QApplication, QGroupBox, QHBoxLayout, QLabel,
                               QLineEdit, QListView, QPushButton,
                               QSizePolicy, QSpacerItem, QVBoxLayout, QAbstractScrollArea, QAbstractItemView, QWidget)
from gnatwriter import GnatWriter
from definitions import CONFIG_PATH


class StoryLink(QWidget):
    def __init__(self, story_id=None, link_id=None, backend=None):
        super().__init__()

        self.setWindowTitle("Story Links Management")

        self.current_story_id = story_id if story_id else None
        self.current_link_id = link_id if link_id else None
        self.gnaw = backend
        self.model = None
        self.selection_model = None

        self.hbx_outermost = QHBoxLayout()
        self.vbx_outermost = QVBoxLayout()

        # The list of links
        self.lst_links = QListView()
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lst_links.sizePolicy().hasHeightForWidth())
        self.lst_links.setSizePolicy(sizePolicy)
        self.lst_links.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.lst_links.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.lst_links.setResizeMode(QListView.ResizeMode.Adjust)
        self.vbx_outermost.addWidget(self.lst_links)

        # The delete button
        self.hbx_delete = QHBoxLayout()
        self.hspacer_delete = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )
        self.hbx_delete.addItem(self.hspacer_delete)
        self.btn_delete = QPushButton("Delete")
        self.btn_delete.clicked.connect(self.delete_link)
        self.hbx_delete.addWidget(self.btn_delete)
        self.vbx_outermost.addLayout(self.hbx_delete)

        # The link's URL
        self.lbl_url = QLabel("URL")
        self.vbx_outermost.addWidget(self.lbl_url)
        self.ldt_url = QLineEdit()
        self.vbx_outermost.addWidget(self.ldt_url)

        # The link's title
        self.lbl_title = QLabel("Title")
        self.vbx_outermost.addWidget(self.lbl_title)
        self.ldt_title = QLineEdit()
        self.vbx_outermost.addWidget(self.ldt_title)

        # The add and clear buttons
        self.hbx_save_clear_open = QHBoxLayout()
        self.hspacer_save = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )
        self.hbx_save_clear_open.addItem(self.hspacer_save)
        self.btn_save = QPushButton("Add")
        self.btn_save.clicked.connect(self.save_link)
        self.hbx_save_clear_open.addWidget(self.btn_save)
        self.btn_clear = QPushButton("Clear")
        self.btn_clear.clicked.connect(self.clear_form)
        self.hbx_save_clear_open.addWidget(self.btn_clear)
        self.btn_open = QPushButton("Open")
        self.btn_open.clicked.connect(self.open_link)
        self.hbx_save_clear_open.addWidget(self.btn_open)
        self.vbx_outermost.addLayout(self.hbx_save_clear_open)

        self.hbx_outermost.addLayout(self.vbx_outermost)
        self.setLayout(self.hbx_outermost)

        self.load_model()
        self.setup_form()
        self.selection_model = self.lst_links.selectionModel()
        self.selection_model.selectionChanged.connect(self.item_selected)

    def open_link(self):
        url = self.ldt_url.text()
        if url:
            webbrowser.open(url)

    def load_model(self):
        self.model = QStandardItemModel()
        self.lst_links.setModel(self.model)
        all_links = self.gnaw("link").get_links_by_story_id(story_id=self.current_story_id)
        for link in all_links:
            link_item = QStandardItem(link.title)
            # Chose 14 to represent the data index holding the identifier
            link_item.setData(link.id, 14)
            self.model.appendRow(link_item)
        self.selection_model = self.lst_links.selectionModel()
        self.selection_model.selectionChanged.connect(self.item_selected)
        self.model.layoutChanged.emit()

    def item_selected(self, item):
        if item.indexes():
            self.current_link_id = item.indexes()[0].data(14)
        else:
            self.current_link_id = None
        self.setup_form()

    def setup_form(self):
        if self.current_link_id:
            link = self.gnaw("link").get_link_by_id(link_id=self.current_link_id)
            if link:
                self.ldt_title.setText(link.title)
                self.ldt_url.setText(link.url)
                self.btn_save.setText("Update")
            else:
                self.clear_form()
        else:
            self.clear_form()

    def clear_form(self):
        self.btn_save.setText("Add")
        self.current_link_id = None
        self.ldt_title.clear()
        self.ldt_url.clear()

    def save_link(self):
        url = self.ldt_url.text()
        title = self.ldt_title.text()
        if not url or not title:
            return
        if self.current_link_id:
            self.gnaw("link").update_link(
                link_id=self.current_link_id, title=title, url=url
            )
            self.setup_form()
        else:
            link = self.gnaw("link").create_link(title=title, url=url)
            if link:
                story = self.gnaw("story").append_links_to_story(
                    story_id=self.current_story_id, link_ids=[link.id]
                )
                del story
                self.current_link_id = link.id
        self.load_model()

    def delete_link(self):
        if self.current_link_id:
            self.gnaw("link").delete_link_by_id(link_id=self.current_link_id)
            self.clear_form()
            self.load_model()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    gnaw = GnatWriter(CONFIG_PATH)
    window = StoryLink(story_id=2, backend=gnaw)
    window.show()
    sys.exit(app.exec())

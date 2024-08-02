import sys
from PySide6.QtCore import (Qt)
from PySide6.QtGui import (QStandardItemModel, QStandardItem)
from PySide6.QtWidgets import (QApplication, QCheckBox, QHBoxLayout, QLabel,
                               QLineEdit, QListView, QPushButton, QSizePolicy,
                               QSpacerItem, QVBoxLayout, QAbstractItemView,
                               QWidget)
from gnatwriter import GnatWriter
from definitions import CONFIG_PATH


class Author(QWidget):
    """ This class is a widget that allows the user to manage authors and their association with stories.
    """
    def __init__(self, story_id=None, author_id=None, gnaw=None):
        super().__init__()

        self.setWindowTitle("Story Authors Management")

        self.current_story_id = story_id if story_id else None
        self.current_author_id = author_id if author_id else None
        self.gnaw = gnaw
        self.selection_model = None

        self.hbx_outermost = QHBoxLayout()
        self.vbx_outermost = QVBoxLayout()

        self.lbl_instructions = QLabel("Checked authors are attached to the current story")
        self.vbx_outermost.addWidget(self.lbl_instructions)

        # The list of authors
        self.lst_authors = QListView()
        size_policy_list = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
        size_policy_list.setHorizontalStretch(0)
        size_policy_list.setVerticalStretch(0)
        size_policy_list.setHeightForWidth(self.lst_authors.sizePolicy().hasHeightForWidth())
        self.lst_authors.setSizePolicy(size_policy_list)
        self.lst_authors.setSizeAdjustPolicy(QListView.SizeAdjustPolicy.AdjustToContents)
        self.lst_authors.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.lst_authors.setResizeMode(QListView.ResizeMode.Adjust)
        self.vbx_outermost.addWidget(self.lst_authors)

        # The delete button
        self.hbx_delete_author = QHBoxLayout()
        self.hspacer_delete_author = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.hbx_delete_author.addItem(self.hspacer_delete_author)
        self.btn_delete_author = QPushButton("Delete")
        self.btn_delete_author.clicked.connect(self.delete_author)
        self.hbx_delete_author.addWidget(self.btn_delete_author)
        self.vbx_outermost.addLayout(self.hbx_delete_author)

        # The author's name and initials
        self.hbx_name_initials = QHBoxLayout()
        self.vbx_name = QVBoxLayout()
        self.lbl_name = QLabel("Name")
        self.vbx_name.addWidget(self.lbl_name)
        self.ldt_name = QLineEdit()
        self.vbx_name.addWidget(self.ldt_name)
        self.hbx_name_initials.addLayout(self.vbx_name)
        self.vbx_initials = QVBoxLayout()
        self.lbl_initials = QLabel("Initials")
        self.vbx_initials.addWidget(self.lbl_initials)
        self.ldt_initials = QLineEdit()
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.ldt_initials.sizePolicy().hasHeightForWidth())
        self.ldt_initials.setSizePolicy(sizePolicy1)
        self.vbx_initials.addWidget(self.ldt_initials)
        self.hbx_name_initials.addLayout(self.vbx_initials)
        self.vbx_outermost.addLayout(self.hbx_name_initials)

        # The pseudonym checkbox
        self.chk_is_pseudonym = QCheckBox("This name is a pseudonym")
        self.vbx_outermost.addWidget(self.chk_is_pseudonym)

        # The append to story checkbox
        self.chk_append_to_story = QCheckBox("Attach this author to the current story")
        self.vbx_outermost.addWidget(self.chk_append_to_story)

        # The add and clear buttons
        self.hbx_add_clear = QHBoxLayout()
        self.hspacer_add_clear = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.hbx_add_clear.addItem(self.hspacer_add_clear)
        self.btn_save = QPushButton("Add")
        self.btn_save.clicked.connect(self.save_author)
        self.hbx_add_clear.addWidget(self.btn_save)
        self.btn_clear = QPushButton("Clear")
        self.btn_clear.clicked.connect(self.clear_form)
        self.hbx_add_clear.addWidget(self.btn_clear)
        self.vbx_outermost.addLayout(self.hbx_add_clear)

        self.hbx_outermost.addLayout(self.vbx_outermost)
        self.setLayout(self.hbx_outermost)

        self.model = QStandardItemModel()
        self.load_model()
        self.setup_form()
        self.selection_model = self.lst_authors.selectionModel()
        self.selection_model.selectionChanged.connect(self.item_selected)

    def load_model(self):
        self.model = QStandardItemModel()
        self.lst_authors.setModel(self.model)
        all_authors = self.gnaw("author").get_all_authors()
        for author in all_authors:
            author_item = QStandardItem(author.name)
            # Chose 14 to represent the data index holding the identifier
            author_item.setData(author.id, 14)  # The integers 1-13 are reserved for other data
            author_item.setCheckable(False)
            author_item.setCheckState(Qt.CheckState.Unchecked)
            if self.current_story_id:
                for author_story in author.stories:
                    if author_story.story_id == self.current_story_id:
                        author_item.setCheckState(Qt.CheckState.Checked)
                    else:
                        author_item.setCheckState(Qt.CheckState.Unchecked)
            self.model.appendRow(author_item)
        self.selection_model = self.lst_authors.selectionModel()
        self.selection_model.selectionChanged.connect(self.item_selected)
        self.model.layoutChanged.emit()

    def item_selected(self, item):
        if item.indexes():
            self.current_author_id = item.indexes()[0].data(14)
        else:
            self.current_author_id = None
        self.setup_form()

    def setup_form(self):
        if self.current_author_id:
            author = self.gnaw("author").get_author_by_id(self.current_author_id)
            if author:
                self.ldt_name.setText(author.name)
                self.ldt_initials.setText(author.initials)
                self.chk_is_pseudonym.setChecked(author.is_pseudonym)
                self.chk_append_to_story.setChecked(False)
                if len(author.stories) > 0:
                    for author_story in author.stories:
                        if author_story.story_id == self.current_story_id:
                            self.chk_append_to_story.setChecked(True)
                            break
                self.btn_save.setText("Update")
            else:
                self.ldt_name.clear()
                self.ldt_initials.clear()
                self.chk_is_pseudonym.setChecked(False)
                self.chk_append_to_story.setChecked(False)
                self.btn_save.setText("Add")
        else:
            self.ldt_name.clear()
            self.ldt_initials.clear()
            self.chk_is_pseudonym.setChecked(False)
            self.chk_append_to_story.setChecked(False)
            self.btn_save.setText("Add")

    def clear_form(self):
        self.current_author_id = None
        self.selection_model.clearSelection()
        self.setup_form()

    def save_author(self):
        name = self.ldt_name.text()
        initials = self.ldt_initials.text()
        is_pseudonym = self.chk_is_pseudonym.isChecked()
        append_to_story = self.chk_append_to_story.isChecked()
        if self.current_story_id:
            if self.current_author_id:
                self.gnaw("author").update_author(
                    author_id=self.current_author_id,
                    name=name,
                    initials=initials,
                    is_pseudonym=is_pseudonym
                )
            else:
                author = self.gnaw("author").create_author(
                    name=name,
                    initials=initials,
                    is_pseudonym=is_pseudonym
                )
                if author:
                    self.current_author_id = author.id
            if self.current_author_id:
                if append_to_story:
                    self.gnaw("story").append_authors_to_story(
                        story_id=self.current_story_id,
                        author_ids=[self.current_author_id]
                    )
                else:
                    self.gnaw("story").detach_authors_from_story(
                        story_id=self.current_story_id,
                        author_ids=[self.current_author_id]
                    )

        self.clear_form()
        self.load_model()

    def delete_author(self):
        if self.current_author_id:
            self.gnaw("author").delete_author_by_id(self.current_author_id)
            self.current_author_id = None
            self.clear_form()
            self.load_model()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    gnaw = GnatWriter(CONFIG_PATH)
    window = Author(story_id=2, gnaw=gnaw)
    window.show()
    sys.exit(app.exec())

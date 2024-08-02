import os
import sys
from PySide6.QtCore import (QCoreApplication, QMetaObject)
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtWidgets import (QComboBox, QGroupBox, QHBoxLayout,
                               QLineEdit, QPlainTextEdit, QPushButton, QSizePolicy,
                               QSpacerItem, QVBoxLayout, QWidget, QApplication, QLabel, QListView, QAbstractScrollArea,
                               QAbstractItemView)
from gnatwriter import GnatWriter
from definitions import ROOT_DIR, CONFIG_PATH


class StoryNote(QWidget):
    def __init__(self, story_id=None, note_id=None, backend=None):
        super().__init__()

        self.setWindowTitle("Story Notes Management")

        self.current_story_id = story_id if story_id else None
        self.current_note_id = note_id if note_id else None
        self.gnaw = backend
        self.model = None
        self.selection_model = None

        self.hbx_outermost = QHBoxLayout()
        self.vbx_outermost = QVBoxLayout()

        # The list of notes
        self.lst_notes = QListView()
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lst_notes.sizePolicy().hasHeightForWidth())
        self.lst_notes.setSizePolicy(sizePolicy)
        self.lst_notes.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.lst_notes.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.lst_notes.setResizeMode(QListView.ResizeMode.Adjust)
        self.vbx_outermost.addWidget(self.lst_notes)

        # The delete button
        self.hbx_delete_note = QHBoxLayout()
        self.hspacer_delete = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.hbx_delete_note.addItem(self.hspacer_delete)
        self.btn_delete = QPushButton("Delete")
        self.btn_delete.clicked.connect(self.delete_note)
        self.hbx_delete_note.addWidget(self.btn_delete)
        self.vbx_outermost.addLayout(self.hbx_delete_note)

        # The note's title
        self.lbl_title = QLabel("Title")
        self.vbx_outermost.addWidget(self.lbl_title)
        self.ldt_title = QLineEdit()
        self.vbx_outermost.addWidget(self.ldt_title)

        # The note's content
        self.lbl_content = QLabel("Content")
        self.vbx_outermost.addWidget(self.lbl_content)
        self.ptt_content = QPlainTextEdit()
        self.vbx_outermost.addWidget(self.ptt_content)

        # The add and clear buttons
        self.hbx_buttons = QHBoxLayout()
        self.hspacer_add = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.hbx_buttons.addItem(self.hspacer_add)
        self.btn_save = QPushButton("Add")
        self.btn_save.clicked.connect(self.save_note)
        self.hbx_buttons.addWidget(self.btn_save)
        self.btn_clear = QPushButton("Clear")
        self.btn_clear.clicked.connect(self.clear_form)
        self.hbx_buttons.addWidget(self.btn_clear)
        self.vbx_outermost.addLayout(self.hbx_buttons)

        self.hbx_outermost.addLayout(self.vbx_outermost)
        self.setLayout(self.hbx_outermost)

        self.load_model()
        self.setup_form()
        self.selection_model = self.lst_notes.selectionModel()
        self.selection_model.selectionChanged.connect(self.item_selected)

    def load_model(self):
        self.model = QStandardItemModel()
        self.lst_notes.setModel(self.model)
        all_notes = self.gnaw("note").get_notes_by_story_id(story_id=self.current_story_id)
        for note in all_notes:
            note_item = QStandardItem(note.title)
            # Chose 14 to represent the data index holding the identifier
            note_item.setData(note.id, 14)
            self.model.appendRow(note_item)
        self.selection_model = self.lst_notes.selectionModel()
        self.selection_model.selectionChanged.connect(self.item_selected)
        self.model.layoutChanged.emit()

    def item_selected(self, item):
        if item.indexes():
            self.current_note_id = item.indexes()[0].data(14)
        else:
            self.current_note_id = None
        self.setup_form()

    def setup_form(self):
        if self.current_note_id:
            note = self.gnaw("note").get_note_by_id(note_id=self.current_note_id)
            if note:
                self.ldt_title.setText(note.title)
                self.ptt_content.setPlainText(note.content)
                self.btn_save.setText("Update")
            else:
                self.clear_form()
        else:
            self.clear_form()

    def clear_form(self):
        self.btn_save.setText("Add")
        self.current_note_id = None
        self.ldt_title.clear()
        self.ptt_content.clear()

    def save_note(self):
        content = self.ptt_content.toPlainText()
        title = self.ldt_title.text()
        if not content or not title:
            return
        if self.current_note_id:
            self.gnaw("note").update_note(
                note_id=self.current_note_id, title=title, content=content
            )
            self.setup_form()
        else:
            note = self.gnaw("note").create_note(title=title, content=content)
            if note:
                story = self.gnaw("story").append_notes_to_story(
                    story_id=self.current_story_id, note_ids=[note.id]
                )
                del story
                self.current_note_id = note.id
        self.load_model()

    def delete_note(self):
        if self.current_note_id:
            self.gnaw("note").delete_note_by_id(note_id=self.current_note_id)
            self.clear_form()
            self.load_model()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    gnaw = GnatWriter(CONFIG_PATH)
    window = StoryNote(story_id=2, backend=gnaw)
    window.show()
    sys.exit(app.exec())

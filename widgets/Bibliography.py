import sys
from datetime import datetime
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
                            QMetaObject, QSize, Qt)
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateEdit,
                               QGroupBox, QHBoxLayout, QLabel, QLineEdit,
                               QListView, QPlainTextEdit, QPushButton, QSizePolicy,
                               QSpacerItem, QVBoxLayout, QWidget, QAbstractScrollArea, QAbstractItemView)
from gnatwriter import GnatWriter
from definitions import CONFIG_PATH


class Bibliography(QWidget):
    def __init__(self, story_id=None, bibliography_id=None, backend=None):
        super().__init__()

        self.setWindowTitle("Story Bibliography Management")

        self.current_story_id = story_id if story_id else None
        self.current_bibliography_id = bibliography_id if bibliography_id else None
        self.gnaw = backend
        self.model = None
        self.selection_model = None

        self.year = datetime.now().year
        self.month = datetime.now().month
        self.day = datetime.now().day
        self.today = QDate()
        self.today.setDate(self.year, self.month, self.day)

        self.hbx_outermost = QHBoxLayout()
        self.vbx_outermost = QVBoxLayout()

        # The list of bibliography references
        self.lst_bibliographies = QListView()
        list_size = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
        list_size.setHorizontalStretch(0)
        list_size.setVerticalStretch(0)
        list_size.setHeightForWidth(self.lst_bibliographies.sizePolicy().hasHeightForWidth())
        self.lst_bibliographies.setSizePolicy(list_size)
        self.lst_bibliographies.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.lst_bibliographies.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.lst_bibliographies.setResizeMode(QListView.ResizeMode.Adjust)
        self.vbx_outermost.addWidget(self.lst_bibliographies)

        # The delete button
        self.hbx_delete = QHBoxLayout()
        self.hspacer_delete = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.hbx_delete.addItem(self.hspacer_delete)
        self.btn_delete = QPushButton("Delete")
        self.btn_delete.clicked.connect(self.delete_reference)
        self.hbx_delete.addWidget(self.btn_delete)
        self.vbx_outermost.addLayout(self.hbx_delete)

        # The title of the reference
        self.lbl_title = QLabel("Title of Reference")
        self.vbx_outermost.addWidget(self.lbl_title)
        self.ldt_title = QLineEdit()
        self.vbx_outermost.addWidget(self.ldt_title)

        # The pages referenced
        self.hbx_pages_pubdate = QHBoxLayout()
        self.vbx_pages = QVBoxLayout()
        self.lbl_pages = QLabel("Referenced Page(s)")
        self.vbx_pages.addWidget(self.lbl_pages)
        self.ldt_pages = QLineEdit()
        self.vbx_pages.addWidget(self.ldt_pages)
        self.hbx_pages_pubdate.addLayout(self.vbx_pages)

        # The publication date
        self.vbx_publication_date = QVBoxLayout()
        self.lbl_publication_date = QLabel("Publication Date")
        self.vbx_publication_date.addWidget(self.lbl_publication_date)
        self.hbx_publication_date = QHBoxLayout()
        self.ddt_publication_date = QDateEdit()
        self.ddt_publication_date = QDateEdit(self.today)
        self.ddt_publication_date.setEnabled(False)
        self.ddt_publication_date.setDisplayFormat('MMMM d, yyyy')
        self.hbx_publication_date.addWidget(self.ddt_publication_date)
        self.chk_enable_date = QCheckBox("enable")
        self.chk_enable_date.setCheckState(Qt.CheckState.Unchecked)
        self.chk_enable_date.toggled.connect(self.ddt_publication_date.setEnabled)
        self.hbx_publication_date.addWidget(self.chk_enable_date)
        self.vbx_publication_date.addLayout(self.hbx_publication_date)
        self.hbx_pages_pubdate.addLayout(self.vbx_publication_date)
        self.vbx_outermost.addLayout(self.hbx_pages_pubdate)

        # The publisher and editor
        self.hbx_publisher_editor = QHBoxLayout()
        self.vbx_publisher = QVBoxLayout()
        self.lbl_publisher = QLabel("Publisher")
        self.vbx_publisher.addWidget(self.lbl_publisher)
        self.ldt_publisher = QLineEdit()
        self.vbx_publisher.addWidget(self.ldt_publisher)
        self.hbx_publisher_editor.addLayout(self.vbx_publisher)
        self.vbx_editor = QVBoxLayout()
        self.lbl_editor = QLabel("Editor")
        self.vbx_editor.addWidget(self.lbl_editor)
        self.ldt_editor = QLineEdit()
        self.vbx_editor.addWidget(self.ldt_editor)
        self.hbx_publisher_editor.addLayout(self.vbx_editor)
        self.vbx_outermost.addLayout(self.hbx_publisher_editor)

        # The authors dropdown box
        self.lbl_authors = QLabel("Author(s)")
        self.vbx_outermost.addWidget(self.lbl_authors)
        self.hbx_authors_combobox = QHBoxLayout()
        self.cbx_authors = QComboBox()
        self.cbx_authors.setEnabled(False)
        self.hbx_authors_combobox.addWidget(self.cbx_authors)
        self.btn_remove_author = QPushButton("Remove Author")
        self.btn_remove_author.clicked.connect(self.remove_author)
        self.btn_remove_author.setEnabled(False)
        self.hbx_authors_combobox.addWidget(self.btn_remove_author)
        self.vbx_outermost.addLayout(self.hbx_authors_combobox)

        # A form for adding an author
        self.gbx_authors = QGroupBox()
        self.hbx_authors = QHBoxLayout()
        self.vbx_name = QVBoxLayout()

        # The author's name
        self.lbl_name = QLabel("Name")
        self.vbx_name.addWidget(self.lbl_name)
        self.ldt_name = QLineEdit()
        self.vbx_name.addWidget(self.ldt_name)
        self.hbx_authors.addLayout(self.vbx_name)
        self.vbx_initials = QVBoxLayout()

        # The author's initials
        self.lbl_initials = QLabel("Initials")
        self.vbx_initials.addWidget(self.lbl_initials)
        self.ldt_initials = QLineEdit()
        initials_size = QSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Fixed)
        initials_size.setHorizontalStretch(0)
        initials_size.setVerticalStretch(0)
        initials_size.setHeightForWidth(self.ldt_initials.sizePolicy().hasHeightForWidth())
        self.ldt_initials.setSizePolicy(initials_size)
        self.vbx_initials.addWidget(self.ldt_initials)
        self.hbx_authors.addLayout(self.vbx_initials)

        # The add author button
        self.vbx_add = QVBoxLayout()
        self.lbl_add = QLabel("")
        self.vbx_add.addWidget(self.lbl_add)
        self.btn_add = QPushButton("Add Author")
        self.btn_add.clicked.connect(self.add_author)
        self.vbx_add.addWidget(self.btn_add)
        self.hbx_authors.addLayout(self.vbx_add)
        self.gbx_authors.setLayout(self.hbx_authors)
        self.gbx_authors.setEnabled(False)
        self.vbx_outermost.addWidget(self.gbx_authors)

        # The add and clear buttons
        self.hbx_add_clear = QHBoxLayout()
        self.hbx_add_clear.setObjectName(u"hbx_add_clear")
        self.hspacer_add_clear = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.hbx_add_clear.addItem(self.hspacer_add_clear)
        self.btn_save = QPushButton("Add")
        self.btn_save.clicked.connect(self.save_reference)
        self.hbx_add_clear.addWidget(self.btn_save)
        self.btn_clear = QPushButton("Clear")
        self.btn_clear.clicked.connect(self.clear_reference_form)
        self.hbx_add_clear.addWidget(self.btn_clear)
        self.vbx_outermost.addLayout(self.hbx_add_clear)

        self.hbx_outermost.addLayout(self.vbx_outermost)
        self.setLayout(self.hbx_outermost)

        self.load_model()
        self.setup_form()

    def load_model(self):
        self.model = QStandardItemModel()
        self.lst_bibliographies.setModel(self.model)
        all_references = self.gnaw("bibliography").get_bibliographies_by_story_id(
            story_id=self.current_story_id
        )
        if all_references:
            for reference in all_references:
                reference_item = QStandardItem(reference.title)
                # Chose 14 to represent the data index holding the identifier
                reference_item.setData(reference.id, 14)
                self.model.appendRow(reference_item)
        self.selection_model = self.lst_bibliographies.selectionModel()
        self.selection_model.selectionChanged.connect(self.reference_selected)
        self.model.layoutChanged.emit()

    def reference_selected(self, item):
        if item.indexes():
            self.current_bibliography_id = item.indexes()[0].data(14)
        else:
            self.current_bibliography_id = None
        self.setup_form()

    def setup_form(self):
        if self.current_bibliography_id:
            reference = self.gnaw("bibliography").get_bibliography_by_id(
                bibliography_id=self.current_bibliography_id
            )
            if reference:
                self.ldt_title.setText(reference.title)
                self.ldt_pages.setText(reference.pages)
                if reference.publication_date:
                    self.ddt_publication_date.setDate(
                        QDate.fromString(str(reference.publication_date), "yyyy-MM-dd")
                    )
                    self.chk_enable_date.setChecked(True)
                self.ldt_publisher.setText(reference.publisher)
                self.ldt_editor.setText(reference.editor)
                self.cbx_authors.clear()
                # need to enable the author form
                self.gbx_authors.setEnabled(True)
                authors = self.gnaw("bibliography").get_bibliography_authors(
                    bibliography_id=self.current_bibliography_id
                )
                if authors:
                    self.cbx_authors.setEnabled(True)
                    for author in authors:
                        self.cbx_authors.addItem(author.name, author.id)
                    self.btn_remove_author.setEnabled(True)
                else:
                    self.cbx_authors.setEnabled(False)
                    self.btn_remove_author.setEnabled(False)
            else:
                self.clear_reference_form()

    def clear_reference_form(self):
        self.ldt_title.clear()
        self.ldt_pages.clear()
        self.ddt_publication_date.setDate(self.today)
        self.chk_enable_date.setChecked(False)
        self.ldt_publisher.clear()
        self.ldt_editor.clear()
        self.cbx_authors.clear()
        self.cbx_authors.setEnabled(False)
        self.btn_remove_author.setEnabled(False)
        self.ldt_name.clear()
        self.ldt_initials.clear()
        self.gbx_authors.setEnabled(False)
        self.btn_add.setEnabled(False)
        self.current_bibliography_id = None
        self.btn_save.setText("Add")

    def save_reference(self):
        if self.current_story_id:
            title = self.ldt_title.text() if self.ldt_title.text() else None
            pages = self.ldt_pages.text() if self.ldt_pages.text() else None
            if self.chk_enable_date.isChecked():
                publication_date = self.ddt_publication_date.date().toPython()
            else:
                publication_date = None
            publisher = self.ldt_publisher.text() if self.ldt_publisher.text() else None
            editor = self.ldt_editor.text() if self.ldt_editor.text() else None

            if self.current_bibliography_id:
                self.gnaw("bibliography").update_bibliography(
                    bibliography_id=self.current_bibliography_id,
                    story_id=self.current_story_id,
                    title=title,
                    pages=pages,
                    publication_date=publication_date,
                    publisher=publisher,
                    editor=editor
                )
            else:
                ref = self.gnaw("bibliography").create_bibliography(
                    story_id=self.current_story_id,
                    title=title,
                    pages=pages,
                    publication_date=publication_date,
                    publisher=publisher,
                    editor=editor
                )
                self.current_bibliography_id = ref.id

            self.load_model()
            self.clear_reference_form()

    def delete_reference(self):
        if self.current_bibliography_id:
            self.gnaw("bibliography").delete_bibliography(
                bibliography_id=self.current_bibliography_id
            )
            self.clear_reference_form()
            self.load_model()

    def add_author(self):
        if self.current_bibliography_id:
            name = self.ldt_name.text() if self.ldt_name.text() else None
            initials = self.ldt_initials.text() if self.ldt_initials.text() else None
            author = self.gnaw("bibliography").add_author(
                bibliography_id=self.current_bibliography_id,
                name=name,
                initials=initials
            )
            if author:
                self.ldt_name.clear()
                self.ldt_initials.clear()
                self.load_model()
                self.setup_form()

    def remove_author(self):
        if self.current_bibliography_id:
            author_id = self.cbx_authors.currentData()
            self.gnaw("bibliography").remove_author(author_id=author_id)
            self.load_model()
            self.setup_form()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    gnaw = GnatWriter(CONFIG_PATH)
    window = Bibliography(story_id=2, backend=gnaw)
    window.show()
    sys.exit(app.exec())

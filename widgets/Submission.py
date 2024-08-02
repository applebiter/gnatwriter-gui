import sys
from datetime import datetime
from PySide6.QtCore import QDate, Qt
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtWidgets import (QHBoxLayout, QVBoxLayout, QListView, QSpacerItem,
                               QSizePolicy, QPushButton, QApplication,
                               QAbstractScrollArea, QAbstractItemView, QLabel,
                               QLineEdit, QDateEdit, QCheckBox, QComboBox,
                               QWidget)
from gnatwriter import GnatWriter
from definitions import CONFIG_PATH


class Submission(QWidget):

    def __init__(self, story_id=None, submission_id=None, backend=None):
        super().__init__()

        self.setWindowTitle("Story Submissions Management")

        self.current_story_id = story_id if story_id else None
        self.current_submission_id = submission_id if submission_id else None
        self.gnaw = backend
        self.model = None

        self.year = datetime.now().year
        self.month = datetime.now().month
        self.day = datetime.now().day
        self.today = QDate()
        self.today.setDate(self.year, self.month, self.day)

        self.hbx_outermost = QHBoxLayout()
        self.vbx_outermost = QVBoxLayout()

        # The list of submissions
        self.lst_submissions = QListView()
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lst_submissions.sizePolicy().hasHeightForWidth())
        self.lst_submissions.setSizePolicy(sizePolicy)
        self.lst_submissions.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.lst_submissions.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.lst_submissions.setResizeMode(QListView.ResizeMode.Adjust)
        self.vbx_outermost.addWidget(self.lst_submissions)

        # The delete button
        self.hbx_delete_submission = QHBoxLayout()
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.hbx_delete_submission.addItem(self.horizontalSpacer)
        self.btn_delete = QPushButton("Delete")
        self.btn_delete.clicked.connect(self.delete_submission)
        self.hbx_delete_submission.addWidget(self.btn_delete)
        self.vbx_outermost.addLayout(self.hbx_delete_submission)

        # The submission's recipient; the publisher
        self.lbl_submitted_to = QLabel("Submitted To")
        self.vbx_outermost.addWidget(self.lbl_submitted_to)
        self.ldt_submitted_to = QLineEdit()
        self.vbx_outermost.addWidget(self.ldt_submitted_to)

        # The date the story was submitted
        self.date_sent = None
        self.date_sent_enabled = False
        self.hbx_date_sent = QHBoxLayout()
        self.lbl_date_sent = QLabel("Date Sent")
        self.hbx_date_sent.addWidget(self.lbl_date_sent)
        self.hsr_date_sent = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.hbx_date_sent.addItem(self.hsr_date_sent)
        self.chk_enable_date_sent = QCheckBox("enable")
        self.chk_enable_date_sent.setCheckState(Qt.CheckState.Unchecked)
        self.chk_enable_date_sent.toggled.connect(self.toggle_enable_date_sent)
        self.hbx_date_sent.addWidget(self.chk_enable_date_sent)
        self.vbx_outermost.addLayout(self.hbx_date_sent)
        self.ddt_date_sent = QDateEdit(self.today)
        self.ddt_date_sent.setEnabled(False)
        self.ddt_date_sent.setDisplayFormat('MMMM d, yyyy')
        self.vbx_outermost.addWidget(self.ddt_date_sent)

        # The date a reply was received
        self.date_reply_received = None
        self.date_reply_received_enabled = False
        self.hbx_date_reply_received = QHBoxLayout()
        self.lbl_date_reply_received = QLabel("Date of Reply")
        self.hbx_date_reply_received.addWidget(self.lbl_date_reply_received)
        self.hsr_date_reply_received = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.hbx_date_reply_received.addItem(self.hsr_date_reply_received)
        self.chk_enable_date_reply_received = QCheckBox("enable")
        self.chk_enable_date_reply_received.setCheckState(Qt.CheckState.Unchecked)
        self.chk_enable_date_reply_received.toggled.connect(self.toggle_enable_date_reply_received)
        self.hbx_date_reply_received.addWidget(self.chk_enable_date_reply_received)
        self.vbx_outermost.addLayout(self.hbx_date_reply_received)
        self.ddt_date_reply_received = QDateEdit(self.today)
        self.ddt_date_reply_received.setEnabled(False)
        self.ddt_date_reply_received.setDisplayFormat('MMMM d, yyyy')
        self.vbx_outermost.addWidget(self.ddt_date_reply_received)

        # The date of publication
        self.date_published = None
        self.date_published_enabled = False
        self.hbx_date_published = QHBoxLayout()
        self.lbl_date_published = QLabel("Date Published")
        self.hbx_date_published.addWidget(self.lbl_date_published)
        self.hsr_date_published = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.hbx_date_published.addItem(self.hsr_date_published)
        self.chk_enable_date_published = QCheckBox("enable")
        self.chk_enable_date_published.setCheckState(Qt.CheckState.Unchecked)
        self.chk_enable_date_published.toggled.connect(self.toggle_enable_date_published)
        self.hbx_date_published.addWidget(self.chk_enable_date_published)
        self.vbx_outermost.addLayout(self.hbx_date_published)

        self.ddt_date_published = QDateEdit(self.today)
        self.ddt_date_published.setEnabled(False)
        self.ddt_date_published.setDisplayFormat('MMMM d, yyyy')
        self.vbx_outermost.addWidget(self.ddt_date_published)

        # The date of payment received
        self.date_paid = None
        self.date_paid_enabled = False
        self.hbx_date_paid = QHBoxLayout()
        self.lbl_date_paid = QLabel("Date Paid")
        self.hbx_date_paid.addWidget(self.lbl_date_paid)
        self.hsr_date_paid = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.hbx_date_paid.addItem(self.hsr_date_paid)
        self.chk_enable_date_paid = QCheckBox("enable")
        self.chk_enable_date_paid.setCheckState(Qt.CheckState.Unchecked)
        self.chk_enable_date_paid.toggled.connect(self.toggle_enable_date_paid)
        self.hbx_date_paid.addWidget(self.chk_enable_date_paid)
        self.vbx_outermost.addLayout(self.hbx_date_paid)
        self.ddt_date_paid = QDateEdit(self.today)
        self.ddt_date_paid.setEnabled(False)
        self.ddt_date_paid.setDisplayFormat('MMMM d, yyyy')
        self.vbx_outermost.addWidget(self.ddt_date_paid)

        # The status of the submission
        self.hbx_result = QHBoxLayout()
        self.vbx_result = QVBoxLayout()
        self.lbl_result = QLabel("Result")
        self.vbx_result.addWidget(self.lbl_result)
        self.cbx_result = QComboBox()
        self.cbx_result.addItem("Pending")
        self.cbx_result.addItem("Rewrite Requested")
        self.cbx_result.addItem("Ignored")
        self.cbx_result.addItem("Withdrawn")
        self.cbx_result.addItem("Rejected")
        self.cbx_result.addItem("Accepted")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.cbx_result.sizePolicy().hasHeightForWidth())
        self.cbx_result.setSizePolicy(sizePolicy1)
        self.vbx_result.addWidget(self.cbx_result)
        self.hbx_result.addLayout(self.vbx_result)

        # The amount paid for the story
        self.vbx_amount = QVBoxLayout()
        self.lbl_amount = QLabel("Amount Paid")
        self.vbx_amount.addWidget(self.lbl_amount)
        self.ldt_amount = QLineEdit()
        self.vbx_amount.addWidget(self.ldt_amount)
        self.hbx_result.addLayout(self.vbx_amount)
        self.vbx_outermost.addLayout(self.hbx_result)

        # The add and clear buttons
        self.hbx_add_clear = QHBoxLayout()
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.hbx_add_clear.addItem(self.horizontalSpacer_2)
        self.btn_save = QPushButton("Add")
        self.btn_save.clicked.connect(self.save_submission)
        self.hbx_add_clear.addWidget(self.btn_save)
        self.btn_clear = QPushButton("Clear")
        self.btn_clear.clicked.connect(self.clear_form)
        self.hbx_add_clear.addWidget(self.btn_clear)
        self.vbx_outermost.addLayout(self.hbx_add_clear)

        self.hbx_outermost.addLayout(self.vbx_outermost)
        self.setLayout(self.hbx_outermost)

        self.load_model()
        self.setup_form()
        self.selection_model = self.lst_submissions.selectionModel()
        self.selection_model.selectionChanged.connect(self.item_selected)

    def load_model(self):
        self.model = QStandardItemModel()
        self.lst_submissions.setModel(self.model)
        all_submissions = self.gnaw("submission").get_all_submissions()
        for submission in all_submissions:
            submission_item = QStandardItem(submission.submitted_to)
            # Chose 14 to represent the data index holding the identifier
            submission_item.setData(submission.id, 14)
            self.model.appendRow(submission_item)
        self.selection_model = self.lst_submissions.selectionModel()
        self.selection_model.selectionChanged.connect(self.item_selected)
        self.model.layoutChanged.emit()

    def item_selected(self, item):
        if item.indexes():
            self.current_submission_id = item.indexes()[0].data(14)
        else:
            self.current_submission_id = None
        self.setup_form()

    def setup_form(self):
        if self.current_submission_id:
            submission = self.gnaw("submission").get_submission_by_id(self.current_submission_id)
            if submission:
                self.ldt_submitted_to.setText(submission.submitted_to)
                if submission.date_sent:
                    self.date_sent = submission.date_sent
                    self.ddt_date_sent.setDate(QDate.fromString(str(submission.date_sent), 'yyyy-MM-dd'))
                    self.ddt_date_sent.setEnabled(True)
                    self.chk_enable_date_sent.setChecked(True)
                else:
                    self.date_sent = None
                    self.ddt_date_sent.setEnabled(False)
                    self.chk_enable_date_sent.setChecked(False)
                if submission.date_reply_received:
                    self.date_reply_received = submission.date_reply_received
                    self.ddt_date_reply_received.setDate(QDate.fromString(str(submission.date_reply_received), 'yyyy-MM-dd'))
                    self.ddt_date_reply_received.setEnabled(True)
                    self.chk_enable_date_reply_received.setChecked(True)
                else:
                    self.date_reply_received = None
                    self.ddt_date_reply_received.setEnabled(False)
                    self.chk_enable_date_reply_received.setChecked(False)
                if submission.date_published:
                    self.date_published = submission.date_published
                    self.ddt_date_published.setDate(QDate.fromString(str(submission.date_published), 'yyyy-MM-dd'))
                    self.ddt_date_published.setEnabled(True)
                    self.chk_enable_date_published.setChecked(True)
                else:
                    self.date_published = None
                    self.ddt_date_published.setEnabled(False)
                    self.chk_enable_date_published.setChecked(False)
                if submission.date_paid:
                    self.date_paid = submission.date_paid
                    self.ddt_date_paid.setDate(QDate.fromString(str(submission.date_paid), 'yyyy-MM-dd'))
                    self.ddt_date_paid.setEnabled(True)
                    self.chk_enable_date_paid.setChecked(True)
                else:
                    self.date_paid = None
                    self.ddt_date_paid.setEnabled(False)
                    self.chk_enable_date_paid.setChecked(False)
                self.cbx_result.setCurrentIndex(self.cbx_result.findText(submission.result))
                self.ldt_amount.setText(str(submission.amount) if submission.amount else "")
                self.btn_save.setText("Update")
            else:
                self.clear_form()
        else:
            self.clear_form()

    def toggle_enable_date_sent(self):
        if self.chk_enable_date_sent.isChecked():
            self.date_sent_enabled = True
            self.ddt_date_sent.setEnabled(True)
        else:
            self.date_sent_enabled = False
            self.ddt_date_sent.setEnabled(False)
            self.ddt_date_sent.setDate(self.today)

    def toggle_enable_date_reply_received(self):
        if self.chk_enable_date_reply_received.isChecked():
            self.date_reply_received_enabled = True
            self.ddt_date_reply_received.setEnabled(True)
        else:
            self.date_reply_received_enabled = False
            self.ddt_date_reply_received.setEnabled(False)
            self.ddt_date_reply_received.setDate(self.today)

    def toggle_enable_date_published(self):
        if self.chk_enable_date_published.isChecked():
            self.date_published_enabled = True
            self.ddt_date_published.setEnabled(True)
        else:
            self.date_published_enabled = False
            self.ddt_date_published.setEnabled(False)
            self.ddt_date_published.setDate(self.today)

    def toggle_enable_date_paid(self):
        if self.chk_enable_date_paid.isChecked():
            self.date_paid_enabled = True
            self.ddt_date_paid.setEnabled(True)
        else:
            self.date_paid_enabled = False
            self.ddt_date_paid.setEnabled(False)
            self.ddt_date_paid.setDate(self.today)

    def clear_form(self):
        self.current_submission_id = None
        self.selection_model.clearSelection()
        self.ldt_submitted_to.clear()
        self.ddt_date_sent.setDate(self.today)
        self.ddt_date_sent.setEnabled(False)
        self.chk_enable_date_sent.setChecked(False)
        self.ddt_date_reply_received.setDate(self.today)
        self.ddt_date_reply_received.setEnabled(False)
        self.chk_enable_date_reply_received.setChecked(False)
        self.ddt_date_published.setDate(self.today)
        self.ddt_date_published.setEnabled(False)
        self.chk_enable_date_published.setChecked(False)
        self.ddt_date_paid.setDate(self.today)
        self.ddt_date_paid.setEnabled(False)
        self.chk_enable_date_paid.setChecked(False)
        self.cbx_result.setCurrentIndex(0)
        self.ldt_amount.clear()
        self.btn_save.setText("Add")

    def save_submission(self):
        submitted_to = self.ldt_submitted_to.text()
        if not submitted_to:
            return
        date_sent = self.ddt_date_sent.date().toString('yyyy-MM-dd') if self.date_sent_enabled else None
        date_reply_received = self.ddt_date_reply_received.date().toString('yyyy-MM-dd') if self.date_reply_received_enabled else None
        date_published = self.ddt_date_published.date().toString('yyyy-MM-dd') if self.date_published_enabled else None
        date_paid = self.ddt_date_paid.date().toString('yyyy-MM-dd') if self.date_paid_enabled else None
        result = self.cbx_result.currentText()
        amount = float(self.ldt_amount.text()) if self.ldt_amount.text() else None
        if self.current_submission_id:
            self.gnaw("submission").update_submission(
                submission_id=self.current_submission_id,
                submitted_to=submitted_to,
                date_sent=date_sent,
                date_reply_received=date_reply_received,
                date_published=date_published,
                date_paid=date_paid,
                result=result,
                amount=amount
            )
            self.setup_form()
        else:
            submission = self.gnaw("submission").create_submission(
                story_id=self.current_story_id,
                submitted_to=submitted_to,
                date_sent=date_sent,
                date_reply_received=date_reply_received,
                date_published=date_published,
                date_paid=date_paid,
                result=result,
                amount=amount
            )
            if submission:
                self.current_submission_id = submission.id
        self.load_model()

    def delete_submission(self):
        if self.current_submission_id:
            self.gnaw("submission").delete_submission_by_id(self.current_submission_id)
            self.current_submission_id = None
            self.clear_form()
            self.load_model()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    gnaw = GnatWriter(CONFIG_PATH)
    window = Submission(story_id=2, backend=gnaw)
    window.show()
    sys.exit(app.exec())

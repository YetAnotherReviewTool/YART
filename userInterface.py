import os

from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QStackedWidget,
    QVBoxLayout,
    QPushButton,
    QLineEdit,
    QLabel,
    QMessageBox,
    QFormLayout,
    QComboBox,
    QDialog,
    QTextEdit,
    QHBoxLayout,
    QCheckBox,
    QFileDialog
)

from PyQt5.QtCore import Qt

import sys

from admin_backend import generate_report
from config.settings import add_url
from models.ReviewModel import Review
from models.ReviewParticipantModel import ReviewParticipant
from services.git_service import RepositoryHelper
from services.login_service import add_user
from services.session_service import Session
from models import CommentModel

STYLE_SHEET = """
QWidget {
    background-color: #f5f5fa;  /* Light gray background */
    font-family: Arial, sans-serif;
    font-size: 14px;
    color: #333;  /* Dark text */
}

QPushButton {
    background-color: #4b0082;  /* Purple button */
    color: white;
    border: none;
    border-radius: 10px;
    padding: 10px;
    max-width: 400px;
}

QPushButton:hover {
    background-color: #5c2d91;  /* Lighter purple on hover */
}

QPushButton:pressed {
    background-color: #37005d;  /* Darker purple on press */
}

QLineEdit, QTextEdit, QComboBox {
    background-color: white;
    color: #333;
    border: 1px solid #ddd;
    border-radius: 10px;
    padding: 5px;
    max-width: 400px;
}

QLabel {
    font-size: 16px;
    font-weight: bold;
    color: #4b0082;  /* Purple text for labels */
}

QMessageBox {
    background-color: #f5f5fa;  /* Background for message box */
    color: #333;
}

QDialog {
    background-color: #f5f5fa;  /* Dialog background */
    border-radius: 10px;
}
"""


class RepositoryInputDialog(QDialog):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.main_window = main_window
        self.setWindowTitle("Repository Location")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        self.folder_input = QLineEdit(self)
        self.folder_input.setPlaceholderText("Select repository location")
        layout.addWidget(self.folder_input)

        self.browse_button = QPushButton("Browse", self)
        self.browse_button.clicked.connect(self.browse_folder)
        layout.addWidget(self.browse_button)

        self.confirm_button = QPushButton("Confirm", self)
        self.confirm_button.clicked.connect(self.confirm_location)
        layout.addWidget(self.confirm_button)

        self.setLayout(layout)

    def browse_folder(self):
        folder_dialog = QFileDialog()
        folder_path = folder_dialog.getExistingDirectory(self, "Select Repository Location")
        if folder_path:
            self.folder_input.setText(folder_path)

    def confirm_location(self):
        folder_path = self.folder_input.text().strip()
        if folder_path and os.path.isdir(folder_path) and not os.listdir(folder_path):
            QMessageBox.information(self, "Repository Location", f"Repository location set to: {folder_path}")
            Session().add_path(folder_path)
            self.close()
        else:
            QMessageBox.warning(self, "Error", "Please select a valid repository location.")


class LoginFrame(QWidget):
    """Frame F0: Login"""

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        center_layout = QVBoxLayout()
        center_layout.setAlignment(Qt.AlignCenter)

        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Username")
        center_layout.addWidget(self.username_input)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        center_layout.addWidget(self.password_input)

        self.login_button = QPushButton("Login", self)
        self.login_button.clicked.connect(self.authenticate_user)
        center_layout.addWidget(self.login_button)

        layout.addStretch()
        layout.addLayout(center_layout)
        layout.addStretch()

        self.setLayout(layout)

    def authenticate_user(self):
        username = self.username_input.text()
        password = self.password_input.text()

        # result = login(username, password)
        # if result is None:
        #     QMessageBox.warning(self, "Login Failed", "Invalid credentials!")
        # else:
        #     self.main_window.user_role = result
        #     self.main_window.navigate_to_frame(1)

        # just for testing

        if username == "admin" and password == "admin123":
            self.main_window.user_role = "Administrator"
            self.main_window.navigate_to_frame(1)
        elif username and password:
            self.main_window.user_role = "RegularUser"
            self.main_window.navigate_to_frame(1)
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid credentials!")


class MainMenuFrame(QWidget):
    """Frame F1: Main Menu"""

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.reviews = [
            Review(1, Session().getUserID(), "Review 1", "Description 1"),
            Review(2, Session().getUserID(), "Review 2", "Description 2"),
            Review(3, Session().getUserID() + 3, "Review 3", "Description 3", reviewParticipants=[Session().getUserID()])

        ]
        # self.reviews = [
        #     {"title": "Review 1", "author": "User A"},
        #     {"title": "Review 2", "author": "User B"},
        # ]
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        top_layout = QHBoxLayout()
        self.back_button = QPushButton("⚙️", self)
        self.back_button.setFixedSize(60, 60)
        self.back_button.setStyleSheet(
            "border-radius: 20px; background-color: #4b0082; color: white; font-size: 36px; font-weight: bold;")
        self.back_button.clicked.connect(lambda: self.main_window.navigate_to_frame(4))
        top_layout.addStretch()
        top_layout.addWidget(self.back_button)
        layout.addLayout(top_layout)

        center_layout = QVBoxLayout()
        center_layout.setAlignment(Qt.AlignCenter)

        self.add_review_button = QPushButton("Add New Review", self)
        self.add_review_button.clicked.connect(lambda: self.main_window.navigate_to_frame(2))
        center_layout.addWidget(self.add_review_button)

        self.admin_panel_button = QPushButton("Admin Panel", self)
        self.admin_panel_button.clicked.connect(lambda: self.main_window.navigate_to_frame(5))
        center_layout.addWidget(self.admin_panel_button)

        self.reviews_label = QLabel("Ongoing Reviews:", self)
        center_layout.addWidget(self.reviews_label)

        self.reviews_container = QWidget()
        self.reviews_layout = QVBoxLayout()
        self.reviews_container.setLayout(self.reviews_layout)
        center_layout.addWidget(self.reviews_container)

        self.see_more_button = QPushButton("See More", self)
        self.see_more_button.clicked.connect(lambda: self.main_window.navigate_to_frame(12))
        center_layout.addWidget(self.see_more_button)

        self.admin_panel_button.setEnabled(False)
        self.admin_panel_button.setVisible(False)

        layout.addStretch()
        layout.addLayout(center_layout)
        layout.addStretch()

        self.setLayout(layout)
        self.refresh_reviews()

    def refresh_reviews(self):
        for i in reversed(range(self.reviews_layout.count())):
            widget = self.reviews_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        for review in self.reviews[:4]:
            button = QPushButton(review.title, self)
            button.clicked.connect(lambda checked, r=review: self.open_review(r))
            self.reviews_layout.addWidget(button)

    def showEvent(self, event):
        self.admin_panel_button.setEnabled(self.main_window.user_role == "Administrator")
        self.admin_panel_button.setVisible(self.main_window.user_role == "Administrator")
        self.refresh_reviews()

    def open_review(self, review):
        if review.authorId == Session().getUserID():
            self.main_window.frames[9].set_review(review)
            self.main_window.navigate_to_frame(9)
        else:
            self.main_window.frames[6].set_review(review)
            self.main_window.navigate_to_frame(6)


class AddNewReviewFrame(QWidget):
    """Frame F2: Add New Review"""

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        top_layout = QHBoxLayout()
        self.back_button = QPushButton("←", self)
        self.back_button.setFixedSize(60, 60)
        self.back_button.setStyleSheet(
            "border-radius: 20px; background-color: #4b0082; color: white; font-size: 36px; font-weight: bold;")
        self.back_button.clicked.connect(lambda: self.main_window.navigate_to_frame(1))
        top_layout.addStretch()
        top_layout.addWidget(self.back_button)
        layout.addLayout(top_layout)

        center_layout = QVBoxLayout()
        center_layout.setAlignment(Qt.AlignCenter)

        form_widget = QWidget()
        form_layout = QFormLayout(form_widget)
        self.title_input = QLineEdit(self)
        self.description_input = QLineEdit(self)
        self.file_link_input = QLineEdit(self)

        form_layout.addRow("Title:", self.title_input)
        form_layout.addRow("Description:", self.description_input)
        form_layout.addRow("File Link:", self.file_link_input)

        self.next_button = QPushButton("Next", self)
        self.next_button.clicked.connect(self.validate_and_proceed)
        form_layout.addWidget(self.next_button)

        form_hbox = QHBoxLayout()
        form_hbox.addStretch()
        form_hbox.addWidget(form_widget)
        form_hbox.addStretch()

        center_layout.addLayout(form_hbox)

        layout.addStretch()
        layout.addLayout(center_layout)
        layout.addStretch()

        self.setLayout(layout)

    def validate_and_proceed(self):
        if all([self.title_input.text(), self.description_input.text(), self.file_link_input.text()]):
            session = Session()
            if session.getReviewBuilder() is None:
                session.initReviewBuilder(self.title_input.text(), self.description_input.text())
                session.getReviewBuilder()._review.fileLink = self.file_link_input.text()
            else:
                session.getReviewBuilder().add_title_and_desc(self.title_input.text(), self.description_input.text())
                session.getReviewBuilder()._review.fileLink = self.file_link_input.text()

            self.main_window.navigate_to_frame(3)  # Navigate to Frame F3
        else:
            QMessageBox.warning(self, "Validation Error", "All fields must be filled!")


class AddNewReviewStep2Frame(QWidget):
    """Frame F3: Add New Review #2"""

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        top_layout = QHBoxLayout()
        self.back_button = QPushButton("←", self)
        self.back_button.setFixedSize(60, 60)
        self.back_button.setStyleSheet(
            "border-radius: 20px; background-color: #4b0082; color: white; font-size: 36px; font-weight: bold;")
        self.back_button.clicked.connect(lambda: self.main_window.navigate_to_frame(2))
        top_layout.addStretch()
        top_layout.addWidget(self.back_button)
        layout.addLayout(top_layout)

        center_layout = QVBoxLayout()
        center_layout.setAlignment(Qt.AlignCenter)

        form_widget = QWidget()
        form_layout = QFormLayout(form_widget)

        self.reviewer_input = QLineEdit(self)
        self.reviewer_input.setPlaceholderText("Reviewer Username")
        form_layout.addRow("Assign Reviewer:", self.reviewer_input)

        self.commit_combo = QComboBox(self)
        self.populate_commit_combo()
        form_layout.addRow("Commit ID:", self.commit_combo)

        self.add_reviewer_button = QPushButton("Add Reviewer", self)
        self.add_reviewer_button.clicked.connect(self.add_reviewer)
        form_layout.addWidget(self.add_reviewer_button)

        self.add_commit_button = QPushButton("Add Commit", self)
        self.add_commit_button.clicked.connect(self.add_commit)
        form_layout.addWidget(self.add_commit_button)

        self.confirm_button = QPushButton("Confirm", self)
        self.confirm_button.clicked.connect(self.confirm_review)
        form_layout.addWidget(self.confirm_button)

        form_hbox = QHBoxLayout()
        form_hbox.addStretch()
        form_hbox.addWidget(form_widget)
        form_hbox.addStretch()

        center_layout.addLayout(form_hbox)

        layout.addStretch()
        layout.addLayout(center_layout)
        layout.addStretch()

        self.setLayout(layout)

    def populate_commit_combo(self):
        session = Session()
        commits = RepositoryHelper().fetch_commits_and_display(session.user)
        if commits:
            for commit in commits:
                self.commit_combo.addItem(f"{commit[0]} - {commit[1]}")

    def add_reviewer(self):
        reviewer = self.reviewer_input.text().strip()
        if reviewer:
            Session().getReviewBuilder().assign_reviewer(reviewer)
            QMessageBox.information(self, "Reviewer Added", f"Reviewer '{reviewer}' added successfully.")
            self.reviewer_input.clear()
        else:
            QMessageBox.warning(self, "Error", "Reviewer username cannot be empty.")

    def add_commit(self):
        commit_id = self.commit_combo.currentText().split(" - ")[0]
        if commit_id:
            Session().getReviewBuilder().add_commit(commit_id)
            QMessageBox.information(self, "Commit Added", f"Commit '{commit_id}' added successfully.")
        else:
            QMessageBox.warning(self, "Error", "Commit ID cannot be empty.")


    def confirm_review(self):
        reviewBuilder = Session().getReviewBuilder()

        reviewBuilder.add_author(Session().getUserID())
        # TODO add commits and reviewers choice
        # reviewBuilder.add_commits()
        # reviewBuilder.add_reviewers()
        # reviewBuilder.add_title_and_desc(self.main_window.frames[2].title_input.text(), self.main_window.frames[2].description_input.text())
        review = reviewBuilder.build()

        # FIXME
        # review = {
        #     "title": reviewBuilder._review.title,
        #     "description": reviewBuilder._review.description,
        #     "fileLink": reviewBuilder._review.fileLink,
        #     "author": Session().user.username,
        #     "commitId": reviewBuilder._review.commitId,
        #     "reviewParticipants": reviewBuilder._review.reviewParticipants,
        # }
        self.main_window.frames[1].reviews.append(review)
        QMessageBox.information(self, "Success", "Review added successfully!")
        self.main_window.navigate_to_frame(1)  # Navigate back to the main frame


class SettingsFrame(QWidget):
    """Frame F4: Settings"""

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        top_layout = QHBoxLayout()
        self.back_button = QPushButton("←", self)
        self.back_button.setFixedSize(60, 60)
        self.back_button.setStyleSheet("border-radius: 20px; background-color: #4b0082; color: white;")
        self.back_button.clicked.connect(lambda: self.main_window.navigate_to_frame(1))
        top_layout.addStretch()
        top_layout.addWidget(self.back_button)
        layout.addLayout(top_layout)

        center_layout = QVBoxLayout()
        center_layout.setAlignment(Qt.AlignCenter)

        form_widget = QWidget()
        form_layout = QFormLayout(form_widget)
        self.old_password_input = QLineEdit(self)
        self.old_password_input.setEchoMode(QLineEdit.Password)
        self.new_password_input = QLineEdit(self)
        self.new_password_input.setEchoMode(QLineEdit.Password)
        #self.options_combo = QComboBox(self)
        #self.options_combo.addItems(["Option 1", "Option 2", "Option 3"])
        form_layout.addRow("Old Password:", self.old_password_input)
        form_layout.addRow("New Password:", self.new_password_input)
        #form_layout.addRow("Select Option:", self.options_combo)

        self.confirm_button = QPushButton("Confirm Change", self)
        self.confirm_button.clicked.connect(self.confirm_changes)
        form_layout.addWidget(self.confirm_button)

        form_hbox = QHBoxLayout()
        form_hbox.addStretch()
        form_hbox.addWidget(form_widget)
        form_hbox.addStretch()

        center_layout.addLayout(form_hbox)

        layout.addStretch()
        layout.addLayout(center_layout)
        layout.addStretch()

        self.setLayout(layout)

    def confirm_changes(self):
        if all([self.new_password_input.text(), self.old_password_input.text()]):
            if Session().user.change_password(self.new_password_input.text(), self.old_password_input.text()):
                QMessageBox.information(self, "Settings Updated", "Successfully changed password!")
            else:
                QMessageBox.information(self, "Settings Updated", "Invalid current password.")
        QMessageBox.information(self, "Invalid input", "Do not leave empty fields!")


class AdminPanelFrame(QWidget):
    """Frame F5: Admin Panel"""

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        top_layout = QHBoxLayout()
        self.back_button = QPushButton("←", self)
        self.back_button.setFixedSize(60, 60)
        self.back_button.setStyleSheet(
            "border-radius: 20px; background-color: #4b0082; color: white; font-size: 36px; font-weight: bold;")
        self.back_button.clicked.connect(lambda: self.main_window.navigate_to_frame(1))
        top_layout.addStretch()
        top_layout.addWidget(self.back_button)
        layout.addLayout(top_layout)

        center_layout = QVBoxLayout()
        center_layout.setAlignment(Qt.AlignCenter)

        self.generate_report_button = QPushButton("Generate Report", self)
        self.generate_report_button.clicked.connect(self.generate_report)

        center_layout.addWidget(self.generate_report_button)

        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Username")
        center_layout.addWidget(self.username_input)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        center_layout.addWidget(self.password_input)

        self.is_admin_checkbox = QCheckBox("Is Admin", self)
        center_layout.addWidget(self.is_admin_checkbox)

        self.create_account_button = QPushButton("Create Account", self)
        self.create_account_button.clicked.connect(self.create_account)
        center_layout.addWidget(self.create_account_button)

        center_layout.addWidget(self.generate_report_button)
        layout.addStretch()
        layout.addLayout(center_layout)
        layout.addStretch()

        self.setLayout(layout)

    def generate_report(self):
        if self.main_window.user_role == "Administrator":
            generate_report()
            QMessageBox.information(self, "Report", "The report has been generated.")
        else:
            QMessageBox.information(self, "Insufficient role", "The report could not been generated. You are not the "
                                                               "admin!")

    def create_account(self):
        username = self.username_input.text()
        password = self.password_input.text()
        is_admin = self.is_admin_checkbox.isChecked()

        if username and password:
            add_user(username, password, is_admin)
            QMessageBox.information(self, "Success", f"User '{username}' created successfully!")
        else:
            QMessageBox.warning(self, "Error", "Username and password cannot be empty.")


class ReviewEvaluationFrame(QWidget):
    """Frame F6: Review Evaluation"""

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.review = None
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        top_layout = QHBoxLayout()
        self.back_button = QPushButton("←", self)
        self.back_button.setFixedSize(60, 60)
        self.back_button.setStyleSheet(
            "border-radius: 20px; background-color: #4b0082; color: white; font-size: 36px; font-weight: bold;")
        self.back_button.clicked.connect(lambda: self.main_window.navigate_to_frame(1))
        top_layout.addStretch()
        top_layout.addWidget(self.back_button)
        layout.addLayout(top_layout)

        center_layout = QVBoxLayout()
        center_layout.setAlignment(Qt.AlignCenter)

        self.evaluation_label = QLabel("Review Evaluation", self)
        center_layout.addWidget(self.evaluation_label)

        self.review_details = QLabel("", self)
        center_layout.addWidget(self.review_details)

        self.add_comment_button = QPushButton("Add Comment", self)
        self.add_comment_button.clicked.connect(self.open_add_comment_popup)
        center_layout.addWidget(self.add_comment_button)

        self.evaluate_button = QPushButton("Evaluate", self)
        self.evaluate_button.clicked.connect(self.open_verdict_popup)
        center_layout.addWidget(self.evaluate_button)

        layout.addStretch()
        layout.addLayout(center_layout)
        layout.addStretch()

        self.setLayout(layout)

    def set_review(self, review: Review):
        self.review = review
        self.review_details.setText(
            f"Title: {review.title}\n"
            f"Author: {review.authorId}\n"
            f"Description: {review.description}\n"
            f"File Link: {review.fileLink}\n"
            f"Commit ID: {', '.join(map(str, review.commitId))}\n"
            f"Review Participants: {', '.join(map(str, review.reviewParticipants))}\n"
        )
    def open_add_comment_popup(self):
        dialog = AddCommentPopup(self.main_window)
        self.main_window.frames[7].set_review(self.review)
        dialog.exec_()

    def open_verdict_popup(self):
        dialog = VerdictPopup(self.main_window)
        dialog.set_review(self.review)
        dialog.exec_()


class AddCommentPopup(QDialog):
    """Frame F7: Add Comment (Pop-up)"""

    def __init__(self, main_window):
        super().__init__(main_window)
        self.main_window = main_window
        self.review = None
        self.setWindowTitle("Add Comment")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        center_layout = QVBoxLayout()
        center_layout.setAlignment(Qt.AlignCenter)

        self.comment_input = QTextEdit(self)
        self.comment_input.setPlaceholderText("Write your comment here...")
        center_layout.addWidget(self.comment_input)

        self.save_button = QPushButton("Save", self)
        self.save_button.clicked.connect(self.save_comment)
        center_layout.addWidget(self.save_button)

        self.cancel_button = QPushButton("Cancel", self)
        self.cancel_button.clicked.connect(self.close)
        center_layout.addWidget(self.cancel_button)

        layout.addStretch()
        layout.addLayout(center_layout)
        layout.addStretch()

        self.setLayout(layout)
        
    def set_review(self, review: Review):
        self.review = review

    def save_comment(self):
        comment_text = self.comment_input.toPlainText()
        if comment_text:
            session = Session()
            # comment = CommentModel.Comment(
            #     reviewID=self.review.reviewId,
            #     authorID=session.getUserID(),
            #     content=comment_text
            # )
            self.review.addComments(session.getUserID(), comment_text)
            QMessageBox.information(self, "Comment Saved", "Your comment has been saved.")
            self.close()
        else:
            QMessageBox.warning(self, "Error", "Comment cannot be empty.")


class VerdictPopup(QDialog):
    """Frame F8: Verdict (Pop-up)"""

    def __init__(self, main_window):
        super().__init__(main_window)
        self.main_window = main_window
        self.review = None
        self.setWindowTitle("Give Evaluation")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        center_layout = QVBoxLayout()
        center_layout.setAlignment(Qt.AlignCenter)

        self.verdict_label = QLabel("Select Verdict:", self)
        center_layout.addWidget(self.verdict_label)

        self.verdict_combo = QComboBox(self)
        self.verdict_combo.addItems(["Accepted", "Rejected"])
        center_layout.addWidget(self.verdict_combo)

        self.comments_label = QLabel("Comments on this review:", self)
        center_layout.addWidget(self.comments_label)

        self.comments_display = QTextEdit(self)
        self.comments_display.setReadOnly(True)
        center_layout.addWidget(self.comments_display)

        self.evaluate_button = QPushButton("Evaluate", self)
        self.evaluate_button.clicked.connect(self.submit_verdict)
        center_layout.addWidget(self.evaluate_button)

        self.cancel_button = QPushButton("Cancel", self)
        self.cancel_button.clicked.connect(self.close)
        center_layout.addWidget(self.cancel_button)

        layout.addStretch()
        layout.addLayout(center_layout)
        layout.addStretch()

        self.setLayout(layout)

    def set_review(self, review: Review):
        self.review = review
        comments = review.seeComments()
        self.comments_display.setText("\n".join([str(comment) for comment in comments]))

    def submit_verdict(self):
        verdict = self.verdict_combo.currentText()
        if verdict:
            QMessageBox.information(self, "Verdict Submitted", f"The review has been {verdict.lower()}.")
            self.close()
        else:
            QMessageBox.warning(self, "Error", "Verdict cannot be empty.")


class OwnReviewEditFrame(QWidget):
    """Frame F9: Own Review Edit"""

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.review = None
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        top_layout = QHBoxLayout()
        self.back_button = QPushButton("←", self)
        self.back_button.setFixedSize(60, 60)
        self.back_button.setStyleSheet(
            "border-radius: 20px; background-color: #4b0082; color: white; font-size: 36px; font-weight: bold;")
        self.back_button.clicked.connect(lambda: self.main_window.navigate_to_frame(1))
        top_layout.addStretch()
        top_layout.addWidget(self.back_button)
        layout.addLayout(top_layout)

        center_layout = QVBoxLayout()
        center_layout.setAlignment(Qt.AlignCenter)

        self.review_label = QLabel("Edit Your Review:", self)
        center_layout.addWidget(self.review_label)

        self.review_details = QLabel("", self)
        center_layout.addWidget(self.review_details)

        self.edit_review_button = QPushButton("Edit Review", self)
        self.edit_review_button.clicked.connect(self.open_edit_review_popup)
        center_layout.addWidget(self.edit_review_button)

        self.see_comments_button = QPushButton("See Comments", self)
        self.see_comments_button.clicked.connect(self.open_see_comments_popup)
        center_layout.addWidget(self.see_comments_button)

        layout.addStretch()
        layout.addLayout(center_layout)
        layout.addStretch()

        self.setLayout(layout)

    def set_review(self, review):
        self.review = review
        self.review_details.setText(
            f"Title: {review['title']}\n"
            f"Author: {review['author']}\n"
            f"Description: {review['description']}\n"
            f"File Link: {review['fileLink']}\n"
            f"Commit ID: {', '.join(map(str, review['commitId']))}\n"
            f"Review Participants: {', '.join(map(str, review['reviewParticipants']))}\n"
        )

    def open_edit_review_popup(self):
        dialog = OwnReviewAddCommentPopup(self.main_window)
        dialog.set_review(self.review)
        dialog.exec_()

    def open_see_comments_popup(self):
        dialog = OwnReviewCommentsPopup(self.main_window)
        dialog.exec_()


class OwnReviewCommentsPopup(QDialog):
    """Frame F10: Own Review Edit/Comments (Pop-up)"""

    def __init__(self, main_window):
        super().__init__(main_window)
        self.setWindowTitle("Review Comments")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        center_layout = QVBoxLayout()
        center_layout.setAlignment(Qt.AlignCenter)

        self.comments_label = QLabel("Comments for this review:", self)
        center_layout.addWidget(self.comments_label)

        # Placeholder for comments
        self.comments_list = QTextEdit(self)
        self.comments_list.setText("Comment 1: Great work!\nComment 2: Needs improvement in section 2.")
        self.comments_list.setReadOnly(True)
        center_layout.addWidget(self.comments_list)

        self.close_button = QPushButton("Close", self)
        self.close_button.clicked.connect(self.close)
        center_layout.addWidget(self.close_button)

        layout.addStretch()
        layout.addLayout(center_layout)
        layout.addStretch()

        self.setLayout(layout)


class OwnReviewAddCommentPopup(QDialog):
    """Frame F11: Own Review Edit"""

    def __init__(self, main_window):
        super().__init__(main_window)
        self.main_window = main_window
        self.review = None
        self.setWindowTitle("Edit Review")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        center_layout = QVBoxLayout()
        center_layout.setAlignment(Qt.AlignCenter)

        self.title_label = QLabel("Edit Title:", self)
        center_layout.addWidget(self.title_label)
        self.title_input = QLineEdit(self)
        center_layout.addWidget(self.title_input)

        self.detail2_label = QLabel("Edit Detail 2:", self)
        center_layout.addWidget(self.detail2_label)
        self.detail2_input = QLineEdit(self)
        center_layout.addWidget(self.detail2_input)

        self.detail3_label = QLabel("Edit Detail 3:", self)
        center_layout.addWidget(self.detail3_label)
        self.detail3_input = QLineEdit(self)
        center_layout.addWidget(self.detail3_input)

        self.save_button = QPushButton("Save", self)
        self.save_button.clicked.connect(self.save_review)
        center_layout.addWidget(self.save_button)

        self.cancel_button = QPushButton("Cancel", self)
        self.cancel_button.clicked.connect(self.close)
        center_layout.addWidget(self.cancel_button)

        layout.addStretch()
        layout.addLayout(center_layout)
        layout.addStretch()

        self.setLayout(layout)

    def set_review(self, review):
        self.review = review
        self.title_input.setText(review.get("title", ""))
        self.detail2_input.setText(review.get("detail2", ""))
        self.detail3_input.setText(review.get("detail3", ""))

    def save_review(self):
        if self.review:
            self.review["title"] = self.title_input.text().strip()
            self.review["detail2"] = self.detail2_input.text().strip()
            self.review["detail3"] = self.detail3_input.text().strip()
            QMessageBox.information(self, "Review Updated", "Your review has been updated.")
            self.close()
        else:
            QMessageBox.warning(self, "Error", "No review to update.")


class ViewAllReviewsFrame(QWidget):
    """Frame F12: View All Reviews"""

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        center_layout = QVBoxLayout()
        center_layout.setAlignment(Qt.AlignCenter)

        top_layout = QHBoxLayout()
        self.back_button = QPushButton("←", self)
        self.back_button.setFixedSize(60, 60)
        self.back_button.setStyleSheet(
            "border-radius: 20px; background-color: #4b0082; color: white; font-size: 36px; font-weight: bold;")
        self.back_button.clicked.connect(lambda: self.main_window.navigate_to_frame(1))
        top_layout.addStretch()
        top_layout.addWidget(self.back_button)
        layout.addLayout(top_layout)

        self.title_label = QLabel("All Reviews:", self)
        center_layout.addWidget(self.title_label)

        self.reviews_list = QWidget()
        self.reviews_layout = QVBoxLayout()
        self.reviews_list.setLayout(self.reviews_layout)
        center_layout.addWidget(self.reviews_list)

        layout.addStretch()
        layout.addLayout(center_layout)
        layout.addStretch()

        self.setLayout(layout)

    def refresh_reviews(self):
        for i in reversed(range(self.reviews_layout.count())):
            widget = self.reviews_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        for review in self.main_window.frames[1].reviews:
            button = QPushButton(f"{review['title']} (Author: {review['author']})", self)
            button.clicked.connect(lambda checked, r=review: self.open_review_details(r))
            self.reviews_layout.addWidget(button)

    def open_review_details(self, review):
        self.main_window.frames[13].set_review(review)
        self.main_window.navigate_to_frame(13)

    def showEvent(self, event):
        self.refresh_reviews()


class ViewReviewDetailsFrame(QWidget):
    """Frame F13: View Review Details"""

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.review = None
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        center_layout = QVBoxLayout()
        center_layout.setAlignment(Qt.AlignCenter)

        self.details_label = QLabel("Review Details:", self)
        center_layout.addWidget(self.details_label)

        self.review_details = QLabel("", self)
        center_layout.addWidget(self.review_details)

        self.add_comment_button = QPushButton("Add Comment", self)
        self.add_comment_button.clicked.connect(self.navigate_to_add_comment)
        center_layout.addWidget(self.add_comment_button)

        self.admin_panel_button = QPushButton("Archive Review", self)
        self.admin_panel_button.clicked.connect(lambda: self.main_window.navigate_to_frame(12))
        center_layout.addWidget(self.admin_panel_button)

        self.back_button = QPushButton("Back", self)
        self.back_button.clicked.connect(lambda: self.main_window.navigate_to_frame(12))
        center_layout.addWidget(self.back_button)

        self.admin_panel_button.setEnabled(False)
        self.admin_panel_button.setVisible(False)

        layout.addStretch()
        layout.addLayout(center_layout)
        layout.addStretch()

        self.setLayout(layout)

    def set_review(self, review):
        self.review = review
        self.review_details.setText(
            f"Title: {review['title']}\n"
            f"Author: {review['author']}\n"
            f"Description: {review['description']}\n"
            f"File Link: {review['fileLink']}\n"
            f"Commit ID: {', '.join(map(str, review['commitId']))}\n"
            f"Review Participants: {', '.join(map(str, review['reviewParticipants']))}\n"
        )

    def showEvent(self, event):
        self.admin_panel_button.setEnabled(self.main_window.user_role == "Administrator")
        self.admin_panel_button.setVisible(self.main_window.user_role == "Administrator")
        # self.refresh_reviews()

    def navigate_to_add_comment(self):
        if self.review:
            self.main_window.frames[14].set_review(self.review)
            self.main_window.navigate_to_frame(14)


class AddReviewCommentFrame(QWidget):
    """Frame F14: Add Review Comment"""

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.review = None
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        center_layout = QVBoxLayout()
        center_layout.setAlignment(Qt.AlignCenter)

        self.comments_label = QLabel("Comments for this Review:", self)
        center_layout.addWidget(self.comments_label)

        self.comments_display = QTextEdit(self)
        self.comments_display.setReadOnly(True)
        center_layout.addWidget(self.comments_display)

        self.back_button = QPushButton("Back", self)
        self.back_button.clicked.connect(lambda: self.main_window.navigate_to_frame(13))
        center_layout.addWidget(self.back_button)
        
        layout.addStretch()
        layout.addLayout(center_layout)
        layout.addStretch()

        self.setLayout(layout)

    def set_review(self, review):
        self.review = review
        self.display_comments()

    def display_comments(self):
        comments = self.review.get("comments", [])
        comments_text = "\n\n".join(comments)
        self.comments_display.setText(comments_text)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Application UI")
        self.setGeometry(100, 100, 800, 600)

        self.user_role = None  # Keeps track of the user role
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        if Session().get_first_time():
            self.show_repository_input_dialog()
            RepositoryHelper(Session().get_path(), True, Session().get_url())
            add_url(Session().get_path())
        else:
            RepositoryHelper(Session().get_path())

        # Create frames
        self.frames = {
            0: LoginFrame(self),
            1: MainMenuFrame(self),
            2: AddNewReviewFrame(self),
            3: AddNewReviewStep2Frame(self),
            4: SettingsFrame(self),
            5: AdminPanelFrame(self),
            6: ReviewEvaluationFrame(self),
            7: AddCommentPopup(self),
            8: VerdictPopup(self),
            9: OwnReviewEditFrame(self),
            10: OwnReviewCommentsPopup(self),
            11: OwnReviewAddCommentPopup(self),
            12: ViewAllReviewsFrame(self),
            13: ViewReviewDetailsFrame(self),
            14: AddReviewCommentFrame(self),
        }

        # Add frames to stacked widget
        for index, frame in self.frames.items():
            self.stacked_widget.addWidget(frame)

        # Set the initial frame to F0 (Login)
        self.stacked_widget.setCurrentWidget(self.frames[0])


    def navigate_to_frame(self, frame_index):
        """Navigate to a specific frame by index."""
        if frame_index in self.frames:
            self.stacked_widget.setCurrentWidget(self.frames[frame_index])

    def show_repository_input_dialog(self):
        dialog = RepositoryInputDialog(self)
        dialog.exec_()


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(STYLE_SHEET)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

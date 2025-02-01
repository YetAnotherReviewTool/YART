import PyQt5
import pytest
from PyQt5.QtWidgets import QApplication
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt
from userInterface import MainWindow


@pytest.fixture
def app(qtbot):
    test_app = MainWindow()
    qtbot.addWidget(test_app)
    return test_app


@pytest.fixture
def login_frame(app):
    return app.frames[0]


def test_valid_admin_login(qtbot, app, login_frame):
    """Test that admin login navigates to the main menu."""
    login_frame.username_input.setText("admin")
    login_frame.password_input.setText("admin123")

    qtbot.mouseClick(login_frame.login_button, Qt.LeftButton)

    assert app.user_role == "Administrator"
    assert app.stacked_widget.currentWidget() == app.frames[1]  # MainMenuFrame


def test_valid_user_login(qtbot, app, login_frame):
    """Test that a regular user login navigates to the main menu."""
    login_frame.username_input.setText("user")
    login_frame.password_input.setText("password")

    qtbot.mouseClick(login_frame.login_button, Qt.LeftButton)

    assert app.user_role == "RegularUser"
    assert app.stacked_widget.currentWidget() == app.frames[1]  # MainMenuFrame


def test_invalid_login(qtbot, app, login_frame, mocker):
    """Test that an invalid login attempt shows an error message."""
    mocker.patch("PyQt5.QtWidgets.QMessageBox.warning")

    login_frame.username_input.setText("invalid")
    login_frame.password_input.setText("wrongpass")

    qtbot.mouseClick(login_frame.login_button, Qt.LeftButton)

    assert app.user_role is None  # User role should remain unset
    assert app.stacked_widget.currentWidget() == login_frame  # Should still be on login frame
    PyQt5.QtWidgets.QMessageBox.warning.assert_called_once()

import pytest
from PyQt5.QtCore import Qt

from config.settings import read_config
from services.session_service import Session
from userInterface import MainWindow

@pytest.fixture(scope="module", autouse=True)
def setup_session():
    url, path = read_config()
    if path is None:
        Session().set_first_time()
    else:
        Session().path = path
    Session().add_url(url)

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
    assert app.stacked_widget.currentWidget() == app.frames[1]


def test_valid_user_login(qtbot, app, login_frame):
    """Test that a regular user login navigates to the main menu."""
    login_frame.username_input.setText("username")
    login_frame.password_input.setText("password")

    qtbot.mouseClick(login_frame.login_button, Qt.LeftButton)

    assert app.user_role == "RegularUser"
    assert app.stacked_widget.currentWidget() == app.frames[1]  # MainMenuFrame
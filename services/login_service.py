from models.UserModel import User
from services.session_service import Session


def check_correct_password(username, password) -> bool:
    # PLACEHOLDER SO PYCHARM WON'T SCREAM AT ME, REPLACE, PROBABLY IN DIFFERENT PLACE TO API CALL
    pass


def get_user_by_username(username) -> User:
    # PLACEHOLDER SO PYCHARM WON'T SCREAM AT ME, REPLACE, PROBABLY IN DIFFERENT PLACE TO API CALL
    pass

def add_user(username: str, password: str, admin: bool):
    # PLACEHOLDER
    pass

def login(username: str, password: str):
    if not check_correct_password(username, password):
        return None

    user = get_user_by_username(username)
    session = Session()
    session.userID = user.userID
    if user.admin:
        return "Administrator"
    return "RegularUser"

from models.UserModel import User
from models.DatabaseModelHelper import DatabaseHelper
from services.session_service import Session

def add_user(username: str, password: str, admin: bool):
    userId = DatabaseHelper.getNextId(User)
    newUser = User(userId, username, password, admin)
    DatabaseHelper.insertIntoDbFromModel(User, newUser)

def login(username: str, password: str):
    if not User.verifyPassword(username, password):
        return None

    user = DatabaseHelper.getModelsFromDbQuery(User, "username", username)
    session = Session()
    session.userID = user.userID
    if user.admin:
        return "Administrator"
    return "RegularUser"

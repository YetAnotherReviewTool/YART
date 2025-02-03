from models.UserModel import User
from models.DatabaseModelHelper import DatabaseHelper
from services.session_service import Session

def add_user(username: str, password: str, admin: bool):
    userId = DatabaseHelper.getNextId(User)
    newUser = User(userId, username, password, "", admin)
    newUser.salt = User.makeSalt()
    newUser.password_hash = User.hash_password(newUser.salt, password)
    DatabaseHelper.insertIntoDbFromModel(User, newUser)

def login(username: str, password: str):
    user = DatabaseHelper.getModelsFromDbQuery(User, "username", username)
    if len(user) <= 0:
        return None

    if not user[0].verifyPassword(password):
        return None

    session = Session()
    session.user = user[0]
    session.userID = user[0].userID
    if user[0].admin:
        return "Administrator"
    return "RegularUser"

if __name__ == "__main__":
    add_user("stud", "stud", False)
    add_user("admin", "admin123", True)
    users = DatabaseHelper.getModelsFromDb(User)
    for user in users:
        print(user.username, user.password_hash, user.salt)
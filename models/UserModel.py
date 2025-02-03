import models.ReviewModel as ReviewModel
from models.DatabaseModelHelper import DatabaseHelper
from models.ReviewParticipantModel import ReviewParticipant
from models.model import Model

import secrets
import hashlib
import base64

SALT_LENGTH = 16

class AccessError(PermissionError):
    """
    Custom exception for handling inufficient permissions.

    This exception is raised when an user with no admin permissions attempts to generate a report.
    """
    pass

class User(Model):
    def __init__(self, 
                 userID: int, 
                 username: str, 
                 password_hash: str, 
                 salt: str = "",
                 admin: bool = False,
                 ):
        
        self.userID: int = userID
        self.username: str = username
        self.password_hash: str = password_hash
        self.salt: str = salt
        self.admin: bool = admin

        self.reviews: list[int] = DatabaseHelper.getValuesFromDb(ReviewParticipant, "reviewID", "userID", self.userID)

    def new (username: str, password_plain: str, admin: bool = False):
        salt: str = User.makeSalt()
        return User(
            userID = DatabaseHelper.getNextId(User),
            username = username,
            salt = salt,
            password_hash = User.hash_password(salt, password_plain),
            admin = admin,
            reviews = [],
        )
    
    def createReview(self, title: str, description: str):

        id = DatabaseHelper.getNextId(ReviewModel.Review)
        newReview = ReviewModel.Review(id, title, description, self.userID)
        self.reviews.append(id)

        DatabaseHelper.insertIntoDbFromModel(ReviewModel.Review, newReview)


    def change_password(self, old_password, new_password) -> bool:
        if User.verifyPassword(old_password):
            self.salt = User.makeSalt()
            self.password_hash =  User.hash_password(self.salt, new_password)



            DatabaseHelper.updateDbRow(User, self.userID, "salt", self.salt)
            DatabaseHelper.updateDbRow(User, self.userID, "password_hash", self.password_hash)
            return True
        else:
            return False
        

    def makeSalt():
        return secrets.token_urlsafe(SALT_LENGTH)
    
    def verifyPassword(self, passedPassword):
        return secrets.compare_digest(self.password_hash, User.hash_password(self.salt, passedPassword))
    
    def getReviews(self) -> list:
        return DatabaseHelper.getModelsFromDbQuery(ReviewModel.Review, "authorID", self.userID)
    
    def hash_password(salt: str, pass_unhashed: str) -> str:
        return str(
            base64.urlsafe_b64encode(      
                hashlib.sha256(
                    salt.encode("utf-8") + pass_unhashed.encode("utf-8")
                ).digest()
            )
        )
    
    def jsonify(self):
        return {
            "userID": self.userID,
            "username": self.username,
            "salt": self.salt,
            "password_hash": self.password_hash,
            "admin": self.admin
        }
    
    def constructFromDbData(data):
        users_data = data
        users = []

        for row in users_data:
            users.append(User(
                userID=row["userID"],
                username=row["username"],
                password_hash=row["password_hash"],
                salt=row["salt"],
                admin=bool(row["admin"])
            ))

        return users
        


    




        
        

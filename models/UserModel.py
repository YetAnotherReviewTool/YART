import models.ReviewModel as ReviewModel
from models.DatabaseModelHelper import DatabaseHelper

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

class User:
    def __init__(self, 
                 userID: int, 
                 username: str, 
                 password_hash: str, 
                 salt: str = "",
                 admin: bool = False,
                 reviews: list[int] = []
                 ):
        
        self.userID: int = userID
        self.username: str = username
        self.password_hash: str = password_hash
        self.salt: str = salt
        self.admin: bool = admin

        self.reviews: list[int] = reviews

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

        DatabaseHelper.updateDbRow(User, self.userID, "reviews", self.reviews)

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
        


    




        
        

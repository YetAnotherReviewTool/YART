import models.ReviewModel as ReviewModel
from models.DatabaseModelHelper import DatabaseHelper

import secrets
import hashlib
import base64


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
                 passwordHash: str, 
                 salt: str = "",
                 admin: bool = False,
                 reviews: list[int] = []
                 ):
        
        self.userID: int = userID
        self.username: str = username
        self.passwordHash: str = passwordHash
        self.salt: str = salt
        self.admin: bool = admin

        self.reviews: list[int] = reviews

    def new (self, username: str, password: str, admin: bool = False):
        self.userID = DatabaseHelper.getNextId(User)
        self.username = username
        self.salt = secrets.token_urlsafe(16)
        self.passwordHash = User.hash_password(self.salt, password)
        self.admin = admin
        self.reviews = []
    def createReview(self, title: str, description: str):

        from models.DatabaseModelHelper import DatabaseHelper
        from models import ReviewModel
        id = DatabaseHelper.getNextId(ReviewModel.Review)
        newReview = ReviewModel.Review(id, title, description, self.userID)
        self.reviews.append(id)

        DatabaseHelper.updateDbRow(User, self.userID, "reviews", self.reviews)

        DatabaseHelper.insertIntoDbFromModel(ReviewModel.Review, newReview)


    def change_password(self, old_password, new_password) -> bool:
        if User.verifyPassword(old_password):
            newPasswordHash =  User.passwordHashFunction(new_password)
            self.passwordHash = newPasswordHash

            from models.DatabaseModelHelper import DatabaseHelper

            DatabaseHelper.updateDbRow(User, self.userID, "passwordHash", newPasswordHash)
            return True
        else:
            return False
        

    def verifyPassword(self, passedPassword):
        return secrets.compare_digest(self.passwordHash, self.hash_password(self.salt, passedPassword))
    def getReviews(self) -> list:
        return DatabaseHelper.getModelsFromDbQuery(ReviewModel.Review, "authorID", self.userID)
    
    def hash_password(salt: str, pass_unhashed: str) -> str:
        return str(
            base64.urlsafe_b64encode(      
                hashlib.sha256(
                    salt + pass_unhashed.encode("utf-8")
                ).digest()
            )
        )
        


    




        
        

import models.ReviewModel as ReviewModel
from models.DatabaseModelHelper import DatabaseHelper


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
                 admin: bool = False,
                 reviews: list[int] = []
                 ):
        
        self.userID: int = userID
        self.username: str = username
        self.passwordHash: str = passwordHash
        self.admin: bool = admin
        self.reviews: list[int] = reviews

    def createReview(self, title: str, description: str):

        id = DatabaseHelper.getNextId(ReviewModel.Review)
        newReview = ReviewModel.Review(id, title, description, self.userID)
        self.reviews.append(id)
        DatabaseHelper.updateDbRow(User, self.userID, "reviews", self.reviews)

        DatabaseHelper.insertIntoDbFromModel(ReviewModel.Review, newReview)


    def change_password(self, old_password, new_password) -> bool:
        if User.verifyPassword(old_password):
            newPasswordHash =  User.passwordHashFunction(new_password)
            self.passwordHash = newPasswordHash
            DatabaseHelper.updateDbRow(User, self.userID, "passwordHash", newPasswordHash)
            return True
        else:
            return False
        

    def verifyPassword(self, passedPassword):
        return User.passwordHashFunction(passedPassword) == self.passwordHash

    def getReviews(self) -> list:
        return DatabaseHelper.getModelsFromDbQuery(ReviewModel.Review, "authorID", self.userID)
    
    def passwordHashFunction(plainText: str) -> str:
        # Maybe put something fancier here? maybe TODO
        return plainText
        


    




        
        

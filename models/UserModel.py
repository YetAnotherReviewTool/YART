import ReviewModel
from UserModel import User
import datetime
import ReviewModel
from DatabaseModelHelper import DatabaseHelper


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
                 admin: bool,
                 reviews: list[int]
                 ):
        
        self.userID: int = userID
        self.username: str = username
        self.passwordHash: str = passwordHash
        self.admin: bool = admin
        self.reviews: list[int] = reviews

    def createReview(self, title: str, description: str):
        reviewId = 0  #somehow figure out new id from database

        newReview = ReviewModel.Review(reviewId, title, description, self.userID)
        self.reviews.append(reviewId)

        DatabaseHelper.updateDbRow(User, self.userID, "reviews", self.reviews)

        DatabaseHelper.insertIntoDbFromModel(ReviewModel.Review, newReview)
        

    def openReview(reviewID: int):
        pass

        #whatever this is supposed to do? TODO

    def change_password(self, old_password, new_password):
        #is_correct_password()
        pass

    def settings(self):
        pass

    def getReviews(self) -> list[ReviewModel.Review]:
        return DatabaseHelper.getModelsFromDbQuery(ReviewModel.Review, "authorID", self.userID)
        


    




        
        

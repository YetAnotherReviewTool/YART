import ReportModel
import ReviewModel
import datetime

class AccessError(PermissionError):
    """
    Custom exception for handling inufficient permissions.

    This exception is raised when an user with no admin permissions attempts to generate a report.
    """
    pass

class User:
    #meow meow meow
    def __init__(self):
        self.userID: int
        self.username: str
        self.passwordHash: str
        self.admin: bool

        self.reviews: list[int]

    def createReview(self, title: str, description: str, reviewID: int):
        newReview = ReviewModel.review(title, description)

        #add new review to DB #TODO

        self.reviews.append(reviewID)

    
    def openReview(reviewID: int):
        pass

        #whatever this is supposed to do? TODO


    def generateReport(self) -> ReportModel.Report:
        if not self.admin:
            raise AccessError
        else:
            return ReportModel.Report #TODO
        
    def settings():
        pass
        
    def getFromDB(userID):
        pass #TODO

    def insertToDB(self):
        pass #TODO
        


    




        
        

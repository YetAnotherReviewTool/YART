from models.ReviewModel import Review
from services.review_service import ReviewBuilder
from services.singleton import singleton


@singleton
class Session:
    userID = None
    reviewBuilder = None

    def __init__(self):
        pass

    def getReviewBuilder(self):
        return self.reviewBuilder

    def initReviewBuilder(self):
        self.reviewBuilder = ReviewBuilder()

    def getUserID(self):
        return self.userID

    def setUserID(self, new_user_id):
        self.userID = new_user_id

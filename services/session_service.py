from models.ReviewModel import Review
from services.review_service import ReviewBuilder


def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


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

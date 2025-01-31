from models.ReviewModel import Review


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
    reviewCreated = None

    def __init__(self):
        pass

    def getReviewCreated(self):
        return self.reviewCreated

    def setReviewCreated(self, new_review: Review | None):
        self.reviewCreated = new_review

    def getUserID(self):
        return self.userID

    def setUserID(self, new_user_id):
        self.userID = new_user_id

from models.ReviewModel import Review
from models.UserModel import User
from services.git_service import RepositoryHelper
from services.review_service import ReviewBuilder
from services.singleton import singleton


@singleton
class Session:
    user = User(1, "SJCaldwell", "ADB123")
    reviewBuilder: ReviewBuilder
    is_first_time = False

    def __init__(self):
        self.path = None
        self.url = None
        self.reviewBuilder = None

    def getReviewBuilder(self):
        return self.reviewBuilder

    def initReviewBuilder(self, title: str, description: str):
        self.reviewBuilder = ReviewBuilder(RepositoryHelper(), title, description)

    def getUserID(self):
        return self.user.userID

    def setUserID(self, new_user):
        self.user = new_user

    def set_first_time(self):
        self.is_first_time = True

    def get_first_time(self):
        return self.is_first_time

    def add_url(self, url: str):
        self.url = url

    def get_url(self):
        return self.url

    def add_path(self, path: str):
        self.path = path

    def get_path(self):
        return self.path


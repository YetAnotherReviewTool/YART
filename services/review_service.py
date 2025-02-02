from typing import List, Dict, Optional, Tuple

from git import Commit

from models.ReviewModel import Review
from models.DatabaseModelHelper import DatabaseHelper
from models.ReviewParticipantModel import ParticipantRole
from models.UserModel import User
from services.git_service import RepositoryHelper


class ReviewBuilder:

    def __init__(self, helper: RepositoryHelper, title: str, description: str) -> None:
        super().__init__()
        self._helper = helper
        self._review = Review(DatabaseHelper.getNextId(Review))
        self.add_title_and_desc(title, description)

    def add_title_and_desc(self, title: str, description: str):
        self._review.title = title
        self._review.description = description

    def add_author(self, user_id):
        self._review.authorId = user_id

    def add_commit(self, review_hex: str):
        self._review.commitId.append(int(review_hex, 16))   #  Looks good?

    def assign_reviewer(self, reviewerID:str, role: ParticipantRole = ParticipantRole.REVIEWER):
        self._review.assignReviewer(int(reviewerID, 16))

    def build(self):
        return self._review
        self.saveToDb()

    def saveToDb(self):
        # Call this after you're done with the Review object!! #TODO
        DatabaseHelper.insertIntoDbFromModel(Review, self._review)

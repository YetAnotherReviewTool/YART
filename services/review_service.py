from typing import List, Dict, Optional, Tuple

from git import Commit

from models.ReviewModel import Review
from models.DatabaseModelHelper import DatabaseHelper
from models.ReviewParticipantModel import ParticipantRole, ReviewParticipant, ParticipantStatus
from models.UserModel import User
from services.git_service import RepositoryHelper


class ReviewBuilder:

    def __init__(self, helper: RepositoryHelper, title: str, description: str) -> None:
        super().__init__()
        self._helper = helper
        self.id = DatabaseHelper.getNextId(Review)
        self._review = Review(self.id)
        self.add_title_and_desc(title, description)
        self.reviewers = []

    def add_title_and_desc(self, title: str, description: str):
        self._review.title = title
        self._review.description = description

    def add_author(self, user_id):
        self._review.authorId = user_id

    def add_commit(self, review_hex: str):
        self._review.commitId.append(int(review_hex, 16))  # Looks good?

    def assign_reviewer(self, reviewer: str, role: ParticipantRole = ParticipantRole.REVIEWER):
        reviewers = DatabaseHelper.getModelsFromDbQuery(User, "username", reviewer[1:])

        if len(reviewers) < 0:
            raise ValueError(f"No user with username {reviewer}")

        self.reviewers.append(
            ReviewParticipant(
                userID=reviewers[0].userID,
                reviewID=self.id,
                role=role,
                isAccepted=ParticipantStatus.IN_PROGRESS
            )
        )

    def build(self):
        self.saveToDb()
        return self._review

    def saveToDb(self):
        # Call this after you're done with the Review object!! #TODO
        DatabaseHelper.insertIntoDbFromModel(Review, self._review)
        for reviewer in self.reviewers:
            DatabaseHelper.insertIntoDbFromModel(ReviewParticipant, reviewer)


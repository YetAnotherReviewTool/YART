from typing import List, Dict, Optional, Tuple

from git import Commit

from models.ReviewModel import Review
from models.DatabaseModelHelper import DatabaseHelper
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

    def fetch_commits_and_display(
        self, user: str
    ) -> list[tuple[str, str | bytes | None, int | None]] | None:
        """
        Fetches commits and prepares them for display.

        Args:
            user (str): user whose commits we should get

        Returns:
            List[tuple] | None: list of commit details for display or None if there are no reviews
        """
        commits = self._helper.get_commits_by_user(user)

        if len(commits) == 0:
            return None

        return [
            (commit.hexsha, commit.message, commit.committed_date) for commit in commits
        ]
    
    def saveToDb(self):
        # Call this after you're done with the Review object!! #TODO
        DatabaseHelper.insertIntoDbFromModel(Review, self._review)

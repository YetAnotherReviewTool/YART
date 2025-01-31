from typing import List, Dict, Optional, Tuple

from git import Commit

from models.ReviewModel import Review
from services.git_service import RepositoryHelper


class ReviewBuilder:

    def __init__(self, helper: RepositoryHelper) -> None:
        super().__init__()
        self._helper = helper
        self._review = Review()

    def add_title_and_desc(self, tile: str, description: str):
        pass

    def add_author(self, user_id):
        pass

    def fetch_commits_and_display(self, user: str) -> list[tuple[str, str | bytes | None, int | None]] | None:
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

        return [(commit.hexsha, commit.message, commit.committed_date) for commit in commits]

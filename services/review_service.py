from typing import List, Dict, Optional

from git import Commit

from services.git_service import RepositoryHelper


class ReviewSystemBackend():


    def __init__(self, helper: RepositoryHelper) -> None:
        super().__init__()
        self._helper = helper

    def verify_review_details(self, details) -> bool:
        """
        Template function to verify the validity of review details.
        """
        raise NotImplementedError("suggest_reviewers needs implementation.")

    def suggest_reviewers(self, commit_hash: str) -> List[str]:
        """
        Template function to suggest reviewers based on the commit history.
        To be implemented by the data layer.
        """
        raise NotImplementedError("suggest_reviewers needs implementation.")

    def save_review(self, details, reviewers: List[str]):
        """
        Template function to save the review with the provided details and reviewers.
        To be implemented by the data layer.
        """
        raise NotImplementedError("save_review needs implementation.")

    def fetch_commits_and_display(self, user: str) -> List[Commit]:
        """
        Fetches commits and prepares them for display.
        TODO, what does frontend need?
        """
        commits = self._helper.get_commits_by_user(user)
        for idx, commit in enumerate(commits, start=1):
            print(f"{idx}: {commit['hash']} - {commit['message']}")
        return commits


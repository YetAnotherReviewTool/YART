import logging
import re
from typing import List, Dict
import git
from git import Repo, GitCommandError, Commit, NULL_TREE

from models.UserModel import User
from services.singleton import singleton


class InvalidGitURL(ValueError):
    """
    Custom exception for invalid Git repository URLs.

    This exception is raised when a provided Git repository URL
    is empty or does not meet the expected format.

    Example scenarios where this exception might be raised:
    - The URL does not start with `http://`, `https://`, or `git@`.
    - The URL does not end with .git
    """

    pass


@singleton
class RepositoryHelper:
    """
    A helper class for interacting with Git repositories to retrieve information.

    This class provides functionality for accessing and retrieving metadata
    and information from a Git repository. It is designed for read-only
    operations such as fetching commits, authors, branches, and logs, and does
    not support modifying the repository.

    Attributes:
        _repo (Repo): A GitPython `Repo` object representing the Git repository.

    Methods:
        __init_repository__(local_path: str, is_new_repo: bool, repo_url: str = "") -> Repo | None:
            Initializes the Git repository by cloning a new repository or loading an existing one.

        get_latest_commits(branch: str = "main") -> List[Commit]:
            Fetches the latest commits for a specified branch.

        get_commits_by_user(author_name: str) -> List[Commit]:
            Retrieves a list of commits authored by a specific user.

        get_branches() -> List[str]:
            Returns a list of all branches in the repository.

        get_repo_stats() -> Dict[str, int]:
            Provides general repository statistics, such as commit count and branch count.

    Note:
        There is 50% chance it's going to blow up when I try this the first time. It didn't, hooray!
    """

    def __init__(self, local_path: str = "", is_new_repo: bool = False, repo_url: str = "") -> None:
        """
        Initialize a RepositoryHelper instance.

        Args:
            local_path (str): Path to the local repository.
            is_new_repo (bool): Whether the repository is new.
            repo_url (str, optional): URL for cloning the repository. Defaults to "".
        """
        super().__init__()

        self._repo = self.__init_repository__(local_path, is_new_repo, repo_url)

        # possible future handling of incorrect urls, for example a pop-up or smth
        if not self._repo:
            logging.error("Failed to initialize the repository")
            raise ValueError("Invalid repository initialization")

        logging.debug("Repository initialized")

    def __init_repository__(
        self, local_path: str, is_new_repo: bool, repo_url: str = ""
    ) -> Repo | None:
        """
        Validate Git repository URL with multiple checks

        Args:
            local_path (str): Git repository URL
            is_new_repo
            repo_url (url): Git repository URL
        Returns:
            Repo | None: Repo object initialized using the parameters or None if any part of initialization failed
        """

        try:
            if is_new_repo:
                validate_git_repository_url(repo_url)
                return Repo.clone_from(repo_url, local_path)

            return Repo(local_path)

        except (
            git.exc.InvalidGitRepositoryError,
            git.exc.NoSuchPathError,
            InvalidGitURL,
        ) as e:
            logging.error("Could not init repository: " + e)
            return

    def get_latest_commits(self, branch: str = "main", count: int = 5) -> List[Commit]:
        """
        Retrieve the latest commits from the specified branch.

        Args:
            branch (str, optional): Branch name. Defaults to "main".
            count (int, optional): Number of commits to retrieve. Defaults to 5.

        Returns:
            List[Commit]: List of commit objects.
        """
        try:
            commits = list(self._repo.iter_commits(branch, max_count=count))
            return commits
        except GitCommandError as e:
            logging.error(f"Failed to fetch commits from branch '{branch}': {e}")
            return []

    def get_commits_by_user(self, user_name: str) -> List[Commit]:
        """
        Retrieve commits authored by a specific user.

        Args:
            user_name (str): Author's name.

        Returns:
            List[Commit]: List of tuples containing commit objects.
        """
        try:
            commits = [
                commit
                for commit in self._repo.iter_commits()
                if commit.author.name == user_name
            ]
            return commits
        except GitCommandError as e:
            logging.error(f"Failed to fetch commits by user '{user_name}': {e}")
            return []

    def get_branches(self) -> List[str]:
        """
        Returns a list of all branches in the repository.

        Returns:
            List[str]: A list of branch names.
        """
        try:
            return [branch.name for branch in self._repo.branches]
        except Exception as e:
            logging.error(f"Failed to retrieve branches: {e}")
            return []

    def get_repo_stats(self) -> Dict[str, int]:
        """
        Provides general repository statistics.

        Returns:
            Dict[str, int]: A dictionary containing stats.
                - 'commit_count': Total number of commits.
                - 'branch_count': Total number of branches.
        """
        try:
            commit_count = sum(1 for _ in self._repo.iter_commits())
            branch_count = len(self._repo.branches)
            return {
                "commit_count": commit_count,
                "branch_count": branch_count,
            }
        except Exception as e:
            logging.error(f"Failed to retrieve repository statistics: {e}")
            return {"commit_count": 0, "branch_count": 0}

    def get_commit_by_id(self, hex: str):
        return self._repo.commit(hex)

    def get_files_affected(self, hex: str):
        commit = self.get_commit_by_id(hex=hex)
        return commit.stats.files

    def get_diff_for_file(self, hex: str, file_path: str):
        """
        Get the diff for a specific file in a given commit.

        Args:
            hex (str) : Commit hash.
            file_path (str) : Path to the file to get the diff for.
        Returns:
             str: A string containing the diff.
        """
        commit = self.get_commit_by_id(hex=hex)
        parent = commit.parents[0] if commit.parents else None

        if parent:
            diff_index = parent.diff(commit, paths=file_path, create_patch=True)
        else:
            diff_index = commit.diff(NULL_TREE, paths=file_path, create_patch=True)

        for diff in diff_index:
            if diff.a_path == file_path or diff.b_path == file_path:
                return diff.diff.decode("utf-8")

        return ""

    def fetch_commits_and_display(
        self, user: User
    ) -> list[tuple[str, str | bytes | None, int | None]] | None:
        """
        Fetches commits and prepares them for display.

        Args:
            user (str): user whose commits we should get

        Returns:
            List[tuple] | None: list of commit details for display or None if there are no reviews
        """
        commits = self.get_commits_by_user(user.username)

        if len(commits) == 0:
            return None

        return [
            (commit.hexsha, commit.message, commit.committed_date) for commit in commits
        ]


def validate_git_repository_url(url: str) -> None:
    """
    Validate Git repository URL format

    Args:
        url (str): Git repository URL

    Raises:
            InvalidGitURL: If the URL is invalid.
    """

    patterns = {
        "https": r"^https://.*\.git$",
        "ssh": r"^git@.*:.*\.git$",
        "git": r"^git://.*\.git$",
    }
    url = url.strip()

    if not url:
        raise InvalidGitURL("Empty URL")

    for _, pattern in patterns.items():
        if re.match(pattern, url):
            return

    raise InvalidGitURL("Invalid URL format")

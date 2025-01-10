import pytest

from services.git_service import InvalidGitURL, validate_git_repository_url


def test_valid_git_urls():
    """Test that valid Git URLs are accepted without raising exceptions."""
    valid_urls = [
        "https://github.com/user/repo.git",
        "git@github.com:user/repo.git",
        "https://github.com/zpqrtbnk/test-repo.git",
        "git@github.com:zpqrtbnk/test-repo.git"
    ]
    for url in valid_urls:
        assert validate_git_repository_url(url) is None


def test_invalid_git_urls():
    invalid_urls = [
        "gi@github.com:zpqrtbnk/test-repo.git",
        "http://example.com/repo.git",
        "https://github.com/user",
        "",
        "random_something"
    ]
    for url in invalid_urls:
        with pytest.raises(InvalidGitURL):
            validate_git_repository_url(url)
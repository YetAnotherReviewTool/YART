import pytest

from services.git_service import InvalidGitURL, validate_git_repository_url


@pytest.mark.parametrize(
    "url",
    [
        "https://github.com/user/repo.git",
        "git@github.com:user/repo.git",
        "https://github.com/zpqrtbnk/test-repo.git",
        "git@github.com:zpqrtbnk/test-repo.git",
    ]
)
def test_valid_git_urls(url):
    """Test that valid Git URLs are accepted without raising exceptions."""
    assert validate_git_repository_url(url) is None


@pytest.mark.parametrize(
    "url",
    [
        "gi@github.com:zpqrtbnk/test-repo.git",
        "http://example.com/repo.git",
        "https://github.com/user",
        "",
        "random_something",
    ],
)
def test_invalid_git_urls(url):
    with pytest.raises(InvalidGitURL):
        validate_git_repository_url(url)

# def test_repo_connection():
#     helper = RepositoryHelper("C:\\Users\\katri\\Desktop\\YART", False)
#     print(helper.get_repo_stats())

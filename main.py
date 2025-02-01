import userInterface
from config.settings import read_config
from services.git_service import RepositoryHelper


def init_repository(url: str, path: str):
    # TODO if there is no path, we panic
    # also if u run it the first time, it has to be True, so the repo will download
    helper = RepositoryHelper(path, False, url)

if __name__ == "__main__":
    url, path = read_config()
    init_repository(url, path)
    userInterface.main()

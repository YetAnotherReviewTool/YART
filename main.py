from models.DatabaseModelHelper import DatabaseHelper
import userInterface
from config.settings import read_config

from models.UserModel import User
from services.git_service import RepositoryHelper
from services.session_service import Session
from models.ReviewModel import Review


if __name__ == "__main__":
    url, path = read_config()
    if path is None:
        Session().set_first_time()
    else:
        Session().path = path
    Session().add_url(url)
    userInterface.main()

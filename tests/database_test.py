import pytest
import models
from models.UserModel import User
from models.database import Database
from models.DatabaseModelHelper import DatabaseHelper
from models.ReviewModel import Review
from models.CommentModel import Comment
from models.ReviewParticipantModel import ReviewParticipant

@pytest.fixture(scope="session")
def mock_db():
	db = Database("mock.db")
	print("mock db opened")
	db.create_tables()
	return db

@pytest.mark.parametrize("user", [User.new("test1", "test1", True), User.new("test2", "test2", False), User.new("test3", "test3", False)])
def test_insert_users(mock_db: Database, user):
	assert mock_db.insertUser(user)

def test_get_user_by_id(mock_db: Database, ):
	user = mock_db.getUserByID(1)
	assert user.username == "test1"
	assert user.admin

def test_getBy_curry(mock_db: Database, ):
	user = mock_db.getBy(User)("username", "test1")
	assert user.username == "test1"
	assert user.admin


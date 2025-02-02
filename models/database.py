import sqlite3

from models.CommentModel import Comment
from models.ReviewModel import Review
from models.UserModel import User
from models.ReviewParticipantModel import ReviewParticipant, ParticipantRole

DEFAULT_DB_PATH = "database.db"

class Database:
	def __init__(self, db_path: str | None = None):
		if db_path is None:
			db_path = DEFAULT_DB_PATH
		self.conn = sqlite3.connect(db_path)
		self.cursor = self.conn.cursor()
		self.cursor.execute("PRAGMA foreign_keys = ON")

	def create_tables(self):
	
		self.cursor.execute(f"""

CREATE TABLE IF NOT EXISTS roles (
	roleID INTEGER PRIMARY KEY,
	name TEXT NOT NULL
)""")
		self.cursor.execute(f"""
CREATE TABLE IF NOT EXISTS statuses (
	statusID INTEGER PRIMARY KEY,
	name TEXT NOT NULL
)""")
		self.cursor.execute(f"""			  
CREATE TABLE IF NOT EXISTS users (
	userID INTEGER PRIMARY KEY,
	username TEXT NOT NULL,
	email TEXT NOT NULL,
	salt TEXT NOT NULL,
	password_hash TEXT NOT NULL,
	admin BOOLEAN NOT NULL
)""")
		self.cursor.execute(f"""
CREATE TABLE IF NOT EXISTS reviews (
	reviewID INTEGER PRIMARY KEY,
	title TEXT,
	description TEXT,
	status TEXT NOT NULL,
	file_path TEXT NOT NULL,
	creation_date DATE NOT NULL,
	creatorID INTEGER NOT NULL,
	FOREIGN KEY(creatorID) REFERENCES users(userID)
)""")
		self.cursor.execute(f"""
CREATE TABLE IF NOT EXISTS review_participants (
	reviewID INTEGER NOT NULL,
	userID INTEGER NOT NULL,
	role TEXT NOT NULL,
	PRIMARY KEY (reviewID, userID),
	FOREIGN KEY(reviewID) REFERENCES reviews(reviewID),
	FOREIGN KEY(userID) REFERENCES users(userID)
)""")
		self.cursor.execute(f"""
CREATE TABLE IF NOT EXISTS comments (
	commentID INTEGER PRIMARY KEY,
	reviewID INTEGER NOT NULL,
	authorID INTEGER NOT NULL,
	content TEXT NOT NULL,
	timestamp DATE NOT NULL,
	FOREIGN KEY(reviewID) REFERENCES reviews(reviewID),
	FOREIGN KEY(authorID) REFERENCES users(userID)
)""")
		self.cursor.execute(f"""
CREATE TABLE IF NOT EXISTS commits (
	commitID INTEGER PRIMARY KEY,
	reviewID INTEGER NOT NULL,
	FOREIGN KEY(reviewID) REFERENCES reviews(reviewID)
)""")
	
	def commit(self):
		self.conn.commit()
	
	def rollback(self):
		self.conn.rollback()
	
	def close(self):
		self.__del__()

	def __del__(self):

		self.conn.close()
import sqlite3
from typing import Callable

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
	fileLink TEXT NOT NULL,
	creationDate DATE NOT NULL,
	creatorId INTEGER NOT NULL,
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
		return
	



	def __init__(self, db_path: str | None = None):
		if db_path is None:
			db_path = DEFAULT_DB_PATH
		self.conn = sqlite3.connect(db_path)
		self.cursor = self.conn.cursor()
		self.cursor.execute("PRAGMA foreign_keys = ON")


	### Some funny method but might be too hard to make it work
	# basically Database.get(Comment).by("reviewID", 1)
	# and Database.get(User).by("username", "Mateusz")


	def getBy(self, model_class: type) -> Callable[[str], object]:
		def by(field: str, value,  **params):
			table_name = f"{self.model.__name__.lower()}s"
			condition = f"{field} = ?"
			placeholders = [value]
			
			# Handle potential multiple conditions
			if params:
				additional_conditions = [f"{key} = ?" for key, val in params.items()]
				condition = f"{condition} AND {' AND '.join(additional_conditions)}"
				placeholders.extend([val for val in params.values()])
			
			query = f"SELECT * FROM {table_name} WHERE {condition}"
			
			self.cursor.execute(query, placeholders)
			results = self.cursor.fetchall()
			
			if results:
				outputs = []
				if model_class is User:
					for result in results:
						join1 = [review[0] for review in self.cursor.execute(f"SELECT reviewID FROM review_participants WHERE userID = {result[0]}").fetchall()]
						outputs.append(User(userID=result[0], username=result[1], password_hash=result[2], admin=result[3], reviews=join1))

				elif model_class is Review:
					for result in results:
						join1 = [user[0] for user in self.cursor.execute(f"SELECT userID FROM review_participants WHERE reviewID = {result[0]}").fetchall()]
						outputs.append(Review(reviewID=result[0], title=result[1], description=result[2], status=result[3], fileLink=result[4], creationDate=result[5], authorId=result[6], reviewParticipants=join1))
						# TODO: how to get commits here

				elif model_class is Comment:
					outputs = [Comment(commentID=result[0], reviewID=result[1], authorID=result[2], content=result[3], timestamp=result[4]) for result in results]
				elif model_class is ReviewParticipant:
					outputs = [ReviewParticipant(reviewID=result[0], userID=result[1], role=result[2]) for result in results]
				else:
					outputs = [model_class(*result) for result in results]

				return outputs
			else:
				return None
		
		return by
		
	def getUserByID(self, userID: int) -> User:
		self.cursor.execute(f"SELECT userID, username, password_hash, admin FROM users WHERE userID = {userID}")
		user = User(*self.cursor.fetchone())
		self.cursor.execute(f"SELECT reviewID FROM reviews WHERE creatorID = {userID}")
		user.reviews = [review[0] for review in self.cursor.fetchall()]
		return user
	
	def getUserByUsername(self, username: str) -> User:
		self.cursor.execute(f"SELECT userID, username, password_hash, admin FROM users WHERE username = '{username}'")
		user = User(*self.cursor.fetchone())
		self.cursor.execute(f"SELECT reviewID FROM reviews WHERE creatorID = {user.userID}")
		user.reviews = [review[0] for review in self.cursor.fetchall()]
		return user
	
	def getReviewByID(self, reviewID: int) -> Review:
		data = self.cursor.execute(f"""SELECT 
							reviewID 
							title 
							description
							status 
							file_path 
							creation_date 
							creatorID 
					 	FROM reviews 
					  	WHERE reviewID = {reviewID}""")
		join1 = self.cursor.execute(f"SELECT")
		review = Review(*self.cursor.fetchone(), commitId=[])
		return review

	
	 
	def commit(self):
		self.conn.commit()
	
	def test(self):
		a = self.getBy(Review)("reviewID", 1)
	def rollback(self):
		self.conn.rollback()
	
	def close(self):
		self.__del__()

	def __del__(self):

		self.conn.close()
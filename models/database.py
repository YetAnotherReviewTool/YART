import logging
import sqlite3
from typing import Callable

from typing import List

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
	
	


	### Some funny method but might be too hard to make it work
	# basically Database.get(Comment).by("reviewID", 1)
	# and Database.get(User).by("username", "Mateusz")


	# def getBy(self, model_class: type) -> Callable[[str], object]:
	# 	def by(field: str, value,  **params):
	# 		table_name = f"{self.model.__name__.lower()}s"
	# 		condition = f"{field} = ?"
	# 		placeholders = [value]
			
	# 		# Handle potential multiple conditions
	# 		if params:
	# 			additional_conditions = [f"{key} = ?" for key, val in params.items()]
	# 			condition = f"{condition} AND {' AND '.join(additional_conditions)}"
	# 			placeholders.extend([val for val in params.values()])
			
	# 		query = f"SELECT * FROM {table_name} WHERE {condition}"
			
	# 		self.cursor.execute(query, placeholders)
	# 		results = self.cursor.fetchall()
			
	# 		if results:
	# 			outputs = []
	# 			if model_class is User:
	# 				for result in results:
	# 					join1 = [review[0] for review in self.cursor.execute(f"SELECT reviewID FROM review_participants WHERE userID = {result[0]}").fetchall()]
	# 					outputs.append(User(userID=result[0], username=result[1], password_hash=result[2], admin=result[3], reviews=join1))

	# 			elif model_class is Review:
	# 				for result in results:
	# 					join1 = [user[0] for user in self.cursor.execute(f"SELECT userID FROM review_participants WHERE reviewID = {result[0]}").fetchall()]
	# 					outputs.append(Review(reviewID=result[0], title=result[1], description=result[2], status=result[3], fileLink=result[4], creationDate=result[5], authorId=result[6], reviewParticipants=join1))
	# 					# TODO: how to get commits here

	# 			elif model_class is Comment:
	# 				outputs = [Comment(commentID=result[0], reviewID=result[1], authorID=result[2], content=result[3], timestamp=result[4]) for result in results]
	# 			elif model_class is ReviewParticipant:
	# 				outputs = [ReviewParticipant(reviewID=result[0], userID=result[1], role=result[2]) for result in results]
	# 			else:
	# 				outputs = [model_class(*result) for result in results]

	# 			return outputs
	# 		else:
	# 			return None
		
	# 	return by
	
	# def getUserByID(self, userID: int) -> User:
	# 	self.cursor.execute(f"SELECT userID, username, password_hash, admin FROM users WHERE userID = {userID}")
	# 	user = User(*self.cursor.fetchone())
	# 	self.cursor.execute(f"SELECT reviewID FROM reviews WHERE creatorID = {userID}")
	# 	user.reviews = [review[0] for review in self.cursor.fetchall()]
	# 	return user
	
	# def getUserByUsername(self, username: str) -> User:
	# 	self.cursor.execute(f"SELECT userID, username, password_hash, admin FROM users WHERE username = '{username}'")
	# 	user = User(*self.cursor.fetchone())
	# 	self.cursor.execute(f"SELECT reviewID FROM reviews WHERE creatorID = {user.userID}")
	# 	user.reviews = [review[0] for review in self.cursor.fetchall()]
	# 	return user
	
	# def getReviewByID(self, reviewID: int) -> Review:
	# 	data = self.cursor.execute(f"""SELECT 
	# 						reviewID 
	# 						title 
	# 						description
	# 						status 
	# 						file_path 
	# 						creation_date 
	# 						creatorID 
	# 				 	FROM reviews 
	# 				  	WHERE reviewID = {reviewID}""").fetchone()
	# 	join1 = [reviewer[0] for reviewer in self.cursor.execute(f"SELECT userID FROM review_participants WHERE reviewID = {reviewID}").fetchall()]
	# 	review = Review(reviewID=data[0], title=data[1], description=data[2], status=data[3], fileLink=data[4], creationDate=data[5], authorId=data[6], reviewParticipants=join1, commitId=[])
	# 	return review
	
	# def getReviewByTitle(self, title: str) -> Review:
	# 	data = self.cursor.execute(f"""SELECT 
	# 						reviewID 
	# 						title 
	# 						description
	# 						status 
	# 						file_path 
	# 						creation_date 
	# 						creatorID 
	# 				 	FROM reviews 
	# 				  	WHERE title = '{title}'""").fetchone()
	# 	join1 = [reviewer[0] for reviewer in self.cursor.execute(f"SELECT userID FROM review_participants WHERE reviewID = {data[0]}").fetchall()]
	# 	review = Review(reviewID=data[0], title=data[1], description=data[2], status=data[3], fileLink=data[4], creationDate=data[5], authorId=data[6], reviewParticipants=join1, commitId=[])
	# 	return review

	# def getCommentByID(self, reviewID: int) -> Comment:
	# 	data = self.cursor.execute(f"SELECT commentID, reviewID, authorID, content, timestamp FROM comments WHERE reviewID = {reviewID}").fetchone()
	# 	return Comment(commentID=data[0], reviewID=data[1], authorID=data[2], content=data[3], timestamp=data[4])

	# def getCommentsByReviewID(self, reviewID: int) -> List[Comment]:
	# 	data = self.cursor.execute(f"SELECT commentID, reviewID, authorID, content, timestamp FROM comments WHERE reviewID = {reviewID}").fetchall()
	# 	return [Comment(commentID=data[0], reviewID=data[1], authorID=data[2], content=data[3], timestamp=data[4]) for data in data]
	# def getReviewParticipants(self, reviewID: int) -> List[ReviewParticipant]:
	# 	data = self.cursor.execute(f"SELECT userID, role FROM review_participants WHERE reviewID = {reviewID}").fetchall()
	# 	return [ReviewParticipant(reviewID=reviewID, userID=userID, role=role) for userID, role in data]
	
	# def getReviewsByUserID(self, userID: int) -> List[Review]:
	# 	data = self.cursor.execute(f"SELECT reviewID FROM review_participants WHERE userID = {userID}").fetchall()
	# 	return [self.getReviewByID(reviewID) for reviewID in data]
	
	# def insertUser(self, user: User):
	# 	self.cursor.execute(f"INSERT INTO users (userID, username, salt, password_hash, admin) VALUES ({user.userID}, '{user.username}', '{user.salt}', '{user.password_hash}', {user.admin})")
	# 	self.commit()

	def getRowsFromTable(self, tableName: str) -> list:
		self.conn.row_factory = sqlite3.Row
		cursor = self.conn.cursor()
		
		query = f"SELECT * FROM {tableName}"
		cursor.execute(query)
		rows = cursor.fetchall()
		
		return [dict(row) for row in rows]


	def getRowsFromTableQuery(self, tableName: str, parameter: str, parameterValue: str) -> list:
		self.conn.row_factory = sqlite3.Row
		cursor = self.conn.cursor()
		
		query = f"SELECT * FROM {tableName} WHERE {parameter} = ?"
		cursor.execute(query, (parameterValue,))
		rows = cursor.fetchall()
		
		return [dict(row) for row in rows]
	
	def getRowsFromTableQueries(self, tableName: str, parameters: list[str], parameterValues: list[str]) -> list:
		self.conn.row_factory = sqlite3.Row
		cursor = self.conn.cursor()
		
		conditions = " AND ".join([f"{param} = ?" for param in parameters])
		query = f"SELECT * FROM {tableName} WHERE {conditions}"
		cursor.execute(query, parameterValues)
		rows = cursor.fetchall()
		
		return [dict(row) for row in rows]
	
	
	def commit(self):
		self.conn.commit()
	
	def rollback(self):
		self.conn.rollback()
	
	def close(self):
		self.__del__()

	def __del__(self):

		self.conn.close()

	def insertTestData(self):			
		self.cursor.execute("""
		INSERT INTO users (userID, username, salt, passworD_hash, admin)
		SELECT 1, 'test_user', "asd", "asd", true WHERE NOT EXISTS (SELECT 1 FROM users WHERE userID = 1)
		""")
			
		self.cursor.execute("""
		INSERT INTO reviews (title, description, status, fileLink, creationDate, creatorId)
		VALUES (?, ?, ?, ?, ?, ?)
		""", ("Sample Title", "Sample Description", "Pending", "http://example.com", "2024-02-02", 1))
		


db = Database()
db.create_tables()
db.insertTestData()
print(db.getRowsFromTable("reviews"))


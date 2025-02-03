import os
import sqlite3


DEFAULT_DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "database.db")

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
	commitId TEXT NOT NULL,
	authorId INTEGER NOT NULL,
	FOREIGN KEY(authorId) REFERENCES users(userID)
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

	TABLE_NAME_MAP = {
		"Comment": "comments",
		"User": "users",
		"ReviewParticipant": "review_participants",
		"Review": "reviews"
	}

	def insertIntoTable(self, tableName: str,  jsonFormInstance: object):
		columns = ", ".join(jsonFormInstance.keys())
		placeholders = ", ".join(["?" for _ in jsonFormInstance.keys()])
		values = tuple(jsonFormInstance.values())

		sql = f"INSERT INTO {Database.TABLE_NAME_MAP[tableName]} ({columns}) VALUES ({placeholders})"

		# Execute the SQL query
		cursor = self.cursor
		cursor.execute(sql, values)
		self.conn.commit()
		


	def getRowsFromTable(self, tableName: str) -> list:
		self.conn.row_factory = sqlite3.Row
		cursor = self.conn.cursor()
		
		query = f"SELECT * FROM {Database.TABLE_NAME_MAP[tableName]}"
		cursor.execute(query)
		rows = cursor.fetchall()
		
		return [dict(row) for row in rows]


	def getRowsFromTableQuery(self, tableName: str, parameter: str, parameterValue: str) -> list:
		self.conn.row_factory = sqlite3.Row
		cursor = self.conn.cursor()
		
		query = f"SELECT * FROM {Database.TABLE_NAME_MAP[tableName]} WHERE {parameter} = ?"
		cursor.execute(query, (parameterValue,))
		rows = cursor.fetchall()
		
		return [dict(row) for row in rows]
	
	def getRowsFromTableQueries(self, tableName: str, parameters: list[str], parameterValues: list[str]) -> list:
		self.conn.row_factory = sqlite3.Row
		cursor = self.conn.cursor()
		
		conditions = " AND ".join([f"{param} = ?" for param in parameters])
		query = f"SELECT * FROM {Database.TABLE_NAME_MAP[tableName]} WHERE {conditions}"
		cursor.execute(query, parameterValues)
		rows = cursor.fetchall()
		
		return [dict(row) for row in rows]
	
	def getValuesFromTable(self, tableName: str, column: str, parameter: str, parameterValue: str):
		cursor = self.conn.cursor()

		query = f"SELECT {column} FROM {Database.TABLE_NAME_MAP[tableName]} WHERE {parameter} = ?"
		cursor.execute(query, (parameterValue,))
		results = cursor.fetchall()

		return [row[0] for row in results]



	def getPrimaryKeyColumnName(self, model: type) -> str:
		"""
        Returns the primary key column name for the table of the given model.
        """
		table_name = self.TABLE_NAME_MAP.get(model.__name__)
		query = f"PRAGMA table_info({table_name})"

		self.cursor.execute(query)
		columns = self.cursor.fetchall()

		for col in columns:
			if col[5] == 1:
				return col[1]
		raise ValueError(f"No primary key found for model {model.__name__}")

	def updateDbRow(self, model: type, primaryKeyValue: int, parameterToChange: str, parameterValue: object):
		"""
        Update the column value for a selected row given by the primary key.
        """
		primary_key_column = self.getPrimaryKeyColumnName(model)
		table_name = self.TABLE_NAME_MAP.get(model.__name__)
		query = f"UPDATE {table_name} SET {parameterToChange} = {parameterValue} WHERE {primary_key_column} = {primaryKeyValue}"

		self.cursor = self.conn.cursor()
		self.cursor.execute(query)
		self.conn.commit()

	def getNextId(self, model: type) -> int:
		"""
        Finds the existing maximum id in the table for the given model and returns the next avaialable one.
        """
		primary_key = self.getPrimaryKeyColumnName(model)
		table_name = self.TABLE_NAME_MAP.get(model.__name__, model.__name__.lower() + 's')
		query = f"SELECT MAX({primary_key}) FROM {table_name}"

		self.cursor.execute(query)
		max_id = self.cursor.fetchone()[0]

		return (max_id or 0) + 1


	def getUniqueValueFromDb(self, model: type, primaryKey: int, parameter: str) -> object:
		"""
        Return the column value of the row specified by the primary key value.
        """
		primary_key_column = self.getPrimaryKeyColumnName(model)
		table_name = self.TABLE_NAME_MAP.get(model.__name__)
		query = f"SELECT * FROM {table_name} WHERE {primary_key_column} = {parameter}"

		self.cursor.execute(query)
		result = self.cursor.fetchone()

		if result:
			return result[0]
		else:
			raise ValueError(f"No record found for {model.__name__} with {primary_key_column}={primaryKey}")

	def commit(self):
		self.conn.commit()

	def rollback(self):
		self.conn.rollback()
	
	def close(self):
		self.__del__()

	def __del__(self):

		self.conn.close()

if __name__ == "__main__":
	db = Database()
	db.create_tables()
	db.cursor.execute("SELECT * FROM sqlite_schema")
	print(db.cursor.fetchall())

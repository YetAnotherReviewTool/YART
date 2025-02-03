from datetime import datetime

from models.database_new import Database as DB


class DatabaseHelper:
    DBInstance = DB("database.db")
    """
    Class with generic methods to handle creating Models from DB and inserting into the DB based on the existing models
    """

    def modelToDbName(model) -> str:
        return model.__name__

    def getRowsFromDb(model: type) -> list[dict]:
        return DatabaseHelper.DBInstance.getRowsFromTable(DatabaseHelper.modelToDbName(model))

    def getRowsFromDbQuery(model: type, parameter: str, parameterValue: object) -> dict:
        return DatabaseHelper.DBInstance.getRowsFromTableQuery(DatabaseHelper.modelToDbName(model), parameter,
                                                               parameterValue)

    def getRowsFromDbQueries(model: type, parameters: list[str], parameterValues: list[object]) -> dict:
        return DatabaseHelper.DBInstance.getRowsFromTableQueries(DatabaseHelper.modelToDbName(model), parameters,
                                                                 parameterValues)

    def getRowFromDbByPrimaryKey(model: type, primaryKey: int):
        """
        Returns a single, unique row based on primary key.
        """
        return DatabaseHelper.getRowsFromDbQuery(model, DatabaseHelper.getPrimaryKeyColumnName(model), primaryKey)

    def getRowFromDbByCompositeKey(model: type, primaryKeyVals: list[int]):
        """
        Returns a single, unique row based on primary key.
        Designed for compound key input to handle ReviewParticipant
        """

        return DatabaseHelper.getRowsFromDbQueries(model, DatabaseHelper.getCompositePrimaryKeyColumnNames(model),
                                                   primaryKeyVals)

    def getModelsFromDb(model: type) -> list:
        """
        Return all review from the database. Not sure if useful. Felt cute, might delete later
        """
        # czekam na endpointy ale zakldam teraz ze to bedzie dict jsonwy gdzie klucze to kolumny #TODO
        rows = DatabaseHelper.getRowsFromDb(DatabaseHelper.modelToDbName(model)).values()
        return [model(*entry.values()) for entry in rows]

    def getModelsFromDbQuery(model: type, parameter: str, parameterValue: object) -> list:
        """
        Returns queried reviews from the database. Basically returns:
        SELECT * FROM ModelDb WHERE parameter = parameterValue
        and converts all rows to Models
        """

        rows = DatabaseHelper.getRowsFromDbQuery(DatabaseHelper.modelToDbName(model), parameter,
                                                 parameterValue).values()
        return [model(*entry.values()) for entry in rows]

    def getModelsFromDbQueries(model: type, parameters: list[str], parameterValues: list[object]) -> list:
        """
        Returns queried reviews from the database. Basically returns:
        SELECT * FROM ModelDb WHERE parameter1 = parameterValue1 AND  parameter2 = parameterValue2 ...
        and converts all rows to Models
        """

        rows = DatabaseHelper.getRowsFromDbQueries(DatabaseHelper.modelToDbName(model), parameters,
                                                   parameterValues).values()
        return [model(*entry.values()) for entry in rows]

    def insertIntoDbFromModel(model: type, instance: object) -> None:
        """
        Inserts a new row into the database for a given model.
        """
        dictForm = {key: value for key, value in instance.__dict__.items()}

        DatabaseHelper.DBInstance.insertIntoTable(DatabaseHelper.modelToDbName(model), dictForm)

    def updateDbRow(model: type, primaryKeyValue: int, parameterToChange: str, parameterValue: object):
        return DatabaseHelper.DBInstance.updateDbRow(model, primaryKeyValue, parameterToChange, parameterValue)

    def getNextId(model: type) -> int:
        return DatabaseHelper.DBInstance.getNextId(model)

    def getPrimaryKeyColumnName(model: type) -> str:
        return DatabaseHelper.DBInstance.getPrimaryKeyColumnName(model)

    def getCompositePrimaryKeyColumnNames(model: type) -> list[str]:
        return DatabaseHelper.getCompositePrimaryKeyColumnNames(model)

    def getUniqueValueFromDb(model: type, primaryKey: int, parameter: str) -> object:
        """
        Return the column value of the row specified by the primary key value.
        """

        return DatabaseHelper.getRowFromDbByPrimaryKey(model, primaryKey)[parameter]

    def get_reviews(self) -> list:

        reviews_data = DatabaseHelper.DBInstance.getRowsFromTable("Review")
        reviews = []

        for row in reviews_data:
            from models.ReviewModel import Review
            from models.ReviewModel import ReviewStatus
            reviews.append(Review(
                reviewID=row["reviewID"],
                authorId=row["creatorId"],
                title=row["title"],
                description=row["description"],
                status=ReviewStatus[row["status"]],
                fileLink=row["fileLink"],
                creationDate=datetime.datetime.strptime(row["creationDate"], "%Y-%m-%d")
            ))

        return reviews

    def get_users(self) -> list:
        users_data = DatabaseHelper.DBInstance.getRowsFromTable("User")
        users = []

        for row in users_data:
            from models.UserModel import User
            users.append(User(
                userID=row["userID"],
                username=row["username"],
                password_hash=row["password_hash"],
                salt=row["salt"],
                admin=bool(row["admin"])
            ))

        return users

    def get_review_participants(self) -> list:
        participants_data = DatabaseHelper.DBInstance.getRowsFromTable("ReviewParticipant")
        participants = []

        for row in participants_data:
            from models.ReviewParticipantModel import ReviewParticipant, ParticipantRole, ParticipantStatus
            participants.append(ReviewParticipant(
                userID=row["userID"],
                reviewID=row["reviewID"],
                role=ParticipantRole[row["role"]],
                isAccepted=ParticipantStatus.IN_PROGRESS  # Default status if not stored explicitly
            ))

        return participants

    def get_comments(self) -> list:
        comments_data = DatabaseHelper.DBInstance.getRowsFromTable("Comment")
        comments = []

        for row in comments_data:
            from models.CommentModel import Comment
            comments.append(Comment(
                commentId=row["commentID"],
                reviewID=row["reviewID"],
                authorID=row["authorID"],
                content=row["content"],
                timestamp=datetime.strptime(row["timestamp"], "%Y-%m-%d")
            ))

        return comments

    def fill_relations(self, reviews, users, review_participants):
        pass
        # TODO should i do it? 

    def insert_reviews(self, reviews: list):
        for review in reviews:
            review_data = {
                "reviewID": review.reviewID,
                "title": review.title,
                "description": review.description,
                "status": review.status.name,
                "fileLink": review.fileLink,
                "creationDate": review.creationDate.strftime("%Y-%m-%d"),
                "creatorId": review.authorId
            }
            DatabaseHelper.DBInstance.insertIntoTable("Review", review_data)

    def insert_users(self, users: list):
        for user in users:
            user_data = {
                "userID": user.userID,
                "username": user.username,
                "salt": user.salt,
                "password_hash": user.password_hash,
                "admin": int(user.admin)
            }
            DatabaseHelper.DBInstance.insertIntoTable("User", user_data)

    def insert_review_participants(self, participants: list):
        for participant in participants:
            participant_data = {
                "reviewID": participant.reviewID,
                "userID": participant.userID,
                "role": participant.role.name
            }
            DatabaseHelper.DBInstance.insertIntoTable("ReviewParticipant", participant_data)

    def insert_comments(self, comments: list):
        for comment in comments:
            comment_data = {
                "commentID": comment.commentId,
                "reviewID": comment.reviewID,
                "authorID": comment.authorID,
                "content": comment.content,
                "timestamp": comment.timestamp.strftime("%Y-%m-%d")
            }
            DatabaseHelper.DBInstance.insertIntoTable("Comment", comment_data)

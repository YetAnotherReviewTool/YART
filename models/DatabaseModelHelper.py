from models.database_new import Database as DB
from models.model import Model

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
        return DatabaseHelper.DBInstance.getRowsFromTableQuery(DatabaseHelper.modelToDbName(model), parameter, parameterValue)

    def getRowsFromDbQueries(model: type, parameters: list[str], parameterValues: list[object]) -> dict:
        return DatabaseHelper.DBInstance.getRowsFromTableQueries(DatabaseHelper.modelToDbName(model),parameters, parameterValues)

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

        return DatabaseHelper.getRowsFromDbQueries(model, DatabaseHelper.getCompositePrimaryKeyColumnNames(model), primaryKeyVals)


    def getModelsFromDb(model: type) -> list:
        """
        Return all review from the database. Not sure if useful. Felt cute, might delete later
        """
        # czekam na endpointy ale zakldam teraz ze to bedzie dict jsonwy gdzie klucze to kolumny #TODO
        rows = DatabaseHelper.getRowsFromDb(model)
        return model.constructFromDbData(rows)
    
    def getModelsFromDbQuery(model: Model, parameter: str, parameterValue: object) -> list:
        """
        Returns queried reviews from the database. Basically returns:
        SELECT * FROM ModelDb WHERE parameter = parameterValue
        and converts all rows to Models
        """

        rows = DatabaseHelper.getRowsFromDbQuery(model, parameter, parameterValue)
        return model.constructFromDbData(rows)
    
    def getModelsFromDbQueries(model: Model, parameters: list[str], parameterValues: list[object]) -> list:
        """
        Returns queried reviews from the database. Basically returns:
        SELECT * FROM ModelDb WHERE parameter1 = parameterValue1 AND  parameter2 = parameterValue2 ...
        and converts all rows to Models
        """

        rows = DatabaseHelper.getRowsFromDbQueries(model, parameters, parameterValues)
        return model.constructFromDbData(rows)

    
    def insertIntoDbFromModel(model: type, instance: Model) -> None:
        """
        Inserts a new row into the database for a given model.
        """
        dictForm = instance.jsonify()

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


    # def get_review_participants(db: Database) -> list[ReviewParticipant]:
    #     participants_data = db.getRowsFromTable("ReviewParticipant")
    #     participants = []

    #     for row in participants_data:
    #         participants.append(ReviewParticipant(
    #             userID=row["userID"],
    #             reviewID=row["reviewID"],
    #             role=ParticipantRole[row["role"]],
    #             isAccepted=ParticipantStatus.IN_PROGRESS  # Default status if not stored explicitly
    #         ))

    #     return participants

    # def get_comments(db: Database) -> list[Comment]:
    #     comments_data = db.getRowsFromTable("Comment")
    #     comments = []

    #     for row in comments_data:
    #         comments.append(Comment(
    #             commentId=row["commentID"],
    #             reviewID=row["reviewID"],
    #             authorID=row["authorID"],
    #             content=row["content"],
    #             timestamp=datetime.datetime.strptime(row["timestamp"], "%Y-%m-%d")
    #         ))

    #     return comments
    

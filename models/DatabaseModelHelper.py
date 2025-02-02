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
        rows = DatabaseHelper.getRowsFromDb(DatabaseHelper.modelToDbName(model)).values()
        return [model(*entry.values()) for entry in rows]
    
    def getModelsFromDbQuery(model: type, parameter: str, parameterValue: object) -> list:
        """
        Returns queried reviews from the database. Basically returns:
        SELECT * FROM ModelDb WHERE parameter = parameterValue
        and converts all rows to Models
        """

        rows = DatabaseHelper.getRowsFromDbQuery(DatabaseHelper.modelToDbName(model), parameter, parameterValue).values()
        return [model(*entry.values()) for entry in rows]
    
    def getModelsFromDbQueries(model: type, parameters: list[str], parameterValues: list[object]) -> list:
        """
        Returns queried reviews from the database. Basically returns:
        SELECT * FROM ModelDb WHERE parameter1 = parameterValue1 AND  parameter2 = parameterValue2 ...
        and converts all rows to Models
        """

        rows = DatabaseHelper.getRowsFromDbQueries(DatabaseHelper.modelToDbName(model), parameters, parameterValues).values()
        return [model(*entry.values()) for entry in rows]

    
    def insertIntoDbFromModel(model: type, instance: object) -> None:
        """
        Inserts a new row into the database for a given model.
        """
        dictForm = {key: value for key, value in instance.__dict__.items()}

        # do insert stuff when I get endpoints #TODO

        return dict

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
    

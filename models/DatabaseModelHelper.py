class DatabaseHelper:
    """
    Class with generic methods to handle creating Models from DB and inserting into the DB based on the existing models
    """

    def modelToDbName(model) -> str:
        return model.__name__

    def getRowsFromDb(model: type) -> dict:
        #mati pls #TODO
        
        pass

    def getRowsFromDbQuery(model: type, parameter: str, parameterValue: object) -> dict:
        #mati pls v2 #TODO

        pass

    def getRowFromDbByPrimaryKey(model: type, primaryKey: int):
        """
        Returns a single, unique row based on primary key.
        """
        return DatabaseHelper.getRowsFromDbQuery(model, DatabaseHelper.getPrimaryKeyColumnName(model), primaryKey)


    def getModelsFromDb(model: type) -> list:
        """
        Return all review from the database. Not sure if useful. Felt cute, might delete later
        """
        # czekam na endpointy ale zakldam teraz ze to bedzie dict jsonwy gdzie klucze to kolumny #TODO

        from models import ReviewModel
        rows = list(DatabaseHelper.getRowsFromDb(DatabaseHelper.modelToDbName(model)).values())
        return [model(*entry.values()) for entry in rows]
    
    def getModelsFromDbQuery(model: type, parameter: str, parameterValue: object) -> list:
        """
        Returns queried reviews from the database. Basically returns:
        SELECT * FROM ModelDb WHERE parameter = parameterValue
        and converts all rows to Models
        """

        # czekam na endpointy ale zakldam teraz ze to bedzie dict jsonwy gdzie klucze to kolumny
        from models import ReviewModel
        rows = list(DatabaseHelper.getRowsFromDb(DatabaseHelper.modelToDbName(model), parameter, parameterValue).values()) #query the DB
        return [model(*entry.values()) for entry in rows]

    
    def insertIntoDbFromModel(model: type, instance: object) -> None:
        """
        Inserts a new row into the database for a given model.
        """
        jsonForm = {key: value for key, value in instance.__dict__.items()}

        # do insert stuff when I get endpoints #TODO

        return jsonForm

    def updateDbRow(model: type, primaryKeyValue: int, parameterToChange: str, parameterValue: object):
        """
        Update the column value for a selected row given by the primary key.
        """

        pass #TODO

    def getNextId(model: type) -> int:
        """
        Finds the existing maximum id in the table for the given model and returns the next avaialable one.
        """
        pass #TODO

    def getPrimaryKeyColumnName(model: type) -> str:
        """
        Returns the primary key column name for the table of the given model.
        """
        pass #TODO

    def getUniqueValueFromDb(model: type, primaryKey: int, parameter: str) -> object:
        """
        Return the column value of the row specified by the primary key value.
        """

        return DatabaseHelper.getRowFromDbByPrimaryKey(model, primaryKey)[parameter]
    

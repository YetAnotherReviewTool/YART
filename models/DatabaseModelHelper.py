import CommentModel
import ReviewModel
import ReviewParticipantModel
import UserModel

class DatabaseHelper:
    """
    Class with generic methods to handle creating Models from DB and inserting into the DB based on the existing models
    """

    def modelToDbName(model) -> str:
        match model:
            case CommentModel.Comment:
                return "Comment"
            case ReviewParticipantModel.ReviewParticipant:
                return "ParticipantModel"
            case UserModel.User:
                return "User"
            case ReviewModel.Review:
                return "Review"

    def getRowsFromDb(model: type) -> dict:
        #mati pls
        
        pass

    def getRowsFromDbQuery(model: type, parameter: str, parameterValue: object) -> dict:
        #mati pls v2

        pass


    def getModelsFromDb(model: type) -> list:
        """
        Return all review from the database. Not sure if useful. Felt cute, might delete later
        """
        # czekam na endpointy ale zakldam teraz ze to bedzie dict jsonwy gdzie klucze to kolumny

        rows = list(DatabaseHelper.getRowsFromDb(DatabaseHelper.modelToDbName(model)).values())
        return [ReviewModel.Review(*entry.values()) for entry in rows]
    
    def getModelsFromDbQuery(model: type, parameter: str, parameterValue: object) -> list:
        """
        Returns queried reviews from the database. Basically returns:
        SELECT * FROM ModelDb WHERE parameter = parameterValue
        and converts all rows to Models
        """

        # czekam na endpointy ale zakldam teraz ze to bedzie dict jsonwy gdzie klucze to kolumny

        rows = list(DatabaseHelper.getRowsFromDb(DatabaseHelper.modelToDbName(model), parameter, parameterValue).values()) #query the DB
        return [ReviewModel.Review(*entry.values()) for entry in rows]

    
    def insertIntoDbFromModel(model: type, instance: object) -> None:
        jsonForm = {key: value for key, value in instance.__dict__.items()}

        # do insert stuff when I get endpoints

        return jsonForm

    def updateDbRow(model: type, primaryKeyValue: int, parameterToChange: str, parameterValue: object):
        pass #TODO
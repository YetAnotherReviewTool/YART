import datetime

class Comment:
    def __init__(self):
        self.reviewID: int
        self.authorID: int
        self.content: str
        self.timestamp: datetime.date

    def getFromDB(reviewID):
        pass #TODO

    def insertToDB(self):
        pass #TODO
        
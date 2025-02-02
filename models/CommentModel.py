import datetime

class Comment:
    def __init__(self, commentId, reviewID, authorID, content, timestamp=datetime.datetime.today()):
        self.commentId: int = commentId
        self.reviewID: int = reviewID
        self.authorID: int = authorID
        self.content: str = content
        self.timestamp: datetime.date = timestamp

    def __str__(self):
        return str(self.authorID) + " (" + str(self.timestamp) + ") " + ": " + self.content

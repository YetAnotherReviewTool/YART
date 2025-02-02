import datetime

class Comment:
    def __init__(self,commentID, reviewID, authorID, content, timestamp=datetime.datetime.today()):
        self.commentID: int = commentID
        self.reviewID: int = reviewID
        self.authorID: int = authorID
        self.content: str = content
        self.timestamp: datetime.date = timestamp

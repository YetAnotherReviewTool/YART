import datetime

class Comment:
    def __init__(self, reviewID, authorID, content, timestamp=datetime.datetime.today()):
        self.reviewID: int = reviewID
        self.authorID: int = authorID
        self.content: str = content
        self.timestamp: datetime.date = timestamp

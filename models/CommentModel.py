from datetime import datetime
from models.model import Model
from pydantic import BaseModel

class Comment(BaseModel, Model):
    commentID: int
    reviewID: int
    authorID: int
    content: str
    timestamp: datetime
    def __init__(self, commentID, reviewID, authorID, content, timestamp=datetime.now()):
        self.commentID: int = commentID
        self.reviewID: int = reviewID
        self.authorID: int = authorID
        self.content: str = content
        self.timestamp: datetime = timestamp

    def __str__(self):
        return str(self.authorID) + " (" + str(self.timestamp) + ") " + ": " + self.content


    def jsonify(self):
        return super().jsonify()
    
    def constructFromDbData(data):
        comments_data = data
        comments = []

        for row in comments_data:
            comments.append(Comment(
                commentID=row["commentID"],
                reviewID=row["reviewID"],
                authorID=row["authorID"],
                content=row["content"],
                timestamp=datetime.strptime(row["timestamp"], "%Y-%m-%d")
            ))

        return comments
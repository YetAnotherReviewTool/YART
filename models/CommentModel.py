import datetime
from models.model import Model

class Comment(Model):
    def __init__(self, commentID, reviewID, authorID, content, timestamp=datetime.datetime.today()):
        self.commentID: int = commentID
        self.reviewID: int = reviewID
        self.authorID: int = authorID
        self.content: str = content
        self.timestamp: datetime.date = timestamp

    def __str__(self):
        return str(self.authorID) + " (" + str(self.timestamp) + ") " + ": " + self.content

    def jsonify(self):
        return super().jsonify()
    
    def constructFromDbData(data):
        comments_data = data
        comments = []

        for row in comments_data:
            comments.append(Comment(
                commentId=row["commentID"],
                reviewID=row["reviewID"],
                authorID=row["authorID"],
                content=row["content"],
                timestamp=datetime.datetime.strptime(row["timestamp"], "%Y-%m-%d")
            ))

        return comments
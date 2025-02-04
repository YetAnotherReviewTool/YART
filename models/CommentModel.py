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
        dict = {
            "commentID": self.commentID,
            "reviewID": self.reviewID,
            "authorID": self.authorID,
            "content": self.content,
            "timestamp": self.timestamp.strftime("%Y-%m-%d")
        }
        print (dict)
        return dict
    
    def constructFromDbData(data):
        comments_data = data
        comments = []

        for row in comments_data:
            try:
                timestamp = datetime.datetime.strptime(row["timestamp"], "%Y-%m-%d %H:%M:%S")
            except ValueError:
                timestamp = datetime.datetime.strptime(row["timestamp"], "%Y-%m-%d")
            comments.append(Comment(
                commentID=row["commentID"],
                reviewID=row["reviewID"],
                authorID=row["authorID"],
                content=row["content"],
                timestamp=timestamp
            ))

        return comments
from pydantic import BaseModel
import models.CommentModel as CommentModel
import models.UserModel as UserModel
import models.ReviewParticipantModel as ReviewParticipantModel
from models.model import Model
from models.DatabaseModelHelper import DatabaseHelper
import enum
from datetime import datetime



class ReviewStatus(enum.Enum):
    IN_REVIEW = 1
    APPROVED = 2

class Review(BaseModel, Model):
    reviewID: int
    authorID: int
    title: str
    description: str
    status: ReviewStatus
    commitID: list[int]
    fileLink: str
    creationDate: datetime
    reviewParticipants: list[int]
    comments: list[int]
    def __init__(self,
                reviewID: int,
                authorID: int = -1,
                title: str = "",
                description: str = "",
                status = ReviewStatus.IN_REVIEW,
                commitID: list[int] = [],
                fileLink = "",
                creationDate = datetime.now(),
                reviewParticipants: list[int] = [],
                comments: list[int] = []
                ):
        
        self.reviewID: int = reviewID
        self.title: str = title
        self.description: str = description
        self.status: ReviewStatus = status
        self.commitID: list[int] = commitID
        self.fileLink: str = fileLink
        self.creationDate: datetime.datetime = creationDate
        self.authorID: int = authorID
        self.reviewParticipants: list[int] = reviewParticipants
        self.comments: list [int] = comments

    def assignReviewer(self, userID: int,
                       role: ReviewParticipantModel.ParticipantRole = ReviewParticipantModel.ParticipantRole.REVIEWER) -> None:
        """
            FR-02: Allow users to create reviews, add specific users and assign them roles
        """
        newParticipant = ReviewParticipantModel.ReviewParticipant(
            userID,
            role,
            ReviewParticipantModel.ParticipantStatus.IN_PROGRESS,
            []
        )

        DatabaseHelper.insertIntoDbFromModel(ReviewParticipantModel.ReviewParticipant, newParticipant)

        self.reviewParticipants.append(userID)
        DatabaseHelper.updateDbRow(Review, self.reviewID, "reviewParticipants", self.reviewParticipants)

    def seeComments(self) -> list:
        return DatabaseHelper.getModelsFromDbQuery(CommentModel.Comment, "reviewID", self.reviewID)
    
    def addComments(self, userID: int, comment):
        if userID not in self.reviewParticipants:
            from models import UserModel
            raise UserModel.AccessError

        DatabaseHelper.insertIntoDbFromModel(CommentModel.Comment, comment)
        self.comments.append(comment.commentID)

        DatabaseHelper.updateDbRow(Review, self.reviewID, "comments", self.comments)

    def evaluateReview(self) -> bool:
        """
        i'm going to assume the documentation is wrong on this one
        since I think sometime ago we agreed that a review is accepted
        when all ReviewParticipants accept it? so thats what imma do here
        """
        for reviewerID in self.reviewParticipants:

            participant = DatabaseHelper.getRowFromDbByPrimaryKey(ReviewParticipantModel.ReviewParticipant, reviewerID)
            if participant.status != ReviewParticipantModel.ParticipantStatus.ACCEPTED:
                return False

        self.status = ReviewStatus.APPROVED 
        return True
        
    def getReviewParticipantS(self) -> list:

        from models.DatabaseModelHelper import DatabaseHelper
        return DatabaseHelper.getModelsFromDbQuery(ReviewParticipantModel.ReviewParticipant, "reviewID", self.reviewID)
    
    def jsonify(self) -> dict:
        return {
            "reviewID": self.reviewID,
            "authorID": self.authorID,
            "title": self.title,
            "description": self.description,
            "status": self.status.value,
            "commitID": str(self.commitID),
            "fileLink": self.fileLink,
            "creationDate": self.creationDate.strftime("%Y-%m-%d"),
            "authorID": self.authorID
        }

    def constructFromDbData(data: list):
        reviews_data = data
        reviews = []

        for row in reviews_data:
            reviews.append(Review(
                row["reviewID"],
                authorID=row["authorID"],
                title=row["title"],
                description=row["description"],
                status=ReviewStatus(int(row["status"])),
                fileLink=row["fileLink"],
                creationDate=datetime.datetime.strptime(row["creationDate"], "%Y-%m-%d")
            ))

        return reviews

    
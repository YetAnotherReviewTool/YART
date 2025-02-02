import models.CommentModel as CommentModel
import models.UserModel as UserModel
import models.ReviewParticipantModel as ReviewParticipantModel
from models.DatabaseModelHelper import DatabaseHelper
import enum
import datetime



class ReviewStatus(enum.Enum):
    IN_REVIEW = enum.auto()
    APPROVED = enum.auto()

class Review:
    def __init__(self,
                reviewID: int,
                authorId: int = -1,
                title: str = "",
                description: str = "",
                status = ReviewStatus.IN_REVIEW,
                commitId = list(),
                fileLink = "",
                creationDate = datetime.datetime.today(),
                reviewParticipants: list[int] = [],
                comments: list[int] = []
                ):
        
        self.reviewID: int = reviewID
        self.title: str = title
        self.description: str = description
        self.status: ReviewStatus = status
        self.commitId: list[int] = commitId
        self.fileLink: str = fileLink
        self.creationDate: datetime.datetime = creationDate
        self.authorId: int = authorId
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
        return DatabaseHelper.getModelsFromDbQuery(CommentModel.Comment, "reviewID", self.reviewId)
    
    def addComments(self, userID: int, comment):
        if userID not in self.reviewParticipants:
            from models import UserModel
            raise UserModel.AccessError

        DatabaseHelper.insertIntoDbFromModel(CommentModel.Comment, comment)
        self.comments.append(comment.commentId)

        DatabaseHelper.updateDbRow(Review, self.reviewId, "comments", self.comments)

    def evaluateReview(self) -> bool:
        """
        i'm going to assume the documentation is wrong on this one
        since I think sometime ago we agreed that a review is accepted
        when all ReviewParticipants accept it? so thats what imma do here
        """
        for reviewerID in self.reviewParticipants:

            participant = ReviewParticipantModel.getFromDB(reviewerID)
            if participant.status != ReviewParticipantModel.ParticipantStatus.ACCEPTED:
                return False

        self.status = ReviewStatus.APPROVED 
        return True
        
    def getReviewParticipantS(self) -> list:

        from models.DatabaseModelHelper import DatabaseHelper
        return DatabaseHelper.getModelsFromDbQuery(ReviewParticipantModel.ReviewParticipant, "reviewId", self.reviewID)


    
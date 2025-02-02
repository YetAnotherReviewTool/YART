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
                reviewId: int,
                authorId: int = -1,
                title: str = "",
                description: str = "",
                status = ReviewStatus.IN_REVIEW,
                commitId = list(),
                fileLink = "",
                creationDate = datetime.datetime.today(),
                reviewParticipants: list[int] = []
                ):
        
        self.reviewId: int = reviewId
        self.title: str = title
        self.description: str = description
        self.status: ReviewStatus = status
        self.commitId: list[int] = commitId
        self.fileLink: str = fileLink
        self.creationDate: datetime.datetime = creationDate
        self.authorId: int = authorId
        self.reviewParticipants: list[int] = reviewParticipants

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
        DatabaseHelper.updateDbRow(Review, self.reviewId, "reviewParticipants", self.reviewParticipants)

    def seeComments(self) -> list[CommentModel.Comment]:
        allComments = []

        for participant in self.reviewParticipants:
            for comment in participant.getComments():
                allComments.append(comment)

        return allComments
    
    def addComments(self, userID: int, comment: CommentModel.Comment):
        if userID not in self.reviewParticipants:
            raise UserModel.AccessError
        
        DatabaseHelper.insertIntoDbFromModel(CommentModel.Comment, comment)

        #are we sure sure sure we want this here and not in ReviewParticipant??
        #cause i gotta do this weird thing now to update the comment id list in DB

        participantComments = DatabaseHelper.getModelsFromDbQuery(ReviewParticipantModel, "userId", userID).comments
        DatabaseHelper.updateDbRow(ReviewParticipantModel.ReviewParticipant, userID, "comments", participantComments.append(comment.authorID))

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
        
    def getReviewParticipantS(self) -> list[ReviewParticipantModel.ReviewParticipant]:
        return DatabaseHelper.getModelsFromDbQuery(ReviewParticipantModel.ReviewParticipant, "reviewId", self.reviewId)


    
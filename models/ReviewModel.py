import models.CommentModel as CommentModel
import models.UserModel as UserModel
import models.ReviewParticipantModel as ReviewParticipantModel
from models.model import Model
from models.DatabaseModelHelper import DatabaseHelper
import enum
import datetime



class ReviewStatus(enum.Enum):
    IN_REVIEW = 1
    APPROVED = 2

class Review(Model):
    def __init__(self,
                reviewId: int,
                authorId: int = -1,
                title: str = "",
                description: str = "",
                status = ReviewStatus.IN_REVIEW,
                commitId: list[int] = [],
                fileLink = "",
                creationDate = datetime.datetime.today(),
                ):
        
        self.reviewId: int = reviewId
        self.title: str = title
        self.description: str = description
        self.status: ReviewStatus = status
        self.commitId: list[int] = commitId
        self.fileLink: str = fileLink
        self.creationDate: datetime.datetime = creationDate
        self.authorId: int = authorId
        self.reviewParticipantsUserIDs: list[int] = DatabaseHelper.getValuesFromDb(ReviewParticipantModel.ReviewParticipant, "userID", "reviewID", self.reviewId)
        self.comments: list [int] = DatabaseHelper.getValuesFromDb(CommentModel.Comment,
                                                                   "commentID", "reviewID", self.reviewId)

    def assignReviewer(self, userID: int,
                       role: ReviewParticipantModel.ParticipantRole = ReviewParticipantModel.ParticipantRole.REVIEWER) -> None:
        """
            FR-02: Allow users to create reviews, add specific users and assign them roles
        """
        newParticipant = ReviewParticipantModel.ReviewParticipant(
            userID,
            self.reviewId,
            ReviewParticipantModel.ParticipantRole.REVIEWER,
            ReviewParticipantModel.ParticipantStatus.IN_PROGRESS
        )

        DatabaseHelper.insertIntoDbFromModel(ReviewParticipantModel.ReviewParticipant, newParticipant)
        self.reviewParticipantsUserIDs.append(userID)


    def seeComments(self) -> list:
        return DatabaseHelper.getModelsFromDbQuery(CommentModel.Comment, "reviewID", self.reviewId)
    
    def addComments(self, userID: int, comment):
        if userID not in self.reviewParticipantsUserIDs:
            from models import UserModel
            raise UserModel.AccessError

        DatabaseHelper.insertIntoDbFromModel(CommentModel.Comment, comment)
        self.comments.append(comment.commentId)


    def evaluateReview(self) -> bool:
        """
        i'm going to assume the documentation is wrong on this one
        since I think sometime ago we agreed that a review is accepted
        when all ReviewParticipants accept it? so thats what imma do here
        """
        for reviewerID in self.reviewParticipantsUserIDs:

            participant = DatabaseHelper.getRowFromDbByPrimaryKey(ReviewParticipantModel.ReviewParticipant, reviewerID)
            if participant.status != ReviewParticipantModel.ParticipantStatus.ACCEPTED:
                return False

        self.status = ReviewStatus.APPROVED 
        return True
        
    def getReviewParticipants(self) -> list:

        from models.DatabaseModelHelper import DatabaseHelper
        return DatabaseHelper.getModelsFromDbQuery(ReviewParticipantModel.ReviewParticipant, "reviewId", self.reviewId)

    def getReviewParticipantsNames(self) -> list[str]:
        participants = self.getReviewParticipants()
        output = []
        for participant in participants:
            user = DatabaseHelper.getModelsFromDbQuery(UserModel.User, "userID",   participant.userID)
            if len(user) <= 0:
                raise ValueError(f"No user found with ID {participant.userID}")
            output.append(user[0].username)
        return output

    def jsonify(self) -> dict:
        return {
            "reviewId": self.reviewId,
            "authorId": self.authorId,
            "title": self.title,
            "description": self.description,
            "status": self.status.value,
            "commitId": str(self.commitId),
            "fileLink": self.fileLink,
            "creationDate": self.creationDate.strftime("%Y-%m-%d"),
            "authorId": self.authorId
        }

    def constructFromDbData(data: list):
        reviews_data = data
        reviews = []

        for row in reviews_data:
            reviews.append(Review(
                row["reviewID"],
                authorId=row["authorId"],
                title=row["title"],
                description=row["description"],
                status=ReviewStatus(int(row["status"])),
                fileLink=row["fileLink"],
                creationDate=datetime.datetime.strptime(row["creationDate"], "%Y-%m-%d")
            ))

        return reviews

    
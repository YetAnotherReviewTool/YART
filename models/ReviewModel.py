from models import ReviewParticipantModel
from models import CommentModel
import enum
import models.UserModel as UserModel
import datetime

class ReviewStatus(enum.Enum):
    IN_REVIEW = enum.auto()
    APPROVED = enum.auto()

class Review:
    def __init__(self, title, description):
        self.reviewId: int 
        self.title: str = title
        self.description: str = description
        self.status: ReviewStatus = ReviewStatus.IN_REVIEW
        self.commitId: list[int]
        self.fileLink: str
        self.creationDate: datetime.datetime = datetime.datetime.today()

        self.authorId: int
        self.reviewParticipants: list[int] #get from DB

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

        #save new reviewer to DB TODO

        self.reviewParticipants.append(userID)

    def seeComments(self) -> list[CommentModel.Comment]:
        allComments = []

        for participant in self.reviewParticipants:
            for comment in participant.getComments():
                allComments.append(comment)

        return allComments
    
    def addComments(self, userID: int, comment: CommentModel.Comment):
        if userID not in self.reviewParticipants:
            raise UserModel.AccessError
        
        # TODO
        # add an entry to comments DB
        # update reviewer comment ID list 

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
    
    def getFromDB(reviewID):
        pass #TODO

    def insertToDB(self):
        pass #TODO
        


    
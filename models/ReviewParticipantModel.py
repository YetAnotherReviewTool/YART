import enum
import CommentModel
from DatabaseModelHelper import DatabaseHelper

class ParticipantRole(enum.Enum):
    AUTHOR = enum.auto()
    REVIEWER = enum.auto()
    OBSERVER = enum.auto()

class ParticipantStatus(enum.Enum):
    REJECTED = enum.auto()
    IN_PROGRESS = enum.auto()
    ACCEPTED = enum.auto()

class ReviewParticipant:
    def __init__(self, userID: int,
                 reviewID: int,
                 role: ParticipantRole,
                 isAccepted: ParticipantStatus,
                 comments: list[int] = []):
        
        self.userID: int = userID
        self.reviewID: int = reviewID
        self.role: ParticipantRole = role
        self.status: ParticipantStatus = isAccepted
        

        self.comments: list[int] = comments


    def getComments(self):
        return DatabaseHelper.getModelsFromDbQuery(CommentModel.Comment, "authorID", self.userID)

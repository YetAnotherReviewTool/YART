import enum
import models.CommentModel as CommentModel
from models.DatabaseModelHelper import DatabaseHelper

class ParticipantRole(enum.Enum):
    AUTHOR = 1
    REVIEWER = 2
    OBSERVER = 3

class ParticipantStatus(enum.Enum):
    REJECTED = enum.auto()
    IN_PROGRESS = enum.auto()
    ACCEPTED = enum.auto()

class ReviewParticipant:
    def __init__(self, userID: int,
                 reviewID: int,
                 role: ParticipantRole,
                 isAccepted: ParticipantStatus,
                 ):
        
        self.userID: int = userID
        self.reviewID: int = reviewID
        self.role: ParticipantRole = role
        self.status: ParticipantStatus = isAccepted

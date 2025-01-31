import enum
import CommentModel

class ParticipantRole(enum.Enum):
    AUTHOR = enum.auto()
    REVIEWER = enum.auto()
    OBSERVER = enum.auto()

class ParticipantStatus(enum.Enum):
    REJECTED = enum.auto()
    IN_PROGRESS = enum.auto()
    ACCEPTED = enum.auto()

class ReviewParticipant:
    def __init__(self, userId: int, role: ParticipantRole, isAccepted: ParticipantStatus):
        self.userID: int = userId
        self.role: ParticipantRole = role
        self.status: ParticipantStatus = isAccepted
        self.comments: list[int] #get from DB

        self.reviewID: int

    def getComments(self):
        return self.comments
    
    def getFromDB(reviewerID: int):
        pass #TODO

    def insertToDB(self):
        pass #TODO
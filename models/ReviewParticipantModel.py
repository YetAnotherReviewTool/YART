import enum
import models.CommentModel
from models.model import Model

class ParticipantRole(enum.Enum):
    AUTHOR = 1
    REVIEWER = 2
    OBSERVER = 3

class ParticipantStatus(enum.Enum):
    REJECTED = 1
    IN_PROGRESS = 2
    ACCEPTED = 3

class ReviewParticipant(Model):
    def __init__(self, userID: int,
                 reviewID: int,
                 role: ParticipantRole,
                 isAccepted: ParticipantStatus,
                 ):
        
        self.userID: int = userID
        self.reviewID: int = reviewID
        self.role: ParticipantRole = role
        self.status: ParticipantStatus = isAccepted

    def jsonify(self):
        return {
            "userID": self.userID,
            "reviewID": self.reviewID,
            "role": self.role.value,
            "status": self.status.value
        }

    def constructFromDbData(data):
        participants_data = data
        participants = []

        for row in participants_data:
            participants.append(ReviewParticipant(
                userID=row["userID"],
                reviewID=row["reviewID"],
                role=ParticipantRole[int(row["role"])],
                isAccepted=ParticipantStatus[int(row["status"])]
            ))

        return participants


import csv
import logging
from typing import List

from models.ReviewModel import Review, ReviewStatus
from models.UserModel import User, AccessError
from models.DatabaseModelHelper import DatabaseHelper

FILENAME = "review_statistics.csv"

def generate_report(userID):
    """
        Generate a report for all reviews and export to a CSV file.
    """

    reviews = DatabaseHelper.getModelsFromDb(Review)
    total_reviews = len(reviews)
    approved_reviews = sum(1 for review in reviews if review.status == ReviewStatus.APPROVED)
    in_review_reviews = sum(1 for review in reviews if review.status == ReviewStatus.IN_REVIEW)

    with open(FILENAME, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow([
            "Review ID", "Title", "Description", "Status", "Commit IDs",
            "Creation Date", "Author ID", "Review Participants"
        ])

        # Write review data
        for review in reviews:
            writer.writerow([
                review.reviewId,
                review.title,
                review.description,
                review.status.value,
                ", ".join(map(str, review.commitId)),
                review.creationDate.strftime("%Y-%m-%d %H:%M:%S"),
                review.authorId,
                ", ".join(map(str, review.reviewParticipants))
            ])

        writer.writerow([])
        writer.writerow(["Overall Statistics"])
        writer.writerow(["Total Reviews", total_reviews])
        writer.writerow(["Approved Reviews", approved_reviews])
        writer.writerow(["In Review", in_review_reviews])

    logging.debug(f"Statistics report generated successfully: {FILENAME}")


def add_user(username: str, password: str):
    new_user = User(DatabaseHelper.getNextId(User), username, password)
    DatabaseHelper.insertIntoDbFromModel(User, new_user)
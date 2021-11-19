from typing import List

from .private import PrivateRequest
from querapi.extractors import extract_class_users, extract_assignment_submission
from querapi.models import ContestModel, Question, ClassUser, AssignmentUser, AssignmentSubmission


class ClassMixin(PrivateRequest):
    def __init__(self) -> None:
        super().__init__()

    def get_class_users(self, url: str) -> List[ClassUser]:
        res = self.private_request(url)
        return extract_class_users(res.text)

    def get_assignment_submissions(self, url) -> List[AssignmentSubmission]:
        res = self.private_request(url)
        return extract_assignment_submission(res.text)

    # def get_user_submission_filter(self, submissions: List[AssignmentSubmission]) -> List[AssignmentSubmission]:
    #     for s in range(submissions):
    #
    #     return extract_assignment_submission(res.text)


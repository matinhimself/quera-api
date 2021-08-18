from typing import List

from .private import PrivateRequest
from querapi.extractors import extract_contests, extract_contest_questions, parse_question, extract_questions_metadata
from querapi.models import ContestModel, Question


class ContestMixin(PrivateRequest):
    def __init__(self) -> None:
        super().__init__()

    def get_contests(self) -> List[ContestModel]:
        res = self.private_request('contest/')
        contests = extract_contests(res.text)
        return contests

    def get_questions(self, url: str) -> List[Question]:
        res = self.private_request(url)
        qs = extract_contest_questions(res.text)
        for q in qs:
            self.get_question_tests(q.link, q)
        return qs

    def get_question(self, url: str) -> Question:
        res = self.private_request(url)
        return extract_questions_metadata(res.text, url)

    def get_question_tests(self, url: str, q: Question) -> Question:
        res = self.private_request(url)
        q = parse_question(res.text, q)
        return q

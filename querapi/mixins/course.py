from typing import List
from .private import PrivateRequest
from querapi.models import Course
from querapi.extractors import extract_courses

class CourseMixin(PrivateRequest):
    def __init__(self) -> None:
        super().__init__()

    def get_courses(self) -> List[Course]:
        res = self.private_request('overview/')
        contests = extract_courses(res.text)
        return contests
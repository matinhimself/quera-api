from typing import List
from .private import PrivateRequest
from querapi.models import Course, Assignment, ShortAssignment
from querapi.extractors import extract_courses, extract_short_assignments

class CourseMixin(PrivateRequest):
    def __init__(self) -> None:
        super().__init__()

    def get_courses(self) -> List[Course]:
        res = self.private_request('overview/')
        contests = extract_courses(res.text)
        return contests
    
    def get_short_assignments(self, url: str) -> List[ShortAssignment]:
        res = self.private_request(url)
        shortassignments = extract_short_assignments(res.text)
        return shortassignments
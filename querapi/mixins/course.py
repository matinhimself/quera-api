from typing import List
from .private import PrivateRequest
from querapi.models import Course, ShortAssignment
from querapi.extractors import extract_courses, extract_short_assignments

class CourseMixin(PrivateRequest):
    def __init__(self) -> None:
        super().__init__()

    def get_courses(self) -> List[Course]:
        res = self.private_request('overview/')
        contests = extract_courses(res.text)
        return contests
    
    def get_short_assignments(self, course_id: str) -> List[ShortAssignment]:
        """
        returns course assignments in descending order.
        """
        res = self.private_request(f'course/qa/api/{course_id}/settings/')
        return extract_short_assignments(res.json())
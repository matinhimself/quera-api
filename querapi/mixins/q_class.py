from typing import List

from .private import PrivateRequest
from querapi.extractors import extract_class_users
from querapi.models import ContestModel, Question, ClassUser


class ClassMixin(PrivateRequest):
    def __init__(self) -> None:
        super().__init__()

    def get_class_users(self, url: str) -> List[ClassUser]:
        res = self.private_request(url)
        return extract_class_users(res.text)


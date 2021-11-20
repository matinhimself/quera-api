import json
from querapi.mixins import AuthMixin, ContestMixin, ClassMixin, CourseMixin


class Client(
            AuthMixin,
            ContestMixin,
            ClassMixin,
            CourseMixin  
        ):
    
    def __init__(self):
        super().__init__()

    def save_session(self, path: str) -> bool:
        with open(path, 'w') as wf:
            json.dump(self.session.cookies.get_dict(), wf, indent=4)
        return True
    
    def load_session(self, path: str) -> bool:
        with open(path, 'r') as rf:
            self.login_by_session_id(json.load(rf)['session_id'])
        return True
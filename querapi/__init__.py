from querapi.mixins import AuthMixin, ContestMixin, ClassMixin


class Client:
    def __init__(self):
        self.name: str
        self.email: str


class QueraApi(AuthMixin, ContestMixin,
               ClassMixin):
    def __init__(self):
        super().__init__()

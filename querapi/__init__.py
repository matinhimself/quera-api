from querapi.mixins import AuthMixin, ContestMixin


class Client:
    def __init__(self):
        self.name: str
        self.email: str


class QueraApi(AuthMixin, ContestMixin):
    def __init__(self):
        super().__init__()

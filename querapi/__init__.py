from querapi.mixins import AuthMixin, ContestMixin, ClassMixin, CourseMixin


class Client(
            AuthMixin,
            ContestMixin,
            ClassMixin,
            CourseMixin  
        ):
    
    def __init__(self):
        super().__init__()

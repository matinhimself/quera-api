import requests
from querapi.constants import BASE_URL


class PrivateRequest:

    def __init__(self) -> None:
        self.session = requests.Session()
        super().__init__()

    def private_request(self, endpoint,
                        data=None, json=None,
                        params=None, headers=None, method="GET"):
        if headers:
            self.session.headers.update(headers)

        response = self.session.request(method, BASE_URL.format(endpoint), params=params, json=json, data=data)

        return response

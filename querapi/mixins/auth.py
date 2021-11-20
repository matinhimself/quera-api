from querapi.mixins.private import PrivateRequest
from querapi.constants import BASE_HEADERS
import re

class AuthMixin(PrivateRequest):

    def login(self, email: str, password: str) -> bool:
        # Clean Login
        self.session.cookies.clear()
        self.session.headers.clear()
        self.session.headers.update(BASE_HEADERS)

        # Get Tokens
        response = self.private_request('accounts/login')
        csrf_token = response.cookies.get('csrf_token')
        csrfmiddleware_token = re.findall(r'csrfmiddlewaretoken" value="(.*?)"', response.text)[0]
        self.session.headers.update({'cookie': f'csrf_token={csrf_token}'})

        # Send Login Request
        payload = {
            'csrfmiddlewaretoken': csrfmiddleware_token,
            'login': email,
            'password': password,
        }
        response = self.private_request('accounts/login', data=payload, method="POST")
        self.session.headers.pop('referer')

        if response.status_code == 200 and '"is_authenticated": true' in response.text:
            self.session.headers.update({
                'cookie': ' '.join([f'{k}={v};' for k, v in self.session.cookies.get_dict().items()])[:-1]
            })
            return True

        return False

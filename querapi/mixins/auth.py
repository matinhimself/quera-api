from querapi.mixins.private import PrivateRequest
from querapi.constants import BASE_HEADERS
import re

class AuthMixin(PrivateRequest):
    
    csrf_token = None
    csrfmiddleware_token = None
    
    def init(self):
        """
        Initialize Login helpers

        """
        self.session.cookies.clear()
        self.session.headers.clear()
        self.session.headers.update(BASE_HEADERS)

        response = self.private_request('accounts/login')
        self.csrf_token = response.cookies.get('csrf_token')
        self.csrfmiddleware_token = re.findall(r'csrfmiddlewaretoken" value="(.*?)"', response.text)[0]
        
        
    def login(self, email: str, password: str) -> bool:
        self.init()
        self.session.headers.update({'cookie': f'csrf_token={self.csrf_token}'})
        
        payload = {
            'csrfmiddlewaretoken': self.csrfmiddleware_token,
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

    def login_by_session_id(self, session_id) -> bool:
        self.init()
        self.session.headers.pop('referer')
        self.session.headers.update({
                'cookie': f'HTTP_REFERER=quera.ir; csrf_token={self.csrf_token}; session_id={session_id}'
        })
        return True
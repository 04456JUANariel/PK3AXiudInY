# 代码生成时间: 2025-08-18 03:27:03
import falcon
from falcon.auth import AuthMiddleware, BasicAuth
from falcon.auth.backends import PlainText

class BasicAuthMiddleware(AuthMiddleware):
    """Middleware to handle basic authentication for secured resources."""
    def __init__(self, realm):
        self.realm = realm
        self.basic_auth = BasicAuth(
            self.plain_text_basic_auth,
            "Basic realm=\"{0}\"".format(realm)
        )

    def plain_text_basic_auth(self, username, password):
        """
        Verify the username and password by checking the credentials against the
        stored user list.
        """
        # For demonstration purposes, use a hardcoded user list.
        # In a real application, you would check against a database or other
        # storage mechanism.
        valid_users = {
            'user1': 'password1',
            'user2': 'password2'
        }
        return valid_users.get(username) == password

    def process_request(self, req, resp):
        "
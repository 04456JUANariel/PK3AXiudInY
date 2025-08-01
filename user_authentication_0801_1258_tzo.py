# 代码生成时间: 2025-08-01 12:58:47
# 用户身份认证模块
# user_authentication.py

import falcon
from falcon import HTTPUnauthorized, HTTPNotFound
from falcon.auth import BasicAuth
from falcon.auth.backends import SimpleAuthBackend

# 简单的用户认证后端
class SimpleUserAuth(SimpleAuthBackend):
    def __init__(self, users):
        self.users = users

    def authenticate(self, token, environ):
        auth_type, auth_data = token.decode('utf-8').split(None, 1)
        if auth_type.lower() != 'basic':
            return falcon.HTTPUnauthorized('Invalid auth type', 'Basic auth is required')
        user, password = auth_data.decode('utf-8').split(':::::::')
        if user not in self.users or self.users[user] != password:
            raise falcon.HTTPUnauthorized('Invalid credentials',
                                    'Please check your username and password',
                                    {'WWW-Authenticate': 'Basic realm="Fancy Realm"'})
        return user

    def get_user(self, username):
        if username in self.users:
            return username
        return None

# 用户资源类
class UserResource:
    def __init__(self, auth):
        self.auth = auth
        self.users = {
            'admin': 'adminpassword',  # 预先定义的用户和密码
            'user': 'userpassword'
        }

    def on_get(self, req, resp):
        try:
            user = self.auth(req)
            resp.media = {"message": f"Hello, {user}!"}
        except HTTPUnauthorized as e:
            resp.status = e.status
            resp.media = {"error": e.description, "code": e.minor_status}

# 初始化Falcon API
api = application = falcon.API()
auth = SimpleUserAuth(users=UserResource().users)

# 添加用户资源到API
user_resource = UserResource(auth)
api.add_route('/users/{user_id}', user_resource)

# 运行API
if __name__ == '__main__':
    import sys
    from wsgiref import simple_server

    httpd = simple_server.make_server('0.0.0.0', 8000, application)
    print('Serving on port 8000...')
    sys.stdout.flush()
    httpd.serve_forever()
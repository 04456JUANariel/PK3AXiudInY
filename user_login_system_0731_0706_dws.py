# 代码生成时间: 2025-07-31 07:06:02
# user_login_system.py
# 使用FALCON框架实现的用户登录验证系统

from falcon import API, Response, HTTPBadRequest, HTTPUnauthorized
from falcon.auth import BasicAuth
from falcon_auth import AuthMiddleware
import hashlib

# 用户数据库模拟
# 在实际应用中，这里应该是数据库查询操作
USER_DATABASE = {
    "admin": "5f4dcc3b5aa765d61d8327deb882cf99"  # 密码是admin, MD5加密
}

class UserResource:
    """处理用户登录请求的资源"""
    def on_post(self, req, resp):
        """处理POST请求，进行用户登录验证"""
        auth = BasicAuth(req.auth)
        if not auth:
            raise HTTPUnauthorized('Authentication required', 'Basic')

        user, passwd = auth.username, auth.password
        if user not in USER_DATABASE:
            raise HTTPBadRequest('Username not found', 'User not found in database')

        # 验证密码
        if hashlib.md5(passwd.encode()).hexdigest() != USER_DATABASE[user]:
            raise HTTPUnauthorized('Authentication failure', 'Invalid password')

        # 登录成功，返回用户信息
        resp.status = falcon.HTTP_OK
        resp.media = {"username": user, "message": "Login successful"}

# 创建API对象
api = API()

# 添加中间件，用于处理认证
api.req_options.auth_provider = BasicAuth
api.add_authmiddleware(AuthMiddleware())

# 添加资源
user_resource = UserResource()
api.add_route("/login", user_resource)

# 以下代码用于测试，实际部署时需要移除
if __name__ == "__main__":
    from wsgiref.simple_server import make_server
    httpd = make_server('0.0.0.0', 8000, api)
    print('Serving on port 8000...')
    httpd.serve_forever()
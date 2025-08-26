# 代码生成时间: 2025-08-26 20:56:24
# 导入Falcon框架和必要的库
from falcon import API, Request, Response, HTTPUnauthorized, HTTPForbidden

# 模拟的用户数据库
users_db = {
    "user1": "password1",
    "user2": "password2"
}

# 访问权限控制类的实现
class AuthMiddleware(object):
    """访问权限控制中间件"""
    def process_request(self, req, resp):
        """请求处理阶段，检查认证信息"""
        auth_header = req.headers.get("Authorization")
        if auth_header is None:
            raise HTTPUnauthorized("Authentication required", "Please provide a valid authentication header")
        
        # 解析Authorization头部，例如：Basic QWxhZGprbWVyOmFkbWlu
        auth_type, credentials = auth_header.split(" ", 1)
        if auth_type.lower() != "basic":
            raise HTTPUnauthorized("Unsupported authentication method", "Only Basic authentication is supported")
        
        try:
            username, password = credentials.decode("base64").split(":")
        except (ValueError, TypeError):
            raise HTTPUnauthorized("Bad credentials", "Invalid authentication credentials")
        
        # 验证用户名和密码
        if username not in users_db or users_db[username] != password:
            raise HTTPUnauthorized("Bad credentials", "The username or password is incorrect")
        
        # 设置当前用户
        req.context.user = username
        
    def process_response(self, req, resp):
        """响应处理阶段，无需处理"""
        pass

# 创建API实例
api = API(middleware=[AuthMiddleware()])

# 定义需要访问控制的资源
class ProtectedResource:
    """需要访问控制的资源"""
    def on_get(self, req, resp):
        """处理GET请求"""
        resp.status = falcon.HTTP_200
        resp.media = {"message": f"Hello, {req.context.user}!"}

# 将资源添加到API中
api.add_route("/protected", ProtectedResource())

# 运行API（仅用于演示，实际部署时需要使用gunicorn等WSGI服务器）
if __name__ == "__main__":
    from wsgiref.simple_server import make_server
    make_server("0.0.0.0", 8000, api).serve_forever()
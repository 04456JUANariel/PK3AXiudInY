# 代码生成时间: 2025-09-01 05:49:25
import falcon
import requests
from urllib.parse import urlparse
from falcon import HTTP_400, HTTP_404, HTTP_500

# 函数用于验证URL是否有效
def is_valid_url(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

# 函数用于检测URL是否可以被访问
def is_reachable_url(url):
    try:
        response = requests.head(url, allow_redirects=True, timeout=5)
        return response.status_code == 200
    except requests.RequestException as e:
        return False

# Falcon API响应类
class UrlValidator:
    def on_get(self, req, resp):
        # 获取请求参数
        url = req.get_param('url')

        # 参数验证
        if not url:
            raise falcon.HTTPBadRequest('URL parameter is missing', 'Please provide a URL parameter')

        # 验证URL是否有效
        if not is_valid_url(url):
            raise falcon.HTTPBadRequest('Invalid URL', 'Provided URL is not valid')

        # 验证URL是否可以被访问
        if is_reachable_url(url):
            resp.media = {'message': 'URL is valid and reachable'}
        else:
            resp.media = {'message': 'URL is valid but not reachable'}
            resp.status = falcon.HTTP_503

# 配置Falcon API
api = falcon.API()
api.add_route('/validate-url', UrlValidator())

# 如果直接运行此文件，将启动Falcon服务器
if __name__ == '__main__':
    # 启动Falcon API服务器
    from wsgiref.simple_server import make_server
    server = make_server('0.0.0.0', 8000, api)
    print('Starting API server on http://0.0.0.0:8000')
    server.serve_forever()
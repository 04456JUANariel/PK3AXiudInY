# 代码生成时间: 2025-09-30 01:30:27
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
API测试工具
"""
import falcon
import json
import requests
from falcon import testing

# 定义API端点
class ApiTest:
    def on_get(self, req, resp):
        """处理GET请求"""
        # 解析请求参数
        method = req.get_param('method')
        url = req.get_param('url')
        params = req.get_param_as_dict('params')
        headers = req.get_param_as_dict('headers')
        data = req.get_param('data') or ''

        # 发送请求
        try:
            if method.upper() == 'GET':
                response = requests.get(url, params=params, headers=headers)
            elif method.upper() == 'POST':
                response = requests.post(url, data=data, params=params, headers=headers)
            else:
                raise ValueError('不支持的请求方法')

            # 设置响应内容和状态码
            resp.status = falcon.HTTP_200
            resp.media = {'status': 'success', 'data': response.json()}
        except Exception as e:
            # 错误处理
            resp.status = falcon.HTTP_400
            resp.media = {'status': 'error', 'message': str(e)}

# 创建Falcon应用
app = falcon.App()

# 配置路由
app.add_route('/api/test', ApiTest())

def main():
    """
    主函数
    """
    # 运行测试服务器
    from wsgiref.simple_server import make_server
    with make_server('0.0.0.0', 8000, app) as httpd:
        print('Serving on port 8000...')
        httpd.serve_forever()

if __name__ == '__main__':
    main()

# 测试代码
# 测试GET请求
class TestApiGet:
    def test_get(self):
        from falcon.testing import TestClient
        sim_client = TestClient(app)
        sim_req = testing.TestRequest(
            path='/api/test',
            method='GET',
            query_string={'method': 'GET', 'url': 'https://httpbin.org/get', 'params': json.dumps({'key': 'value'})}
        )
        sim_res = sim_client.simulate_request(sim_req)
        assert sim_res.status == falcon.HTTP_200
        assert 'data' in sim_res.json

# 测试POST请求
class TestApiPost:
    def test_post(self):
        from falcon.testing import TestClient
        sim_client = TestClient(app)
        sim_req = testing.TestRequest(
            path='/api/test',
            method='GET',
            query_string={'method': 'POST', 'url': 'https://httpbin.org/post', 'data': 'key=value', 'headers': json.dumps({'Content-Type': 'application/x-www-form-urlencoded'})}
        )
        sim_res = sim_client.simulate_request(sim_req)
        assert sim_res.status == falcon.HTTP_200
        assert 'data' in sim_res.json

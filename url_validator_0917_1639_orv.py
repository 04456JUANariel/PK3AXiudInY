# 代码生成时间: 2025-09-17 16:39:50
#!/usr/bin/env python

"""
URL链接有效性验证程序
使用FALCON框架创建一个简单的API来验证URL链接的有效性。
"""

import falcon
from urllib.parse import urlparse
import requests

# 定义一个错误响应类
class ValidationError(falcon.HTTPError):
    def __init__(self, description, *args, **kwargs):
        super(ValidationError, self).__init__(400, description, *args, **kwargs)

# URL验证逻辑
def validate_url(url):
    """
    验证URL的有效性
    :param url: 要验证的URL字符串
    :return: 如果URL有效返回True，否则抛出ValidationError
    """
    try:
        result = urlparse(url)
        if all([result.scheme, result.netloc]):
            # 进一步验证URL是否可达
            response = requests.head(url, timeout=5)
            if response.status_code == 200:
                return True
            else:
                raise ValidationError("URL is not reachable: {}".format(url))
        else:
            raise ValidationError("Invalid URL format: {}".format(url))
    except ValueError as e:
        raise ValidationError("Invalid URL format: {}".format(url))

# Falcon路由处理器
class URLValidator:
    def on_get(self, req, resp):
        """
        处理GET请求，验证传入的URL参数
        """
        url = req.get_param('url', required=True)
        try:
            if validate_url(url):
                resp.status = falcon.HTTP_OK
                resp.body = 'URL is valid'
        except ValidationError as e:
            resp.status = falcon.HTTP_BAD_REQUEST
            resp.body = str(e)

# 创建Falcon应用实例
app = falcon.App()
# 添加路由
app.add_route('/validate', URLValidator())

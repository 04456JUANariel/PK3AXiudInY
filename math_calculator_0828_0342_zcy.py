# 代码生成时间: 2025-08-28 03:42:46
# math_calculator.py

import falcon

# 定义一个 Falcon API 应用
app = application = falcon.App()

# 数学计算工具集的路由前缀
MATH_ROUTE = '/math/'

# 定义数学工具集类
class MathTools:
    # 构造函数
    def __init__(self):
        pass

    # 加法
    def add(self, a, b):
        try:
            return float(a) + float(b)
        except ValueError:
            raise falcon.HTTPError(falcon.HTTP_400, 'Invalid value.')

    # 减法
    def subtract(self, a, b):
        try:
            return float(a) - float(b)
        except ValueError:
            raise falcon.HTTPError(falcon.HTTP_400, 'Invalid value.')

    # 乘法
    def multiply(self, a, b):
        try:
            return float(a) * float(b)
        except ValueError:
            raise falcon.HTTPError(falcon.HTTP_400, 'Invalid value.')

    # 除法
    def divide(self, a, b):
        try:
            return float(a) / float(b)
        except ZeroDivisionError:
            raise falcon.HTTPError(falcon.HTTP_400, 'Cannot divide by zero.')
        except ValueError:
            raise falcon.HTTPError(falcon.HTTP_400, 'Invalid value.')

    # 定义一个方法处理请求
    def on_get(self, req, resp, operation):
        try:
            a = float(req.get_param('a'))
            b = float(req.get_param('b'))
        except ValueError:
            raise falcon.HTTPError(falcon.HTTP_400, 'Invalid input values.')

        if operation == 'add':
            result = self.add(a, b)
        elif operation == 'subtract':
            result = self.subtract(a, b)
        elif operation == 'multiply':
            result = self.multiply(a, b)
        elif operation == 'divide':
            result = self.divide(a, b)
        else:
            raise falcon.HTTPError(falcon.HTTP_404, 'Method not found.')

        resp.body = str(result)
        resp.status = falcon.HTTP_200

# 创建数学工具集实例
math_tools = MathTools()

# 添加路由
app.add_route(MATH_ROUTE + 'add', math_tools, suffix='on_get')
app.add_route(MATH_ROUTE + 'subtract', math_tools, suffix='on_get')
app.add_route(MATH_ROUTE + 'multiply', math_tools, suffix='on_get')
app.add_route(MATH_ROUTE + 'divide', math_tools, suffix='on_get')
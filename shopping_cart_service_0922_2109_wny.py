# 代码生成时间: 2025-09-22 21:09:42
import falcon
import json
from falcon import HTTP_200, HTTP_400

# 购物车服务
class ShoppingCartService:
    # 初始化购物车
    def __init__(self):
        self.cart = []

    # 添加商品到购物车
    def add_item(self, item):
        self.cart.append(item)
        return {
            "status": "success",
            "message": "Item added to cart.",
            "cart": self.cart
        }

    # 从购物车移除商品
    def remove_item(self, item_id):
        try:
            self.cart = [item for item in self.cart if item["id"] != item_id]
            return {
                "status": "success",
                "message": "Item removed from cart.",
                "cart": self.cart
            }
        except KeyError:
            return {
                "status": "error",
                "message": "Item not found in cart."
            }

    # 获取购物车内容
    def get_cart(self):
        return {
            "status": "success",
            "cart": self.cart
        }

# 将购物车服务作为资源
class ShoppingCartResource:
    def __init__(self):
        self.service = ShoppingCartService()

    # 处理添加商品请求
    def on_post(self, req, resp):
        # 从请求体中获取商品数据
        item = req.media or {}

        # 调用服务添加商品
        result = self.service.add_item(item)

        # 设置响应状态和返回结果
        resp.status = HTTP_200
        resp.body = json.dumps(result)

    # 处理移除商品请求
    def on_delete(self, req, resp, item_id):
        # 调用服务移除商品
        result = self.service.remove_item(item_id)

        # 设置响应状态和返回结果
        resp.status = HTTP_200
        resp.body = json.dumps(result)

    # 处理获取购物车内容请求
    def on_get(self, req, resp):
        # 调用服务获取购物车内容
        result = self.service.get_cart()

        # 设置响应状态和返回结果
        resp.status = HTTP_200
        resp.body = json.dumps(result)

# 定义API路由
api = application = falcon.API()
api.add_route("/cart", ShoppingCartResource())
api.add_route("/cart/{item_id}", ShoppingCartResource())
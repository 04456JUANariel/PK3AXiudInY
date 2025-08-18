# 代码生成时间: 2025-08-18 09:28:34
# 用户权限管理系统
# 使用FALCON框架实现RESTful API

from falcon import API, HTTPCreated, HTTPNotFound, HTTPConflict, HTTPBadRequest, HTTPInternalServerError
import json

class UserPermission:
    """用户权限管理类"""
    def __init__(self):
        self.permissions = {}

    def add_user(self, user_id, permissions):
        """添加用户及其权限"""
        if user_id in self.permissions:
            raise HTTPConflict('User already exists')
        self.permissions[user_id] = permissions
        return HTTPCreated()

    def remove_user(self, user_id):
        """删除用户"""
        if user_id not in self.permissions:
            raise HTTPNotFound('User not found')
        del self.permissions[user_id]
        return HTTPCreated()

    def update_user_permissions(self, user_id, permissions):
        "
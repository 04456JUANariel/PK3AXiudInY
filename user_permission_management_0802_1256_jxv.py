# 代码生成时间: 2025-08-02 12:56:02
#!/usr/bin/env python
"""
User Permission Management System using FALCON framework.
"""

import falcon
from falcon import API
from falcon_auth import FalconAuth
from falcon_auth.backends import SimpleAuthBackend

class UserPermission:
    """
    Class to handle user permissions.
    """
    def __init__(self):
        """
        Initialize the user permission system.
        """
        self.permissions = {}

    def add_permission(self, user_id, permission):
        """
        Add a permission to a user.
        """
        if user_id not in self.permissions:
            self.permissions[user_id] = []
        self.permissions[user_id].append(permission)

    def remove_permission(self, user_id, permission):
        """
        Remove a permission from a user.
        """
        if user_id in self.permissions:
            self.permissions[user_id] = [p for p in self.permissions[user_id] if p != permission]

    def check_permission(self, user_id, permission):
        """
        Check if a user has a specific permission.
        """
        if user_id in self.permissions:
            return permission in self.permissions[user_id]
        return False

class PermissionResource:
    """
    FALCON resource to handle permission requests.
    """
    def __init__(self, permission_manager):
        """
        Initialize the permission resource.
        """
        self.permission_manager = permission_manager

    def on_get(self, req, resp, user_id):
        """
        Handle GET request to retrieve user permissions.
        """
        try:
            permissions = self.permission_manager.permissions[user_id]
            resp.media = {"permissions": permissions}
        except KeyError:
            raise falcon.HTTPNotFound("User not found")

    def on_post(self, req, resp, user_id):
        """
        Handle POST request to add a permission to a user.
        """
        try:
            permission = req.media["permission"]
            self.permission_manager.add_permission(user_id, permission)
            resp.status = falcon.HTTP_NO_CONTENT
        except KeyError:
            raise falcon.HTTPBadRequest("Permission not provided")
        except TypeError:
            raise falcon.HTTPBadRequest("Invalid permission format")

    def on_delete(self, req, resp, user_id, permission):
        """
        Handle DELETE request to remove a permission from a user.
        """
        try:
            self.permission_manager.remove_permission(user_id, permission)
            resp.status = falcon.HTTP_NO_CONTENT
        except KeyError:
            raise falcon.HTTPNotFound("Permission not found")
        except ValueError:
            raise falcon.HTTPBadRequest("Invalid permission format")

def main():
    """
    Main function to start the FALCON app.
    """
    auth = SimpleAuthBackend(user_check=lambda x: x == "admin")
    auth_provider = FalconAuth(auth, header="Authorization")
    
    permission_manager = UserPermission()
    
    app = API(middleware=auth_provider)

    # Add permissions resource
    app.add_route("/users/{user_id}/permissions", PermissionResource(permission_manager), suffix="id")
    app.add_route("/users/{user_id}/permissions/{permission}", PermissionResource(permission_manager), suffix="permission")

    # Start the app
    app.run(host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()
# 代码生成时间: 2025-08-16 20:21:22
#!/usr/bin/env python

"""
XSS Protection with Falcon Framework
This script implements an XSS protection middleware in Falcon framework.
It sanitizes input to prevent Cross-Site Scripting (XSS) attacks.
"""

from falcon import App, Request, Response
from html import escape

# Middleware to sanitize inputs to protect against XSS
class XSSProtectionMiddleware:
    def process_request(self, req, resp):
        # Iterate over all params and sanitize them
        for param, value in req.params.items():
            req.params[param] = escape(value)

    def process_resource(self, req, resp, resource):
        pass

# A sample resource to demonstrate XSS protection
class SimpleResource:
    def on_get(self, req, resp):
        # Retrieve sanitized input from request
        user_input = req.params.get('user_input')
        # Respond with sanitized input
        resp.body = f"User input sanitized: {user_input}"
        resp.media = {"message": "User input has been sanitized to prevent XSS"}

# Create a Falcon app
app = App(middleware=[XSSProtectionMiddleware()])

# Register the resource with the app
app.add_route('/', SimpleResource())

# The Falcon wsgi app
if __name__ == '__main__':
    import falcon.testing
    from wsgiref.simple_server import make_server

    # Create a server
    httpd = make_server('localhost', 8000, app)
    print('Serving on localhost port 8000...')
    # Start the server
    httpd.serve_forever()
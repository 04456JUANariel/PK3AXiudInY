# 代码生成时间: 2025-08-09 11:38:09
#!/usr/bin/env python

"""
XSS Protection Middleware for Falcon Framework

This middleware provides basic XSS protection by sanitizing input from HTTP requests.
It removes potentially malicious script tags and other HTML elements that can be used
for cross-site scripting attacks.
"""

import falcon
from html import escape

class XSSMiddleware:
    """
    Falcon middleware for XSS protection.
    This middleware will sanitize URL and query string parameters.
    """
    def process_request(self, req, resp):
        # Sanitize URL and query string parameters
        req.params = {key: escape(value) for key, value in req.params.items()}
        req.url = escape(req.url)
        
    def process_resource(self, req, resp, resource, params):
        # Pass through the request to the resource
        pass
        
    def process_response(self, req, resp, resource):
        # Sanitize the response body
        if resp.body:
            resp.body = escape(resp.body).encode('utf-8')
        
# Example usage of the middleware with Falcon
app = falcon.App(middleware=[XSSMiddleware()])

# Define a simple resource that will utilize the XSSMiddleware
class SimpleResource:
    def on_get(self, req, resp):
        # Respond with a simple message
        resp.media = {"message": "Hello, world!"}
        
# Add the resource to the app
app.add_route('/', SimpleResource())

# Note: This is a simple example and in a real-world scenario, you may want to
#      use more sophisticated methods for sanitizing input to protect against XSS.
#      Libraries such as bleach can be used for this purpose.

# 代码生成时间: 2025-09-11 09:28:16
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test Data Generator using Falcon framework

This module provides a simple test data generator endpoint.
"""

import falcon
import json
from random import randint, choice
from string import ascii_letters, digits

# Define the API resource
class TestDataResource:
    """Handles GET requests to generate test data."""
    def on_get(self, req, resp):
        try:
            # Generate test data
            test_data = self.generate_test_data()
            # Set response body and status code
            resp.body = json.dumps(test_data)
            resp.status = falcon.HTTP_200
        except Exception as e:
            # Handle any exceptions and return error response
            resp.body = json.dumps({'error': str(e)})
            resp.status = falcon.HTTP_500

    def generate_test_data(self):
        """Generates random test data."""
        test_data = {
            'id': randint(1000, 9999),
            'username': ''.join(choice(ascii_letters + digits) for _ in range(8)),
            'email': ''.join(choice(ascii_letters + digits) for _ in range(6)) + '@example.com',
            'is_active': choice([True, False])
        }
        return test_data

# Initialize Falcon API
api = falcon.API()
# Add resource
api.add_route('/test-data', TestDataResource())

# This function is called when running the script directly.
# It allows the script to be tested directly by running it
# and also allows it to be used as a module.
if __name__ == '__main__':
    # Start the API service
    import wsgiref.simple_server as wsgiref
    httpd = wsgiref.make_server('localhost', 8000, api)
    print("Serving on localhost port 8000")
    httpd.serve_forever()
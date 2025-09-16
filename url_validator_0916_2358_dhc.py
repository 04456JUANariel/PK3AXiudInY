# 代码生成时间: 2025-09-16 23:58:19
#!/usr/bin/env python

"""
URL Validator using Falcon Framework

This script is designed to validate the validity of a given URL.
It uses the Falcon framework to create a simple web service.
"""

import falcon
import requests
from urllib.parse import urlparse

# Create a custom exception for validation errors
class ValidationError(falcon.HTTPError):
    """Custom exception for validation errors"""
    def __init__(self, url, message, status=falcon.HTTP_400):
        self.url = url
        self.message = message
        super(ValidationError, self).__init__(status, message)

# Define the URLValidator class
class URLValidator:
    """Class to validate URL links"""
    def on_get(self, req, resp, url_to_validate):
        """
        Handle GET requests to validate a URL.
        The URL to validate is passed as a query parameter 'url'.
        """
        try:
            # Parse the URL using urlparse
            parsed_url = urlparse(url_to_validate)
            
            # Check if the URL has a scheme and a netloc (domain)
            if not parsed_url.scheme or not parsed_url.netloc:
                raise ValidationError(url_to_validate, 'Invalid URL. Missing scheme or domain.')
                
            # Attempt to make a HEAD request to the URL to check its validity
            response = requests.head(url_to_validate, timeout=5)
            if response.status_code != 200:
                raise ValidationError(url_to_validate, f'Invalid URL. Status code: {response.status_code}')
                
            # Respond with a success message
            resp.body = f'The URL {url_to_validate} is valid and active.'
            resp.status = falcon.HTTP_200
        except ValidationError as e:
            # Handle validation errors
            resp.status = e.status
            resp.body = str(e)
        except Exception as e:
            # Handle any other exceptions
            resp.status = falcon.HTTP_500
            resp.body = f'An error occurred while validating the URL: {str(e)}'

# Initialize the Falcon API
api = falcon.API()

# Add the URLValidator resource to the API
api.add_route('/api/validate', URLValidator())

# Run the API
if __name__ == '__main__':
    import socket
    host = '0.0.0.0'
    port = 8000
    print(f'Starting the Falcon API on {host}:{port}')
    api.run(host=host, port=port, debug=True)
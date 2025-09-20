# 代码生成时间: 2025-09-20 23:17:20
# hash_calculator.py

"""
A simple hash calculator tool using Falcon framework.
"""

from falcon import API, Request, Response
import hashlib
import json

# Falcon API instance
api = API()

# Calculate hash for a given string
def calculate_hash(text):
    """
    Calculate the hash of a given text.

    Args:
        text (str): The text to calculate the hash for.

    Returns:
        str: The hash of the given text.
    """
    try:
        # Choose the desired hashing algorithm (e.g., 'sha256')
        hash_algorithm = hashlib.sha256
        # Encode the text to bytes and calculate the hash
        return hash_algorithm(text.encode()).hexdigest()
    except Exception as e:
        # Return the error message as a JSON response
        return json.dumps({'error': str(e)})

# Create a Falcon resource for the hash calculator
class HashCalculatorResource:
    """
    Falcon resource for calculating hash values.
    """
    def on_get(self, req, resp):
        """
        Handle GET requests to calculate hash values.
        """
        # Retrieve the text from the query parameters
        text = req.get_param('text', required=True)
        
        # Calculate the hash and set the response body
        hash_value = calculate_hash(text)
        resp.media = json.dumps({'hash': hash_value})
        resp.status = falcon.HTTP_200

# Add the resource to the API
api.add_route('/calculate_hash', HashCalculatorResource())

# If this module is executed as the main program, start the Falcon API server
if __name__ == '__main__':
    import falcon
    import socket
    from wsgiref.simple_server import make_server
    
    # Allow the server to bind to 0.0.0.0, so it's accessible from any IP
    HOST, PORT = '0.0.0.0', 8000
    server = make_server(HOST, PORT, api)
    
    print(f'Starting hash calculator server on {HOST}:{PORT}')
    server.serve_forever()
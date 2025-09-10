# 代码生成时间: 2025-09-11 04:02:51
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
System Performance Monitor using Falcon Framework.

This application provides an endpoint to monitor system performance metrics using Falcon.
"""

import falcon
import psutil
from datetime import datetime

def on_get(req, resp):
    """Handle GET requests."""
    try:
        # Collect system performance metrics
        cpu_usage = psutil.cpu_percent()
        memory_usage = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage('/').percent
        network_io = psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv

        # Create a response body with the collected metrics
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        body = {
            'timestamp': now,
            'cpu_usage': cpu_usage,
            'memory_usage': memory_usage,
            'disk_usage': disk_usage,
            'network_io': network_io
        }
        resp.body = json.dumps(body)
        resp.status = falcon.HTTP_200
    except Exception as e:
        # Handle any unexpected errors
        resp.body = "An error occurred: " + str(e)
        resp.status = falcon.HTTP_500

# Create a Falcon API instance
api = falcon.API()

# Add the monitor endpoint
api.add_route('/monitor', Resource())

# Define the Resource class
class Resource():
    def on_get(self, req, resp, *args):
        on_get(req, resp)

if __name__ == '__main__':
    # Start the Falcon application
    import sys
    from wsgiref.simple_server import make_server

    host = '0.0.0.0'
    port = 8000
    httpd = make_server(host, port, api)
    print(f"Starting server at http://{host}:{port}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('Server stopped.')
        sys.exit(0)
    except Exception as e:
        print(f'An unexpected error occurred: {e}')
        sys.exit(1)
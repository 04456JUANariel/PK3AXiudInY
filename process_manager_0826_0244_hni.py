# 代码生成时间: 2025-08-26 02:44:29
# process_manager.py
# A simple process manager using Falcon framework.

import falcon
import subprocess
import psutil
import json

# Falcon router
api = falcon.App()

# Error handler
class ErrorHandler:
    def process_request(self, req, resp):
        resp.set_header('Content-Type', 'application/json')

    def process_response(self, req, resp, resource, req_succeeded):
        if req_succeeded:
            return
        raise falcon.HTTPError(f"{resp.status}", "Internal Server Error")

api.req_options.default_media_type = "application/json"
api.resp_options.default_media_type = "application/json"
api.add_error_handler(Exception, ErrorHandler())

# Process Manager Resource
class ProcessManager:
    def on_get(self, req, resp):
        """
        List all running processes.
        """"
        try:
            processes = []
            for proc in psutil.process_iter(['name', 'pid']):
                processes.append({'name': proc.info['name'], 'pid': proc.info['pid']})
            resp.body = json.dumps(processes)
            resp.status = falcon.HTTP_OK
        except Exception as e:
            raise falcon.HTTPError(falcon.HTTP_INTERNAL_SERVER_ERROR, str(e))

    def on_post(self, req, resp):
        """
        Start a new process.
        """
        try:
            data = req.media
            process_name = data.get('name')
            command = data.get('command')
            if not process_name or not command:
                raise ValueError("Both process name and command are required.")
            subprocess.Popen(command, shell=True)
            resp.body = json.dumps({'message': 'Process started successfully'})
            resp.status = falcon.HTTP_CREATED
        except ValueError as ve:
            raise falcon.HTTPError(falcon.HTTP_BAD_REQUEST, str(ve))
        except Exception as e:
            raise falcon.HTTPError(falcon.HTTP_INTERNAL_SERVER_ERROR, str(e))

    def on_delete(self, req, resp):
        """
        Terminate a process.
        """
        try:
            data = req.media
            pid = data.get('pid')
            if not pid:
                raise ValueError("Process ID is required.")
            proc = psutil.Process(pid)
            proc.terminate()
            resp.body = json.dumps({'message': 'Process terminated successfully'})
            resp.status = falcon.HTTP_OK
        except psutil.NoSuchProcess:
            raise falcon.HTTPError(falcon.HTTP_NOT_FOUND, f'Process with PID {pid} not found.')
        except Exception as e:
            raise falcon.HTTPError(falcon.HTTP_INTERNAL_SERVER_ERROR, str(e))

# Add resource
api.add_route('/processes', ProcessManager())


# This allows the script to be run directly
# For testing purposes
if __name__ == '__main__':
    import socket
    from wsgiref.simple_server import make_server

    # Use a different host and port for your production server
    httpd = make_server('localhost', 8000, api)
    print('Serving on localhost port 8000...')
    httpd.serve_forever()
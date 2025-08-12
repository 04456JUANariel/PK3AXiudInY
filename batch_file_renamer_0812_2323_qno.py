# 代码生成时间: 2025-08-12 23:23:06
# batch_file_renamer.py
# A utility for batch renaming files using Falcon framework in Python

import os
import logging
from falcon import API, Request, Response
from falcon.asgi import ASGISender

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FileRenamer:
    def __init__(self, path):
        self.path = path

    def rename_files(self, prefix, suffix):
        """
        Rename files in the specified directory with the given prefix and suffix.
        Args:
            prefix (str): The prefix to add to each file name.
            suffix (str): The suffix to add to each file name.
        """
        try:
            for filename in os.listdir(self.path):
                filepath = os.path.join(self.path, filename)
                if os.path.isfile(filepath):
                    new_filename = f"{prefix}{filename}{suffix}"
                    new_filepath = os.path.join(self.path, new_filename)
                    os.rename(filepath, new_filepath)
                    logger.info(f"Renamed {filename} to {new_filename}")
        except Exception as e:
            logger.error(f"Error renaming files: {e}")

# Falcon API resource class for renaming files
class RenameFileResource:
    def on_get(self, req: Request, resp: Response):
        """
        Handle GET requests to rename files in the specified directory.
        Args:
            req (Request): Falcon request object containing query parameters.
            resp (Response): Falcon response object.
        """
        path = req.get_param('path')
        prefix = req.get_param('prefix', required=False)
        suffix = req.get_param('suffix', required=False)

        if not path or not prefix or not suffix:
            resp.status = falcon.HTTP_400
            resp.media = {'error': 'Missing required query parameters'}
            return

        renamer = FileRenamer(path)
        renamer.rename_files(prefix, suffix)

        resp.status = falcon.HTTP_200
        resp.media = {'message': 'Files renamed successfully'}

# Initialize Falcon API
api = API()

# Add the resource to the API
api.add_route('/rename', RenameFileResource())

# ASGI application
async def application(scope, receive, send):
    if scope['type'] == 'http':
        await api.asgi_app(scope, receive, send)
    else:
        await ASGISender.send(send, f"{scope=} is not supported")

# 代码生成时间: 2025-08-25 18:45:59
#!/usr/bin/env python

"""
Decompression Tool using Python and Falcon framework.
This tool provides a REST API to decompress files.
"""

import falcon
import zipfile
import os
import shutil

from falcon import HTTP_NotFound, HTTP_InternalServerError
from wsgiref import simple_server

# Configuration for Falcon API
API = falcon.API()
API.req_options.media = {'zip'}


# Route for decompressing files
class DecompressionResource:
    def on_post(self, req, resp):
        """
        Handles POST requests for decompressing files.
        The compressed file is expected to be sent in the request body.
        """
        # Get the uploaded file from the request
        file = req.get_param('zip', required=True)
        file_path = file['filename']
        file_data = file['body']

        try:
            # Extract the compressed file content
            self.extract_zip(file_path, file_data)
            resp.status = falcon.HTTP_200
            resp.media = {'message': 'File decompressed successfully'}
        except zipfile.BadZipFile:
            raise falcon.HTTP_BadRequest('Invalid zip file', 'The file provided is not a valid zip file')
        except Exception as e:
            raise falcon.HTTP_InternalServerError(
                title='An error occurred',
                description=str(e),
            )

    def extract_zip(self, file_path, file_data):
        """
        Extracts the content of a zip file.
        Args:
        file_path (str): The path where the zip file should be saved temporarily.
        file_data (bytes): The content of the zip file.
        """
        # Save the zip file content to a temporary file
        with open(file_path, 'wb') as temp_zip:
            temp_zip.write(file_data)

        # Extract the zip file content
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(os.path.splitext(file_path)[0])

        # Remove the temporary zip file
        os.remove(file_path)


# Add the resource to the API
decompression_resource = DecompressionResource()
API.add_route('/decompress', decompression_resource)


# Entry point for the application
def main():
    # Run the WSGI server
    httpd = simple_server.make_server('0.0.0.0', 8000, API)
    print('Serving on port 8000...')
    httpd.serve_forever()


if __name__ == '__main__':
    main()
